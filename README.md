# 🛡️ CreditPulse Autonomous ML Risk System

CreditPulse-AI is an end-to-end, high-utility machine learning application built with **Streamlit** and **Scikit-Learn**. It functions as an automated portfolio auditor, automated card-control switcher, and financial statement generator for credit risk management ecosystems.


🌐 **Live Interactive Web App:** [Launch Live Streamlit Dashboard](https://creditpulse-ai-ow7sdnqsrbt6yf4ddtrxmc.streamlit.app/)
## 🖥️ Project Presentation Pitch Deck

[![Pitch Deck PDF](https://shields.io)](https://github.com/SRINIVASTA/CreditPulse-AI/blob/main/CreditPulse-AI%20Pitch%20Deck.pdf)

📌 *Note for Judges: Click the red badge above to open our complete **Project Underwriting Pitch Deck PDF** directly within GitHub's native, interactive document viewer.*


---

## 🚀 Core Platform Features

* **Interactive Data Intake**: Seamless ingestion engine accepting credit transaction metrics via raw `.csv` or formatted `.xlsx` files.
* **Automatic ML Training**: Real-time training using a Scikit-Learn `RandomForestClassifier` optimized with custom max-depth settings for predictable classification tracking.
* **Waterfall Decision Engine**: A cascading conditional auditor that prioritizes default prediction risk and sudden behavioral balance vectors over baseline utilization scores.
* **Audit-Ready Statement Generation**: Dynamic, localized client documentation rendering powered by the ReportLab layout matrix with built-in multicurrency support (`₹` and `$`).
* **Explainable AI Analytics**: Live dashboard performance blocks plotting Receiver Operating Characteristic (ROC) curves, calculated Area Under Curve (AUC), and relative structural feature weights.

---

## ⚙️ Mathematical Transformations & Logic Engine

### 1. Simulated Default Probability Generation
For synthetic evaluation, baseline user behavior default boundaries are mapped using the equation:
$$\text{Probability} = 0.1 + (\text{PAY\_0} \times 0.2) + \left(\frac{\text{BILL\_AMT1}}{\text{LIMIT\_BAL}} \times 0.3\right)$$
*Values are strictly bound using standard array clipping `[0.0, 1.0]` to guarantee statistical validity during downstream binomial distribution sampling.*

### 2. Defensive Feature Engineering
To prevent fatal application failure (`ZeroDivisionError` or infinite `NaN` errors), all vectors are transformed using boundary safeguards:
* **Card Utilization (`UTIL_RATE`)**: Evaluated cleanly against a clipped lower boundary of $1$ on the denominator:
  $$\text{UTIL\_RATE} = \frac{\text{BILL\_AMT1}}{\max(1, \text{LIMIT\_BAL})}$$
* **Velocity Shift (`SPENDING_JUMP`)**: Mitigates zero-balance histories with conditional matrix scaling:
  $$\text{SPENDING\_JUMP} = \begin{cases} \frac{\text{BILL\_AMT1}}{\text{BILL\_AMT2}}, & \text{if } \text{BILL\_AMT2} > 0 \\ 1.0, & \text{otherwise} \end{cases}$$

---

## 📑 Priority Strategic Decision Waterfall

The system reads portfolios through a top-down priority cascade inside the `ai_auditor` engine. Accounts stop evaluating immediately at the first triggered match:

| Execution Priority | Strategy Segment | Visual Anchor | Technical Trigger Condition |
| :--- | :--- | :---: | :--- |
| **Priority 1** | AI RISK BLOCK | 🛑 | Calculated Model Probability $\ge$ Sidebar Threshold (`ml_threshold`) |
| **Priority 2** | SECURITY BLOCK | ⚠️ | Velocity Shift Velocity Jump Scaling: $\text{SPENDING\_JUMP} \ge 5.0\text{x}$ |
| **Priority 3** | NUDGE TARGET | 🟡 | Repayment status clean ($\text{PAY\_0} \le 0$) **AND** Utilization $\text{UTIL\_RATE} > 80\%$ |
| **Priority 4** | GROWTH TARGET | 🟢 | Repayment status clean ($\text{PAY\_0} \le 0$) **AND** Utilization $\text{UTIL\_RATE} < 25\%$ |
| **Priority 5** | STABLE | ✅ | Default fall-through state when no operational risk markers are met |

---

## 🛠️ Installation & Local Setup

Ensure you have Python installed locally on your system before proceeding.

### 1. Clone the Project
```bash
git clone https://github.com
cd creditpulse-ai
```

### 2. Install Required Dependencies
Initialize your virtual environment and install the required numerical computing, reporting, and dashboarding frameworks:
```bash
pip install streamlit pandas numpy matplotlib scikit-learn reportlab
```

### 3. Run the Application
Boot the Streamlit orchestration controller from your command-line workspace:
```bash
streamlit run app.py
```

---

## 📂 Project Architecture

```filepath
├── app.py                 # Core Streamlit app orchestration & custom CSS dashboard
├── requirements.txt       # Hardcoded python framework and styling engine versions
└── README.md              # Project onboarding documentation, math, and engine rule logs
```

---

## 📋 Data Schema Blueprint
To run processing scripts seamlessly, verification data sources must contain these precise column arrays:
* `ID`: Primary key tracking unique credit accounts.
* `LIMIT_BAL`: Full allocated account credit ceiling.
* `PAY_0`: Most recent repayment timeline status index.
* `BILL_AMT1`: Total statement calculation for the current active billing cycle.
* `BILL_AMT2`: Prior historical billing record statement values.
* `PAY_AMT1`: The most recent transaction remittance total.
* `default payment next month`: Binary matrix labels ($0$ or $1$) indicating target tracking metrics.
---

**SRINIVASTA / CreditPulse-AI**  
*Building the future of autonomous risk management.*

*Note: Any blank rows trailing below your data grids inside sheet ranges are automatically detected, filtered out, and logged as system-rejected anomaly rows.*
> ⚠️ **IMPORTANT COPYRIGHT NOTICE**
> 
> **All Rights Reserved © 2026 T A Srinivas.**
> This repository is strictly for portfolio viewing purposes. **DO NOT COPY, CLONE, OR REDISTRIBUTE** this code. Stolen copies or unauthorized forks will be reported immediately for a GitHub copyright takedown.

* **Lead Architect & Developer:** [Srinivasta](https://github.com/SRINIVASTA)

### 🌐 Let’s Connect

- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/srinivas-t-a-557637119/)  
- [![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/srinivasta)  
- [![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:tasrinivass@gmail.com)  
- [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/srinivasta)
- [![Website](https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=website&logoColor=white)](https://srinivasta/github.io)







