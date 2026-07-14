import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="CreditPulse-AI (ML Engine)", layout="wide")

# --- CUSTOM CSS FOR BETTER VISUALS ---
st.markdown("""
    <style>
    .metric-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 10px;
    }
    .metric-title { font-size: 14px; color: #6c757d; font-weight: bold; }
    .metric-value { font-size: 24px; font-weight: bold; color: #212529; }
    </style>
""", unsafe_allow_html=True)

# --- 1. DATA INTAKE & AUTOMATIC ML TRAINING ---
@st.cache_data
def get_data(uploaded_file=None):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                return pd.read_csv(uploaded_file)
            else:
                return pd.read_excel(uploaded_file, header=1)
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return None
    else:
        # Fallback Mock Data generation
        np.random.seed(42)
        data_size = 1000  # Larger size for stable ML training
        
        # Simulating realistic behavioral data
        limit_bal = np.random.choice([10000, 20000, 50000, 100000, 200000], data_size)
        pay_0 = np.random.choice([-1, 0, 1, 2, 3], data_size, p=[0.3, 0.4, 0.15, 0.1, 0.05])
        bill_amt1 = np.random.uniform(500, 45000, data_size)
        bill_amt2 = bill_amt1 * np.random.uniform(0.5, 1.2, data_size)
        pay_amt1 = np.random.uniform(0, 5000, data_size)
        
        # Create a logical ground-truth target label where high risk patterns default more often
        prob = 0.1 + (pay_0 * 0.2) + ((bill_amt1/limit_bal) * 0.3)
        prob = np.clip(prob, 0, 1)
        default_next_month = np.random.binomial(1, prob)

        return pd.DataFrame({
            'ID': range(1, data_size + 1),
            'LIMIT_BAL': limit_bal,
            'PAY_0': pay_0,
            'BILL_AMT1': bill_amt1,
            'BILL_AMT2': bill_amt2,
            'PAY_AMT1': pay_amt1,
            'default payment next month': default_next_month
        })

@st.cache_resource
def train_ml_model(data):
    """Trains a Random Forest model on features to predict defaults."""
    # Features used for the prediction pipeline
    features = ['LIMIT_BAL', 'PAY_0', 'BILL_AMT1', 'BILL_AMT2', 'PAY_AMT1']
    target = 'default payment next month'
    
    X = data[features]
    y = data[target]
    
    # Train the Machine Learning Classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=6)
    model.fit(X, y)
    return model

# --- 2. SIDEBAR CONTROLS ---
st.sidebar.header("📁 Data Intake")
user_file = st.sidebar.file_uploader("Upload Credit CSV/Excel", type=["csv", "xls", "xlsx"])
df = get_data(user_file)

st.sidebar.header("🤖 ML Control Panel")
# Replaced rule sliders with a standard mathematical classification probability limit
ml_threshold = st.sidebar.slider(
    "Risk Decision Cut-off", 
    0.1, 0.9, 0.50, 
    help="Block accounts if the AI predicts a default probability higher than this value."
)

