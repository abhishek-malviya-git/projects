# 🚀 SmartOps GenAi-Powered Integrated Platform
**_Agentic AI & Generative AI for Intelligent Operations & Automation_**  

## 📌 Overview  
The **SmartOps GenAi-Powered Integrated Platform** leverages **Agentic AI** and **Generative AI** to provide an intelligent, automated decision-making and troubleshooting system. This platform integrates:  
✔ **Conversational GenAi** via SmartOps Chatbot (Gradio UI)  
✔ **Agentic Action Hub** for AI-powered automation  
✔ **Flask-based Alert Receiver** for processing real-time system alerts  
✔ **Monitoring System** to detect system anomalies  

The **Agentic AI** capabilities allow **AI-driven task execution**, while **Generative AI** enables intelligent problem-solving and automation. This platform helps IT and operations teams optimize workflows, resolve issues proactively, and reduce manual intervention.  

## 🗂️ Project Folder Structure  

```
SmartOps-Integrated-Platform/
│── src/
│   ├── main.py                       # 🚀 Launches the entire platform (Gradio UI + Flask + Monitoring)
│   ├── agents/
│   │   ├── launch_flask_and_monitoring_app.py  # 🔥 Starts Flask & Monitoring (No UI)
│   │   ├── GenAI_SmartOps_Integrated_Platform.py  # 🤖 Starts SmartOps Chatbot & Agentic Hub (Gradio UI)
│   │   ├── flask_alert_receiver_agent.py  # 🌐 Flask server for alert handling
│   ├── scripts/
│   │   ├── monitoring_scripts/
│   │   │   ├── m_temp_files_size_monitoring.py  # 📊 Monitors system temp file size
│── docs/                               # 📖 Documentation & API References
│── requirements.txt                    # 📦 Python dependencies
│── README.md                           # 📄 Project documentation (You're here!)
│── .gitignore                           # 🚫 Files to ignore in Git
```

## 🎯 Key Features  

### 1️⃣ SmartOps Chatbot & Agentic Action Hub (via **Gradio UI**)  
- **Conversational AI**: AI-powered chatbot for troubleshooting & insights  
- **Agentic AI Execution**: Automate tasks using the **Agentic Action Hub**  
- **Multi-Tab UI**: Separate tabs for chatbot & automated action execution  

### 2️⃣ Flask-Based Alert Receiver  
- Handles **real-time alerts** and triggers automated resolutions  
- Supports **JSON-based API requests** for external integrations  
- Flask server listens on `http://127.0.0.1:5006/alert`  

### 3️⃣ Monitoring System  
- **Monitors system health, disk usage, and temp file size**  
- **Triggers alerts** when thresholds exceed  
- Works in **real-time with Flask-based alerting**  

## 🚀 Getting Started  

### 🔧 Prerequisites  
- Python **3.8+**  
- Install dependencies:  
  ```sh
  pip install -r requirements.txt
  ```

### ▶️ Running the Platform  

#### 1️⃣ Start Full Platform (Chatbot + Agentic AI + Flask + Monitoring)
```sh
python src/main.py
```
🔹 **This will launch**:  
✔ **SmartOps Chatbot & Agentic Hub** (Gradio UI)  
✔ **Flask Alert Receiver**  
✔ **Monitoring System**  

#### 2️⃣ Start Flask & Monitoring Only
```sh
python src/agents/launch_flask_and_monitoring_app.py
```
🔹 **This will launch**:  
✔ **Flask Alert Receiver**  
✔ **Monitoring System**  

#### 3️⃣ Start SmartOps Chatbot & Agentic AI UI Only
```sh
python src/agents/GenAI_SmartOps_Integrated_Platform.py
```
🔹 **This will launch**:  
✔ **SmartOps Chatbot**  
✔ **Agentic Action Hub** (Gradio UI)  

## 🖥️ API Usage  

### 1️⃣ Sending an Alert (Simulating a CURL Request)
```sh
curl -X POST http://127.0.0.1:5006/alert -H "Content-Type: application/json" -d "{\"status\": \"firing\", \"message\": \"Check system memory usage!\"}"
```
📌 **Python Equivalent**
```python
import requests

url = "http://127.0.0.1:5006/alert"
headers = {"Content-Type": "application/json"}
data = {"status": "firing", "message": "Check system memory usage!"}

response = requests.post(url, json=data)
print(response.json())
```

### 2️⃣ Checking Flask Health Status
```sh
curl http://127.0.0.1:5006/
```
📌 **Python Equivalent**
```python
requests.get("http://127.0.0.1:5006/").text
```

## 🤖 Technologies Used  

| Technology | Description |
|------------|-------------|
| **Python** | Backend language |
| **Gradio** | Web UI for chatbot & automation hub |
| **Flask** | REST API & alert receiver |
| **Subprocess** | Background process handling |
| **Agentic AI** | AI-powered task execution |
| **Generative AI** | AI-based chatbot responses |

## 🔍 Troubleshooting  

### 1️⃣ Flask Server Not Starting?  
- Run: `netstat -ano | findstr :5006` to check if the port is already in use.  
- Kill the existing process:  
  ```sh
  taskkill /PID <PID> /F
  ```

### 2️⃣ Gradio App Not Opening Automatically?  
- Open manually in browser:  
  ```
  http://127.0.0.1:<your_port>
  ```

## 👨‍💻 Contribution Guidelines  
1. **Fork** the repository  
2. **Create** a feature branch (`git checkout -b feature-branch`)  
3. **Commit** your changes (`git commit -m "Added new feature"`)  
4. **Push** to GitHub (`git push origin feature-branch`)  
5. **Open a Pull Request** 🚀  

## 📜 License  
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.  

## 📧 Contact & Support  
💡 **Have questions or suggestions?** Reach out via:  
📩 **Email**: `abhishekmalviya214@gmail.com`  
🔗 **GitHub Issues**: [Open an issue](https://github.com/abhishek-malviya-git/issues)  

> **🚀 SmartOps AI – Redefining IT & Operations Automation with AI & Intelligent Agents!**  
