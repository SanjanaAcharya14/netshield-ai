# 🛡️ NetShield AI — Real-Time Network Anomaly Detection System

NetShield AI is a full-stack security telemetry platform that captures local network packets in real time, extracts structural feature metrics, and analyzes traffic flow using Machine Learning to identify potential cyber anomalies and network intrusions on the fly.

---

## ✨ Key Features

* **Live Packet Sniffing**: Uses `Scapy` and `Npcap` to intercept network traffic (IP, TCP, UDP, and custom protocols) on local interfaces without dropping frames.
* **AI-Powered Anomaly Detection**: Integrates an `Isolation Forest` unsupervised machine learning model to classify traffic behavior in real time based on packet sizes, frequencies, and structural dynamics.
* **Low-Latency Streaming**: Built with `FastAPI` and async `WebSockets` for thread-safe, continuous data transmission from the backend packet sniffer to the frontend.
* **Interactive Security Dashboard**: Real-time visualization powered by `Chart.js`, dynamically graphing live packet sizes and streaming security logs with color-coded threat alerts (`NORMAL` vs `SUSPICIOUS`).

---

## 🛠️ Tech Stack

* **Backend**: Python 3.x, FastAPI, Scapy, Scikit-Learn, Uvicorn
* **Frontend**: HTML5, CSS3, JavaScript (ES6+), Chart.js
* **Network Driver**: Npcap (Windows Packet Capture API)

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* Npcap installed with WinPcap compatibility enabled

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/SanjanaAcharya14/netshield-ai.git](https://github.com/SanjanaAcharya14/netshield-ai.git)
   cd netshield-ai
