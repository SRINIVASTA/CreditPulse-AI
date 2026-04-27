import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="CreditPulse-AI", layout="wide")

# --- 1. DATA INTAKE (Safe Loading) ---
@st.cache_data
def get_data(uploaded_file=None):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                return pd.read_csv(uploaded_file)
            else:
                # header=1 handles the specific UCI Excel format
                return pd.read_excel(uploaded_file, header=1)
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return None
    else:
        # Fallback Mock Data for immediate demo
        data_size = 500
        return pd.DataFrame({
            'ID': range(1, data_size + 1),
            'LIMIT_BAL': np.random.choice([5000, 10000, 20000, 50000], data_size),
            'PAY_0': np.random.randint(-1, 4, data_size),
            'BILL_AMT1': np.random.uniform(500, 15000, data_size),
            'BILL_AMT2': np.random.uniform(500, 15000, data_size),
            'PAY_AMT1': np.random.uniform(0, 5000, data_size),
            'default payment next month': np.random.randint(0, 2, data_size)
        })

# --- 2. SIDEBAR CONTROLS ---
st.sidebar.header("📁 Data Intake")
user_file = st.sidebar.file_uploader("Upload Credit CSV/Excel", type=["csv", "xls", "xlsx"])
df = get_data(user_file)

st.sidebar.header("🛠️ Policy Engine")
risk_t = st.sidebar.slider("Risk Threshold (Delinquency)", 1, 4, 2)
util_l = st.sidebar.slider("Nudge Limit (Util %)", 0.5, 1.0, 0.85)
growth_l = st.sidebar.slider("Growth Limit (Util %)", 0.1, 0.5, 0.3)

# --- 3. THE BRAIN & AUDITOR ---
if df is not None:
    # Ensure Column Names exist
    required = ['BILL_AMT1', 'LIMIT_BAL', 'PAY_0']
    if all(col in df.columns for col in required):
        
        # Calculations
        df['UTIL_RATE'] = df['BILL_AMT1'] / (df['LIMIT_BAL'] + 1)
        b2_col = 'BILL_AMT2' if 'BILL_AMT2' in df.columns else 'BILL_AMT1'
        df['SPENDING_JUMP'] = df['BILL_AMT1'] / (df[b2_col] + 1)
        
        # Decision Engine
        def auditor(row):
            if row['PAY_0'] >= risk_t: return "⛔ CRITICAL BLOCK"
            if row['SPENDING_JUMP'] >= 5: return "🛡️ SECURITY BLOCK"
            if row['UTIL_RATE'] > util_l: return "📩 NUDGE"
            if row['PAY_0'] <= 0 and row['UTIL_RATE'] < growth_l: return "🌟 GROWTH"
            return "✅ STABLE"

        df['Autonomous_Action'] = df.apply(auditor, axis=1)

        # --- 4. THE DASHBOARD ---
        st.title("🚀 CreditPulse Autonomous Risk System")
        
        # Row 1: Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Portfolio Size", len(df))
        m2.metric("Blocking Actions", len(df[df['Autonomous_Action'].str.contains('BLOCK')]))
        m3.metric("Growth Leads", len(df[df['Autonomous_Action'] == "🌟 GROWTH"]))
        m4.metric("Avg Util Rate", f"{df['UTIL_RATE'].mean():.1%}")

        st.divider()

        # Row 2: 3D Visualization & Policy
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.subheader("Autonomous Portfolio Health (3D View)")
            counts = df['Autonomous_Action'].value_counts()
            
            fig, ax = plt.subplots(figsize=(8, 5))
            labels = counts.index
            explode = [0.1 if 'BLOCK' in l or 'NUDGE' in l else 0.05 for l in labels]
            
            # Using specific colors for impact
            color_map = {
                '✅ STABLE': '#2ECC71', '📩 NUDGE': '#3498DB', 
                '🌟 GROWTH': '#F1C40F', '⛔ CRITICAL BLOCK': '#E74C3C', 
                '🛡️ SECURITY BLOCK': '#95A5A6'
            }
            colors = [color_map.get(label, '#bdc3c7') for label in labels]

            ax.pie(counts, labels=labels, autopct='%1.1f%%', shadow=True, 
                   startangle=140, explode=explode, colors=colors)
            ax.axis('equal')
            st.pyplot(fig)
        
        with c2:
            st.subheader("Policy Rules")
            st.info(f"**Growth:** Pay_0 <= 0 & Util < {growth_l*100:.0f}%")
            st.warning(f"**Nudge:** Util > {util_l*100:.0f}%")
            st.error(f"**Block:** Delay >= {risk_t} months")
            
            st.write("---")
            st.write("**Quick Audit:**")
            for action, count in counts.items():
                st.write(f"{action}: {count}")

        # Row 3: Data Table
        st.subheader("Actionable Customer List")
        st.dataframe(df[['ID', 'UTIL_RATE', 'PAY_0', 'Autonomous_Action']].head(100), use_container_width=True)

        # Download Report
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Risk Report", csv, "risk_report.csv", "text/csv")
        
    else:
        st.error("⚠️ Data Error: Required columns (BILL_AMT1, LIMIT_BAL, PAY_0) not found.")
        st.info(f"Columns detected: {list(df.columns)}")
