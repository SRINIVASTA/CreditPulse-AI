# 🚀 CreditPulse-AI: Autonomous Risk Dashboard

Developed by **SRINIVASTA**, CreditPulse-AI is a high-performance, autonomous credit monitoring system built with **Streamlit** and **Scikit-Learn**. It transforms static financial data into an interactive decision-making engine with real-time portfolio grading.

[![Streamlit App](https://streamlit.io)](https://your-app-link.streamlit.app)
![Python](https://shields.io)

## ✨ Key Features

- **🧠 Autonomous Auditor:** Uses a decision logic engine to instantly categorize accounts into *Growth, Stable, Nudge,* or *Critical Block*.
- **📊 3D Health Analytics:** An interactive 3D portfolio view that updates live as you adjust policies.
- **🏷️ Real-Time Health Grading:** The system live-evaluates the entire portfolio from **💎 EXCELLENT** to **🔴 BAD** based on your current risk tolerance.
- **🛠️ Dynamic Policy Engine:** Tweak Risk Thresholds and Utilization Limits via sidebar sliders to see the immediate business impact.
- **📁 Universal File Intake:** Optimized for UCI Credit Card datasets; supports CSV and Excel with automatic header management.

## 🚦 Portfolio Grading System

The engine evaluates your current configuration against real-time data:
- **💎 EXCELLENT**: High growth potential (>30% accounts for limit increases).
- **🟢 VERY GOOD**: Healthy, stable portfolio with minimal delinquency.
- **🟠 GOOD**: Manageable risk with standard maintenance.
- **🔴 BAD**: High-risk environment requiring immediate intervention (>20% blocks).

## 🛠️ Quick Start

1. **Clone the Project**
   ```bash
   git clone https://github.com
   cd CreditPulse-AI
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Dashboard**
   ```bash
   streamlit run app.py
   ```

## 📦 Requirements
- `streamlit`
- `pandas`
- `numpy`
- `matplotlib`
- `scikit-learn`
- `openpyxl`

---
**SRINIVASTA / CreditPulse-AI**  
*Building the future of autonomous risk management.*
