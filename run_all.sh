#!/bin/bash

echo "==========================================="
echo "        Honeypot ML Automation Suite        "
echo "==========================================="

echo
echo "[*] Cleaning up old logs and processes..."
rm -f honeypot_logs.json honeypot_out.log encoded_honeypot_logs.csv attack_classifier.pkl model_metrics.txt exported_logs_with_predictions.csv exported_logs_with_predictions.json honeypot_report.html
pkill -f honeypots 2>/dev/null

echo
echo "[*] Starting honeypots in background..."
python3 -m honeypots --setup ssh:2222,ftp:2121,smtp:2525,http:8080 | tee honeypot_out.log &
HONEYPOT_PID=$!
sleep 3

echo
echo "[*] Running simulated attacks..."
python3 sim_attack.py

echo
echo "[*] Waiting for honeypots to flush logs (sleeping 6s)..."
sleep 6

echo
echo "[*] Stopping honeypots and saving logs..."
kill $HONEYPOT_PID 2>/dev/null
sleep 1

# Extract JSON log lines (if not already generated)
if [[ ! -f honeypot_logs.json ]]; then
    echo "[*] Attempting to extract JSON lines from honeypot_out.log..."
    grep '^{.*}$' honeypot_out.log > honeypot_logs.json
fi

echo
echo "[*] Encoding logs for ML training..."
python3 encode_logs.py

echo
echo "[*] Training the attack classifier..."
python3 train_model.py

echo
echo "[*] Evaluating the model..."
python3 evaluate_model.py

echo
echo "[*] Exporting logs with predictions..."
python3 export_logs_with_predictions.py

echo
echo "[*] Generating HTML report..."
python3 generate_report.py

echo
echo "✅ Automation complete! Opening dashboard..."
if command -v xdg-open >/dev/null 2>&1; then
    xdg-open honeypot_report.html
elif command -v open >/dev/null 2>&1; then
    open honeypot_report.html
else
    echo "Please open honeypot_report.html manually in your browser."
fi

echo
echo "All deliverables generated:"
ls -lh honeypot_report.html exported_logs_with_predictions.csv exported_logs_with_predictions.json model_metrics.txt 2>/dev/null

