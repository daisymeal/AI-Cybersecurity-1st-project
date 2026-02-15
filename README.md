# 🛡️ AI-Powered Autonomous Network Defense System

**A localized SOAR (Security Orchestration, Automation, and Response) pipeline powered by Intel Core Ultra NPU.**

## 📌 Project Overview
This project demonstrates a next-generation approach to cybersecurity: moving threat detection from the cloud to the **Edge**. By leveraging the **Intel NPU (Neural Processing Unit)** on a standard laptop, this system analyzes network traffic in real-time and triggers automated defense protocols without relying on external servers.

### 🌟 Key Features
* **Edge AI Analysis:** Python-based engine running on local NPU hardware (OpenVINO™).
* **Deep Packet Inspection (DPI):** Regex-based payload scanning for SQL Injection, XSS, and Malware signatures.
* **Automated Response:** n8n workflow orchestrates instant alerts (Email/Slack) and blocking actions.
* **Privacy-First:** Data never leaves the local network for analysis.

## 🛠️ Tech Stack
* **Hardware:** Intel Core Ultra 7 (NPU)
* **Language:** Python 3.14 (FastAPI, Uvicorn)
* **AI Inference:** OpenVINO™ Toolkit
* **Orchestration:** n8n (Docker)
* **Protocol:** HTTP/REST Webhooks

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/daisymeal/AI-Cybersecurity-1st-project.git](https://github.com/daisymeal/AI-Cybersecurity-1st-project.git)
cd ai-cyber

2. Install Dependencies
Bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
3. Run the AI Engine
Bash
uvicorn ai_engine:app --reload --port 8000
4. Import n8n Workflow
Open n8n (localhost:5678).

Go to Workflows > Import from File.

Select n8n_workflow.json from this repository.

Configure your SMTP credentials.

🧪 Testing (Simulation)
Send a simulated malicious payload via PowerShell:

PowerShell
$body = @{ ip="192.168.1.50"; size=120; payload="admin' OR 1=1 --" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:5678/webhook-test/..." -Body $body

📄 License
MIT License - Free to use for educational purposes