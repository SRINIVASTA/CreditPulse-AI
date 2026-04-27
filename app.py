import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Page Config
st.set_page_config(page_title="Autonomous Credit System", layout="wide")

# --- DATA GENERATION / LOADING ---
@st.cache_data
def load_data():
    # Simulating the Excel data structure
    data_size = 5000
    df = pd.DataFrame({
        'ID': range(1, data_size + 1),
        'LIMIT_BAL': np.random.choice([5000, 10000, 20000, 50000], data_size),
        'PAY_0': np.random.randint(-1, 5, data_size),
        'BILL_AMT1': np.random.uniform(1000, 40000, data_size),
        'BILL_AMT2': np.random.uniform(1000, 40000, data_size),
        'PAY_AMT1': np.random.uniform(0, 5000, data_size),
        'default': np.random.randint(0, 2, data_size)
    })
    return df

df = load_data()

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🛠️ Policy Configuration")
risk_threshold = st.sidebar.slider("Risk Threshold (Months Delay)", 1, 4, 2)
util_limit = st.sidebar.slider("Nudge Limit (Utilization %)", 0.5, 1.0, 0.85)
reward_util = st.sidebar.slider("Growth Limit (Utilization %)", 0.1, 0.5, 0.3)

# --- LOGIC ENGINE ---
def process_data(data, risk_t, util_l, reward_l):
    temp_df = data.copy()
    # Math logic
    temp_df['UTIL_RATE'] = temp_df['BILL_AMT1'] / (temp_df['LIMIT_BAL'] + 1)
    temp_df['SPENDING_JUMP'] = temp_df['BILL_AMT1'] / (temp_df['BILL_AMT2'] + 1)
    
    def engine(row):
        if row['PAY_0'] >= risk_t: return "⛔ CRITICAL BLOCK"
        if row['SPENDING_JUMP'] >= 5: return "🛡️ SECURITY BLOCK"
        if row['UTIL_RATE'] > util_l: return "📩 NUDGE"
        if row['PAY_0'] <= 0 and row['UTIL_RATE'] < reward_l: return "🌟 GROWTH"
        return "✅ STABLE"

    temp_df['Autonomous_Action'] = temp_df.apply(engine, axis=1)
    return temp_df

processed_df = process_data(df, risk_threshold, util_limit, reward_util)

# --- DASHBOARD LAYOUT ---
st.title("🚀 Autonomous Credit Risk System")
st.markdown("### Real-time Portfolio Logic & Action Engine")

col1, col2, col3 = st.columns(3)
with col1:
    total_val = processed_df['BILL_AMT1'].sum()
    st.metric("Total Portfolio Volume", f"${total_val:,.0f}")
with col2:
    blocked = processed_df[processed_df['Autonomous_Action'].str.contains("BLOCK")]
    st.metric("Quarantined Volume", f"${blocked['BILL_AMT1'].sum():,.0f}", delta_color="inverse")
with col3:
    growth = processed_df[processed_df['Autonomous_Action'] == "🌟 GROWTH"]
    st.metric("Upsell Potential", f"${growth['BILL_AMT1'].sum():,.0f}")

# --- VISUALS ---
st.divider()
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Portfolio Distribution")
    counts = processed_df['Autonomous_Action'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = {'✅ STABLE': '#2ECC71', '📩 NUDGE': '#3498DB', '🌟 GROWTH': '#FFD700', '⛔ CRITICAL BLOCK': '#E74C3C', '🛡️ SECURITY BLOCK': '#95A5A6'}
    current_colors = [colors.get(x, '#333') for x in counts.index]
    
    counts.plot(kind='bar', color=current_colors, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with c2:
    st.subheader("Policy Rulebook")
    st.info(f"**Growth:** Pay_0 <= 0 & Util < {reward_util*100:.0f}%")
    st.warning(f"**Nudge:** Util > {util_limit*100:.0f}%")
    st.error(f"**Block:** Delay >= {risk_threshold} months")

# --- DATA TABLE ---
st.subheader("Actionable Customer List")
st.dataframe(processed_df[['ID', 'UTIL_RATE', 'PAY_0', 'Autonomous_Action']].head(100), use_container_width=True)

# CSV Download
csv = processed_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Action Report", data=csv, file_name="credit_actions.csv", mime="text/csv")
