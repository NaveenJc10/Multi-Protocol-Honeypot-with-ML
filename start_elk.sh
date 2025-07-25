#!/bin/bash
echo "[*] Starting ELK stack with Filebeat shipping logs..."
docker-compose up -d

echo "[*] Done. Access Kibana at: http://localhost:5601"
echo "[*] Default index pattern should pick up your honeypot logs in a minute."

