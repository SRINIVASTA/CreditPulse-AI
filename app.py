import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="CreditPulse-AI", layout="wide")

# --- DATA INTAKE (Dual Mode) ---
@st.cache_data
def get_data(uploaded_file=None):
    if uploaded_file is not None:
        try:
            # Detect file type
            if uploaded_file.name.endswith('.csv'):
                return pd.read_csv(uploaded_file)
            else:
                return pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return None
    else:
        # AUTOMATIC SAMPLE DATA (Matches UCI Column Names)
        # In GitHub, you can replace this with: pd.read_csv("default_credit_data.csv")
        np.random.seed(42)
        data_size = 1000
        return pd.DataFrame({
            'ID': range(1, data_size + 1),
            'LIMIT_BAL': np.random.choice([10000, 50000, 100000, 200000], data_size),
            'PAY_0': np.random.randint(-1, 5, data_size),
            'BILL_AMT1': np.random.uniform(500, 20000, data_size),
            'BILL_AMT2': np.random.uniform(500, 20000, data_size),
            'PAY_AMT1': np.random.uniform(0, 5000, data_size),
            'default payment next month': np.random.randint(0, 2, data_size)
        })

# Sidebar - File Upload
st.sidebar.header("📁 Data Intake")
user_file = st.sidebar.file_uploader("Upload Credit CSV/Excel", type=["csv", "xls", "xlsx"])
df = get_data(user_file)

# Sidebar - Policy Controls
st.sidebar.header("🛠️ Policy Engine")
risk_t = st.sidebar.slider("Risk Threshold (Delinquency)", 1, 4, 2)
util_l = st.sidebar.slider("Nudge Limit (Util %)", 0.5, 1.0, 0.85)

# --- CORE LOGIC ---
if df is not None:
    # Ensure correct column names for UCI or Sample
    target = 'default payment next month' if 'default payment next month' in df.columns else 'default'
    
    # Brain (Quick ML Prediction)
    df['UTIL_RATE'] = df['BILL_AMT1'] / (df['LIMIT_BAL'] + 1)
    df['SPENDING_JUMP'] = df['BILL_AMT1'] / (df['BILL_AMT2'] + 1)
    
    # Auditor (Decision Engine)
    def auditor(row):
        if row['PAY_0'] >= risk_t: return "⛔ CRITICAL BLOCK"
        if row['SPENDING_JUMP'] >= 5: return "🛡️ SECURITY BLOCK"
        if row['UTIL_RATE'] > util_l: return "📩 NUDGE"
        if row['PAY_0'] <= 0 and row['UTIL_RATE'] < 0.3: return "🌟 GROWTH"
        return "✅ STABLE"

    df['Autonomous_Action'] = df.apply(auditor, axis=1)

    # --- UI RENDERING ---
    st.title("🚀 CreditPulse Autonomous System")
    
    # High-level Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Portfolio Size", f"{len(df)} Accounts")
    m2.metric("Loss Prevention", f"{len(df[df['Autonomous_Action'].str.contains('BLOCK')]):,}")
    m3.metric("Growth Leads", len(df[df['Autonomous_Action'] == "🌟 GROWTH"]))

    # Visuals
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Automated Action Distribution")
        counts = df['Autonomous_Action'].value_counts()
        st.bar_chart(counts)
    with c2:
        st.subheader("Policy Rulebook")
        st.write(f"- **Block:** Delay ≥ {risk_t} months")
        st.write(f"- **Nudge:** Utilization > {util_l*100:.0f}%")
        st.write("- **Growth:** No delay & Low usage")

    st.subheader("Actionable Customer Insights")
    st.dataframe(df[['ID', 'UTIL_RATE', 'PAY_0', 'Autonomous_Action']].head(50), use_container_width=True)