# --- 3. THE ML ENGINE & AUDITOR ---
if df is not None:
    required = ['LIMIT_BAL', 'PAY_0', 'BILL_AMT1', 'BILL_AMT2', 'PAY_AMT1', 'default payment next month']
    if all(col in df.columns for col in required):
        
        # Run ML Training Background Pipeline
        ml_model = train_ml_model(df)
        
        # Calculate engineered metrics for dashboard visualization
        df['UTIL_RATE'] = df['BILL_AMT1'] / (df['LIMIT_BAL'] + 1)
        df['SPENDING_JUMP'] = df['BILL_AMT1'] / (df['BILL_AMT2'] + 1)
        
        # Run ML inference to generate predictive risk probabilities
        features_list = ['LIMIT_BAL', 'PAY_0', 'BILL_AMT1', 'BILL_AMT2', 'PAY_AMT1']
        df['DEFAULT_PROBABILITY'] = ml_model.predict_proba(df[features_list])[:, 1]

        # Clean, explicit decision tree mapping based on ML outputs
        def ai_auditor(row):
            if row['DEFAULT_PROBABILITY'] >= ml_threshold: return "⛔ AI RISK BLOCK"
            if row['SPENDING_JUMP'] >= 5: return "🛡️ SECURITY BLOCK"
            if row['PAY_0'] <= 0 and row['UTIL_RATE'] > 0.80: return "📩 NUDGE"
            if row['PAY_0'] <= 0 and row['UTIL_RATE'] < 0.25: return "🌟 GROWTH"
            return "✅ STABLE"

        df['Autonomous_Action'] = df.apply(ai_auditor, axis=1)
        counts = df['Autonomous_Action'].value_counts()

        # --- 4. DYNAMIC HEALTH RATING LOGIC ---
        total = len(df)
        block_pct = (len(df[df['Autonomous_Action'] == '⛔ AI RISK BLOCK']) / total) * 100
        growth_pct = (len(df[df['Autonomous_Action'] == '🌟 GROWTH']) / total) * 100

        if block_pct > 25:
            status = "🚨 CRITICAL RISK"
            color = "red"
        elif block_pct > 12:
            status = "⚠️ CAUTION REQUIRED"
            color = "orange"
        elif growth_pct > 25:
            status = "🚀 EXPANSION ZONE"
            color = "blue"
        else:
            status = "🟢 HEALTHY PORTFOLIO"
            color = "green"

        # --- 5. THE DASHBOARD ---
        st.title("🚀 CreditPulse Autonomous ML Risk System")
        st.caption("Predictive artificial intelligence portfolio auditor & card control switcher")
        
        # HEALTH STATUS HEADER
        st.markdown(f"### Current Portfolio Status: :{color}[{status}]")
        st.write("---")
        
        # Executive Summary Metrics Block
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-box" style="border-left-color: #7f8c8d;"><div class="metric-title">📋 TOTAL PORTFOLIO</div><div class="metric-value">{total} Accounts</div></div>', unsafe_allow_html=True)
        with m2:
            risk_block_count = len(df[df['Autonomous_Action'] == "⛔ AI RISK BLOCK"])
            st.markdown(f'<div class="metric-box" style="border-left-color: #e74c3c;"><div class="metric-title">⛔ AI PREDICTIVE BLOCKS</div><div class="metric-value">{risk_block_count} Cards</div></div>', unsafe_allow_html=True)
        with m3:
            growth_count = len(df[df['Autonomous_Action'] == "🌟 GROWTH"])
            st.markdown(f'<div class="metric-box" style="border-left-color: #2ecc71;"><div class="metric-title">💎 UPGRADE LEADS</div><div class="metric-value">{growth_count} Accounts</div></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-box" style="border-left-color: #3498DB;"><div class="metric-title">📊 PORTFOLIO DEFAULT RISK</div><div class="metric-value">{df["DEFAULT_PROBABILITY"].mean():.1%}</div></div>', unsafe_allow_html=True)

        st.write("")

        # Row 2: Distribution Chart & Policy Breakdown
        c1, c2 = st.columns([3, 2])
        
        with c1:
            st.subheader("Autonomous Distribution")
            fig, ax = plt.subplots(figsize=(6, 4))
            labels = counts.index
            explode = [0.08 if 'BLOCK' in l or 'NUDGE' in l else 0.02 for l in labels]
            
            color_map = {
                '✅ STABLE': '#2ECC71', '📩 NUDGE': '#3498DB', 
                '🌟 GROWTH': '#F1C40F', '⛔ AI RISK BLOCK': '#E74C3C', 
                '🛡️ SECURITY BLOCK': '#95A5A6'
            }
            colors = [color_map.get(label, '#bdc3c7') for label in labels]

            ax.pie(counts, labels=labels, autopct='%1.1f%%', shadow=False, 
                   startangle=140, explode=explode, colors=colors,
                   textprops={'fontsize': 9})
            ax.axis('equal')
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
        
        with c2:
            st.subheader("Active AI Policy Engine Guide")
            st.error(f"**⛔ AI RISK BLOCK:** ML Model calculated risk probability is higher than **{ml_threshold:.0%}**.")
            st.info("**🛡️ SECURITY BLOCK:** Fraud protection triggered due to sudden 5x spending spikes.")
            st.warning("**📩 NUDGE Target:** Safe history, but account card utilization is high (>80%).")
            st.success("**🌟 GROWTH Target:** Safe history with clear open spending capacity (<25% used).")
            
            st.write("---")
            st.write("**Operational Counter:**")
            for action, count in counts.items():
                st.write(f"• **{action}**: {count} users calculated")

        # Row 3: Actionable Customer List Data Table
        st.write("---")
        st.subheader("Actionable Customer Registry")
        # Included the clean AI probability column inside the UI table view
        display_cols = ['ID', 'UTIL_RATE', 'PAY_0', 'DEFAULT_PROBABILITY', 'Autonomous_Action']
        st.dataframe(df[display_cols].sort_values(by='DEFAULT_PROBABILITY', ascending=False).head(100), use_container_width=True)

        # File Export System
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Compiled Risk Report (CSV)", csv, "ml_risk_report.csv", "text/csv")
        
    else:
        st.error("⚠️ Data Error: Uploaded file missing required target/features.")
        st.info(f"Columns processed: {list(df.columns)}")
