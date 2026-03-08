# 🚀 AI-Powered OS Monitor Pro

A state-of-the-art, AI-powered system monitoring tool that collects real-time system metrics, logs them into a durable database, and uses machine learning for anomaly detection. 

The project features a lightweight backend telemetry collector, an advanced **Machine Learning Pipeline (StandardScaler + IsolationForest)**, and a highly polished **PyQt5/PyQtGraph-based UI** for buttery-smooth 60 FPS visualization.

## ✨ Features

- **5-Dimensional Telemetry**: Tracks CPU, Memory, Disk, Network Velocity, and **Swap Memory** in real-time.
- **Premium Dark Mode UI**: A stunning `QPalette` Fusion dark theme with a modern card-based layout and synchronized grid charts.
- **60 FPS Rendering**: Uses `pyqtgraph` (bypassing slow matplotlib redraws) for instantaneous, lag-free data plotting.
- **AI Anomaly Detection**: Unsupervised `IsolationForest` continuously calculates feature-space distances to flag spontaneous background performance spikes.
- **Native OS Integration**: 
  - Triggers native Windows Desktop Toast Notifications (`plyer`) instantly upon an anomaly.
  - Minimizes to the System Tray for true background execution.
- **Durable Logging**: Every telemetry tick and anomaly evaluation is permanently stored in an append-only `SQLite3` database for historical audits.

---

## 🛠 Project Structure

```text
AI-Powered-OS-Monitor/
├── backend-monitoring/
│   ├── database.py             # Schema definition & recreation scripts
│   └── monitor_with_anomaly.py # The background collector, ML evaluator, and alerter
├── frontend-ui/
│   ├── main.py                 # The Pyqt5/Pyqtgraph High-Performance Dashboard
│   ├── system_logs.db          # SQLite Database
│   └── system_stats.txt        # Inter-process communication buffer
├── ml-ai/
│   ├── anomaly_detection.py    # Training script to build the StandardScaler pipeline
│   └── isolation_forest_model.pkl # The serialized, active AI model
├── requirements.txt
└── README.md
```

---

## 💻 Requirements

- **Python 3.10+** (Tested on 3.12)
- Built on top of `PyQt5`, `pyqtgraph`, `scikit-learn`, `psutil`, and `plyer`.
- For the full list, see [requirements.txt](requirements.txt).

---

## 🚀 Setup Instructions

1. **Clone the Repository:**
```bash
git clone https://github.com/yourusername/AI-Powered-OS-Monitor.git
cd AI-Powered-OS-Monitor
```

2. **Create and Activate a Virtual Environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Initialize the Database:**  
*Run to create/recreate the 5-feature database schema.*
```bash
python backend-monitoring/database.py
```

5. **Train the Initial Anomaly Model:**  
*Will train on the existing database, or explicitly generate synthetic baseline data.*
```bash
python ml-ai/anomaly_detection.py
```

---

## 🎮 Usage

You need two active terminals (both with your `venv` activated) to run the full application suite.

**Terminal 1: Start the Background AI Telemetry Agent**
```bash
python backend-monitoring/monitor_with_anomaly.py
```
*This script will run silently in the background. It will log data, evaluate AI predictions, and trigger native Windows Toast Notifications if a critical anomaly occurs.*

**Terminal 2: Launch the Pro Dashboard**
```bash
python frontend-ui/main.py
```
*The PyQt5 Pro interface will open displaying your real-time metrics, dynamically plotted smooth charts, and a master system Status Indicator.*

### Simulating an Anomaly
If you want to manually test the UI and OS notification integrations without waiting for a real system spike:
1. Keep both the frontend and backend running.
2. Open `frontend-ui/system_stats.txt` in a text editor.
3. The string looks like this: `12.0, 45.3, 80.1, 0.5, 40.0, 0`
4. Change the final `0` to a `1` and save the file.
5. The UI will instantly turn red, and a Desktop Notification will explicitly fire!

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit pull requests. Ensure your code follows the project structure and is well-documented. For major changes involving the UI or the AI Pipeline, open an issue first to discuss what you would like to change.

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
