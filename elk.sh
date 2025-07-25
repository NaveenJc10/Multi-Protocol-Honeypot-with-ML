#!/bin/bash

set -e

echo "[*] Cleaning up old containers and network if any..."
sudo docker rm -f elasticsearch kibana 2>/dev/null || true
sudo docker network rm elk-net 2>/dev/null || true

echo "[*] Creating Docker network elk-net..."
sudo docker network create elk-net

echo "[*] Starting Elasticsearch (dev mode, no security)..."
sudo docker run -d \
  --name elasticsearch \
  --network elk-net \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms1g -Xmx1g" \
  -e "xpack.security.enabled=false" \
  -p 9200:9200 \
  -v elasticsearch-data:/usr/share/elasticsearch/data \
  docker.elastic.co/elasticsearch/elasticsearch:8.5.3

echo "[*] Starting Kibana..."
sudo docker run -d \
  --name kibana \
  --network elk-net \
  -e "ELASTICSEARCH_HOSTS=http://elasticsearch:9200" \
  -p 5601:5601 \
  -v kibana-data:/usr/share/kibana/data \
  docker.elastic.co/kibana/kibana:8.5.3

echo "[*] Waiting 90 seconds for Elasticsearch & Kibana to be fully up..."
sleep 90

echo
echo "✅ ELK is up!"
echo "   - Kibana:      http://localhost:5601"
echo "   - Elasticsearch: http://localhost:9200"
echo "   - Username/password: Not needed (security disabled for demo/dev)"
echo
echo "📢 Ready for log ingestion and dashboard creation!"

