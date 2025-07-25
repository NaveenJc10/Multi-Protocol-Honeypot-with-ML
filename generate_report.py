import pandas as pd
import os
import datetime

csv_file = "encoded_honeypot_logs.csv"
html_file = "honeypot_report.html"

if not os.path.exists(csv_file):
    with open(html_file, "w") as f:
        f.write("<h2>No CSV log data found. Please run your honeypot and attacks first.</h2>")
    print(f"⚠ No CSV found. Created {html_file} with error message.")
    exit()

# Read data
df = pd.read_csv(csv_file)

# Prepare data for JS
table_html = df.tail(100).to_html(classes="data-table", index=False)

# Prepare summary
attack_counts = df['attack_type'].value_counts().to_dict()
server_counts = df['server'].value_counts().to_dict()
trend_data = df.groupby(df['timestamp'].str[:10])['attack_type'].value_counts().unstack(fill_value=0)

# Chart.js data strings
pie_labels = list(attack_counts.keys())
pie_values = list(attack_counts.values())

bar_labels = list(server_counts.keys())
bar_values = list(server_counts.values())

trend_labels = list(trend_data.index)
trend_datasets = []
for atk in trend_data.columns:
    trend_datasets.append({
        "label": atk,
        "data": list(trend_data[atk].values)
    })

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(html_file, "w") as f:
    f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Honeypot Attack Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2em; }}
        h1, h2 {{ color: #333; }}
        .container {{ max-width: 1200px; margin: auto; }}
        .charts {{ display: flex; gap: 3em; flex-wrap: wrap; }}
        .chart-block {{ flex: 1; min-width: 350px; }}
        .data-table {{ width: 100%; border-collapse: collapse; margin-top: 2em; }}
        .data-table th, .data-table td {{ border: 1px solid #ddd; padding: 8px; }}
        .data-table th {{ background: #f4f4f4; }}
        .controls {{ margin-bottom: 1em; }}
        .btn {{ background: #1966d2; color: #fff; border: none; padding: 10px 18px; cursor: pointer; border-radius: 5px; margin-right: 1em; }}
        .btn:hover {{ background: #1452a1; }}
    </style>
</head>
<body>
<div class="container">
    <h1>Honeypot Attack Dashboard</h1>
    <p>Last updated: {timestamp}</p>

    <div class="controls">
        <label for="attackFilter"><b>Filter by Attack Type:</b></label>
        <select id="attackFilter">
            <option value="">All</option>
            {''.join([f'<option value="{atk}">{atk}</option>' for atk in pie_labels])}
        </select>
        <input type="text" id="logSearch" placeholder="Search logs..." style="padding: 7px; margin-left: 1em;">
        <button class="btn" onclick="exportPDF()">Export as PDF</button>
        <button class="btn" onclick="location.reload()">Refresh Now</button>
    </div>

    <div class="charts">
        <div class="chart-block">
            <canvas id="pieChart"></canvas>
        </div>
        <div class="chart-block">
            <canvas id="barChart"></canvas>
        </div>
        <div class="chart-block" style="min-width: 600px;">
            <canvas id="trendChart"></canvas>
        </div>
    </div>

    <h2>Recent Logs</h2>
    <div id="logTable">
        {table_html}
    </div>
</div>

<script>
    // PIE chart
    const pieCtx = document.getElementById('pieChart').getContext('2d');
    new Chart(pieCtx, {{
        type: 'pie',
        data: {{
            labels: {pie_labels},
            datasets: [{{ data: {pie_values}, backgroundColor: ['#1966d2', '#28b463', '#e74c3c', '#f7b731', '#8e44ad', '#16a085'] }}]
        }},
        options: {{ plugins: {{ legend: {{ position: 'bottom' }} }} }}
    }});

    // BAR chart
    const barCtx = document.getElementById('barChart').getContext('2d');
    new Chart(barCtx, {{
        type: 'bar',
        data: {{
            labels: {bar_labels},
            datasets: [{{ label: 'Count', data: {bar_values}, backgroundColor: '#1966d2' }}]
        }},
        options: {{ scales: {{ y: {{ beginAtZero: true }} }} }}
    }});

    // Trend line chart
    const trendCtx = document.getElementById('trendChart').getContext('2d');
    new Chart(trendCtx, {{
        type: 'line',
        data: {{
            labels: {trend_labels},
            datasets: {trend_datasets}
        }},
        options: {{ plugins: {{ legend: {{ position: 'bottom' }} }} }}
    }});

    // Filter/search logs
    const attackFilter = document.getElementById('attackFilter');
    const logSearch = document.getElementById('logSearch');
    attackFilter.addEventListener('change', filterTable);
    logSearch.addEventListener('input', filterTable);

    function filterTable() {{
        let type = attackFilter.value.toLowerCase();
        let search = logSearch.value.toLowerCase();
        let table = document.querySelector('#logTable table');
        for (let row of table.rows) {{
            if (row.rowIndex === 0) continue; // skip header
            let cells = Array.from(row.cells).map(td => td.textContent.toLowerCase());
            let matchesType = !type || cells.join(' ').includes(type);
            let matchesSearch = !search || cells.join(' ').includes(search);
            row.style.display = (matchesType && matchesSearch) ? '' : 'none';
        }}
    }}

    // Export to PDF
    function exportPDF() {{
        var doc = new jspdf.jsPDF({{orientation:'landscape', unit:'pt', format:'a4'}});
        doc.html(document.body, {{
            callback: function (doc) {{
                doc.save('honeypot_report.pdf');
            }},
            x: 12, y: 12
        }});
    }}

    // Auto refresh every 60 seconds
    setTimeout(() => location.reload(), 60000);
</script>
</body>
</html>
""")
print(f"✅ Report generated as {html_file} with charts, filter/search, PDF export, and auto-refresh!")

