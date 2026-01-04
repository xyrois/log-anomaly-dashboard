# 🔍 Log Anomaly Detection Dashboard

An intelligent log analysis tool that parses web server access logs, detects suspicious patterns, and visualizes anomalies through an interactive dashboard.

## ✨ Features

- **Automated Log Parsing**: Extracts IP addresses, timestamps, HTTP methods, endpoints, and status codes from Apache-style access logs
- **Anomaly Detection**: Identifies suspicious patterns including:
  - Repeated authentication failures (potential brute force attacks)
  - High request volumes from single IPs (potential DDoS)
  - Unauthorized access attempts to restricted endpoints
- **Interactive Dashboard**: Real-time visualization with metrics, charts, and highlighted anomalies
- **Severity Classification**: Anomalies ranked by severity (HIGH/MEDIUM) with color coding

## 🛠️ Tech Stack

- **Python 3.9+**
- **Pandas**: Data manipulation and analysis
- **Streamlit**: Interactive web dashboard
- **Plotly**: Dynamic data visualizations
- **Regex**: Log pattern matching

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/log-anomaly-dashboard.git
cd log-anomaly-dashboard
```

2. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### 1. Parse the Logs
Place your access log file in the project directory and run:
```bash
python3 parser.py
```

This creates `parsed_logs.csv` with structured data and additional features like error flags and IP request counts.

### 2. Detect Anomalies (Optional)
Run the anomaly detector standalone:
```bash
python3 anomaly_detector.py
```

This generates `anomalies.csv` with detected suspicious patterns.

### 3. Launch the Dashboard
Start the interactive Streamlit dashboard:
```bash
streamlit run dashboard.py
```

The dashboard opens in your browser at `http://localhost:8501`

## 📋 Log Format

The parser expects Apache Common Log Format:
```
192.168.1.10 - - [01/Jan/2026:02:13:20 +0000] "GET /login HTTP/1.1" 401 -
```

## 📁 Project Structure
```
log-anomaly-dashboard/
├── access.log              # Input: Raw server logs
├── parser.py               # Parses logs and extracts features
├── anomaly_detector.py     # Detects suspicious patterns
├── dashboard.py            # Streamlit visualization dashboard
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## 🎯 Anomaly Detection Rules

| Anomaly Type | Threshold | Severity |
|-------------|-----------|----------|
| Repeated Auth Failures | ≥3 failed attempts from same IP | HIGH |
| High Request Volume | >10 requests from same IP | MEDIUM |
| Unauthorized Access | 403 status on admin endpoints | HIGH |

## 📊 Dashboard Metrics

- **Total Requests**: Count of all log entries
- **Unique IPs**: Number of distinct IP addresses
- **Error Responses**: Count of 4xx and 5xx status codes
- **Anomalies Detected**: Number of suspicious patterns found

## 📈 Visualizations

- Status code distribution (bar chart)
- Top 10 IPs by request count (horizontal bar chart)
- Request timeline by status code (line chart with markers)
- Anomaly table with severity highlighting

## 💡 Example Output
```
✓ Parsed logs saved to parsed_logs.csv
✓ Total entries: 5
✓ Unique IPs: 2
✓ Error responses: 4

✓ Detected 2 anomalies
┌─────────────────────────────┬──────────────┬───────┬──────────┐
│ Type                        │ IP           │ Count │ Severity │
├─────────────────────────────┼──────────────┼───────┼──────────┤
│ Repeated Auth Failure       │ 192.168.1.10 │ 3     │ HIGH     │
│ Unauthorized Access Attempt │ 203.0.113.9  │ 2     │ HIGH     │
└─────────────────────────────┴──────────────┴───────┴──────────┘
```

## 🔮 Future Enhancements

- [ ] Machine learning-based anomaly detection
- [ ] Real-time log streaming
- [ ] Email/Slack alerts for critical anomalies
- [ ] Geographic IP visualization
- [ ] Export anomaly reports (PDF/JSON)
- [ ] Configurable detection thresholds
- [ ] Support for multiple log formats

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

Built with Brinta Kundu
