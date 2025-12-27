
# Enhancing Glastopf Honeypot with Multi-Protocol Support & Machine Learning

## 📌 Project Overview
This project enhances **Glastopf**, a traditional HTTP-based honeypot, by transforming it into a **dynamic multi-protocol honeypot** capable of detecting and analyzing modern **multi-vector cyberattacks**.

The enhanced system introduces **dynamic protocol toggling** and **machine learning–driven protocol detection**, allowing the honeypot to seamlessly emulate multiple services and adapt to attacker behavior in real time.

Supported protocols include **HTTP, SSH, FTP, and SMTP**, enabling comprehensive monitoring of attacks that span multiple communication channels.

> 🎓 **Final Year Project (Capstone)**  
> BSc (Hons) Information Technology (Computer Networking & Security)  
> Sunway University

---

## 🎯 Objectives
- Transform Glastopf from a **single-protocol (HTTP)** honeypot into a **multi-protocol honeypot**
- Implement **dynamic protocol detection and toggling**
- Integrate **machine learning** for real-time protocol identification and adaptive responses
- Capture detailed attacker **Tactics, Techniques, and Procedures (TTPs)**
- Improve threat intelligence for **multi-stage, multi-protocol attacks**

---

## 🏗️ System Architecture
The enhanced architecture introduces:
- **Dynamic protocol detection** using ML classifiers
- **Protocol-specific emulation modules** (HTTP, SSH, FTP, SMTP)
- **Adaptive response generation** to sustain attacker engagement
- **Centralized logging and visualization**

Key components:
- Protocol Dispatcher  
- Machine Learning Engine (SVM, Random Forest)  
- High-interaction emulation modules  
- ELK Stack (Elasticsearch, Logstash, Kibana)

---

## 🤖 Machine Learning Integration
Machine learning is used to:
- Identify active protocols in real time
- Classify attack behavior based on traffic patterns
- Detect anomalies across multiple protocols
- Adapt honeypot responses dynamically

Models explored:
- **Random Forest Classifier**
- **Support Vector Machine (SVM)**

---

## 🔐 Supported Protocols
| Protocol | Purpose |
|--------|--------|
| HTTP | Web attacks (SQLi, XSS, RFI) |
| SSH | Brute-force attacks, lateral movement |
| FTP | Payload delivery, data exfiltration |
| SMTP | Phishing and email-based attacks |

---

## 📈 Performance Metrics

### System Performance
| Metric | Value |
|------|------|
| Protocol Detection Accuracy | 95% |
| Response Latency | 120 ms |
| Concurrent Sessions | 500+ |
| Anomaly Detection Rate | 92% |
| False Positive Rate | 3% |

### Comparison with Traditional Honeypots
| System | Protocols | Accuracy | F1-Score | Scalability |
|------|-----------|----------|----------|-------------|
| **Enhanced Glastopf** | 4 | **95%** | **93%** | **500+** |
| Dionaea | 1–2 | 80–85% | 70–75% | 300 |
| Honeytrap | 1–2 | 80–85% | 70–75% | 400 |
| T-Pot | 3–4 | 85–90% | 75–80% | 450 |

### ML Model Performance
```
Random Forest Classifier:
├── Training Accuracy: 96.2%
├── Test Accuracy: 94.7%
├── Precision: 93.8%
├── Recall: 92.3%
└── F1-Score: 93.0%

SVM Classifier:
├── Training Accuracy: 91.5%
├── Test Accuracy: 89.2%
├── Precision: 88.5%
├── Recall: 87.7%
└── F1-Score: 88.1%
```

---

## 📁 Project Structure
```
enhanced-glastopf-honeypot/
│
├── controller.py
├── sim_attack.py
├── train_models.py
├── preprocessing.py
├── evaluate_models.py
├── run_all.sh
├── elk.sh
├── requirements.txt
├── config.yaml
│
├── honeypots/
│   ├── http/
│   ├── ssh/
│   ├── ftp/
│   └── smtp/
│
├── ml_models/
│   ├── classifiers/
│   ├── feature_extraction/
│   └── anomaly_detection/
│
├── logs/
│   ├── raw/
│   ├── processed/
│   └── exports/
│
├── dashboards/
│   ├── attack_overview.ndjson
│   ├── protocol_analysis.ndjson
│   └── ml_performance.ndjson
│
├── docker/
│   ├── docker-compose.yml
│   ├── Dockerfile.honeypot
│   └── Dockerfile.elk
│
├── docs/
│   ├── installation.md
│   ├── configuration.md
│   ├── api_reference.md
│   └── troubleshooting.md
│
└── tests/
    ├── unit/
    ├── integration/
    └── performance/
```

---

## ⚠️ Ethical & Legal Notice
This project is intended **strictly for academic research and defensive cybersecurity purposes**.  
Do **NOT** deploy this system on production or unauthorized networks.

---

## 🚀 Future Enhancements
- [ ] Additional protocol support (Telnet, DNS, etc.)
- [ ] Enhanced ML models (Deep Learning, Reinforcement Learning)
- [ ] Improved visualization dashboards
- [ ] Performance optimization
- [ ] Mobile/web interface
- [ ] Cloud deployment templates (AWS, Azure, GCP)
- [ ] Automated threat intelligence sharing


---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```





