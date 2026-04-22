#  Digital Cybersecurity Surveillance System (v2.1)

A **live digital cybersecurity surveillance system** designed to monitor identification code usage, detect behavioral anomalies, perform graph-based suspicious relationship analysis, and deliver risk-based decisions automatically.

## About the Tool

In modern environments, compromised credentials and shared accounts are significant vulnerabilities. This tool serves as an autonomous **Decision Engine** that processes access logs (who accessed what, when, and from which device) and intelligently determines whether an activity is normal or suspicious. 

It evaluates usage patterns using **rule-based anomaly detection** and visualizes relationships using **Graph Theory**, making it incredibly easy to identify a single user exploiting multiple IDs or a single ID being suspiciously shared across multiple devices.

###  Key Features
- **Multi-format Data Upload**: Supports uploading live access logs in `CSV`, `JSON`, and tabular `PDF` formats.
- **Data Validation & Sanitization**: Automatically checks ID formatting and handles missing/invalid entries securely.
- **Rule-Based Anomaly Detection**: Flags users who exceed standard login thresholds.
- **Behavioral Graph Analysis**: Creates relationship networks mapping `Users ↔ IDs ↔ Devices` to identify centralized points of failure or abuse.
- **Risk Scoring System**: Assigns qualitative scores (`Low`, `Medium`, `High`) and automated responses (`Allow`, `Flag`, `Block`).
- **Interactive UI**: A dark-mode, premium Streamlit dashboard to interactively visualize threats and download flagged reports.

##  Architecture

```text
├── app/
│   ├── main.py                 # Main execution pipeline
│   ├── validation.py           # Data sanitization and formatting
│   ├── anomaly_detector.py     # Threshold-based detection
│   ├── graph_analysis.py       # NetworkX relationship mapping
│   └── decision_engine.py      # Automated risk scoring & decisions
├── dashboard/
│   └── streamlit_dashboard.py  # Premium Streamlit UI
├── data/
│   └── access_logs.csv         # Sample dataset
├── outputs/                    # Exported analysis results
├── Dockerfile                  # Docker configuration
└── requirements.txt            # Python dependencies
```

## How to Run Locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Ruhisingh4/Survilleance2.1-Cybersecurity-and-blockchain.git
   cd Survilleance2.1-Cybersecurity-and-blockchain
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Live Dashboard**
   ```bash
   streamlit run dashboard/streamlit_dashboard.py
   ```

## Docker Deployment

To run this application via Docker:

```bash
docker build -t cybersec-surveillance .
docker run -p 8501:8501 cybersec-surveillance
```
The app will be available at `http://localhost:8501`.

##Cloud Deployment (Render)
This project is deployment-ready for platforms like **Render**:
1. Connect your GitHub repo to Render.
2. Select **Web Service** -> **Docker**.
3. Render will automatically build the `Dockerfile` and expose port `8501`.
