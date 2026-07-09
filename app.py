import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="CreditPulse-AI", layout="wide")

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

# --- 1. DATA INTAKE (Safe Loading) ---
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
        # Fallback Mock Data for demo
        np.random.seed(42)  # Fixed seed so chart results remain predictable
        data_size = 500
        return pd.DataFrame({
            'ID': range(1, data_size + 1),
            'LIMIT_BAL': np.random.choice([10000, 20000, 50000, 100000], data_size),
            'PAY_0': np.random.randint(-1, 5, data_size),
            'BILL_AMT1': np.random.uniform(500, 45000, data_size),
            'BILL_AMT2': np.random.uniform(500, 15000, data_size),
            'PAY_AMT1': np.random.uniform(0, 5000, data_size),
            'default payment next month': np.random.randint(0, 2, data_size)
        })

# --- 2. SIDEBAR CONTROLS ---
st.sidebar.header("📁 Data Intake")
user_file = st.sidebar.file_uploader("Upload Credit CSV/Excel", type=["csv", "xls", "xlsx"])
df = get_data(user_file)

st.sidebar.header("🛠️ Policy Engine")
risk_t = st.sidebar.slider("Risk Threshold (Delinquency)", 1, 4, 2, help="Trigger block if customer is behind by this many months")
util_l = st.sidebar.slider("Nudge Limit (Util %)", 0.5, 1.0, 0.85, help="Trigger warning text if card is maxed past this %")
growth_l = st.sidebar.slider("Growth Limit (Util %)", 0.1, 0.5, 0.3, help="Target for offer upgrades if usage is under this %")

# --- 3. THE BRAIN & AUDITOR ---
if df is not None:
    required = ['BILL_AMT1', 'LIMIT_BAL', 'PAY_0']
    if all(col in df.columns for col in required):
        
        # Math Formula 1: Safely calculate percentage of credit limit used (+1 avoids division by zero)
        df['UTIL_RATE'] = df['BILL_AMT1'] / (df['LIMIT_BAL'] + 1)
        
        # Math Formula 2: Safely calculate sudden spending spikes (Handles missing historical billing columns)
        if 'BILL_AMT2' in df.columns:
            df['SPENDING_JUMP'] = df['BILL_AMT1'] / (df['BILL_AMT2'] + 1)
        else:
            df['SPENDING_JUMP'] = 1.0  # Default safe fall-back value if previous bill is missing

        # Automated Business Logic Selector (The Bucketing Engine)
        def auditor(row):
            if row['PAY_0'] >= risk_t: return "⛔ CRITICAL BLOCK"
            if row['SPENDING_JUMP'] >= 5: return "🛡️ SECURITY BLOCK"
            if row['UTIL_RATE'] > util_l: return "📩 NUDGE"
            if row['PAY_0'] <= 0 and row['UTIL_RATE'] < growth_l: return "🌟 GROWTH"
            return "✅ STABLE"

        df['Autonomous_Action'] = df.apply(auditor, axis=1)
        counts = df['Autonomous_Action'].value_counts()

        # --- 4. DYNAMIC HEALTH RATING LOGIC ---
        total = len(df)
        block_pct = (len(df[df['Autonomous_Action'].str.contains('BLOCK')]) / total) * 100
        growth_pct = (len(df[df['Autonomous_Action'] == "🌟 GROWTH"]) / total) * 100

        if block_pct > 20:
            status = "BAD (High Risk Portfolio)"
            color = "red"
        elif block_pct > 10:
            status = "GOOD (Manageable Portfolio)"
            color = "orange"
        elif growth_pct > 30:
            status = "EXCELLENT (High Opportunity Portfolio)"
            color = "blue"
        else:
            status = "VERY GOOD (Stable Portfolio)"
            color = "green"

        # --- 5. THE DASHBOARD ---
        st.title("🚀 CreditPulse Autonomous Risk System")
        st.caption("Automated portfolio auditor & card control switcher")
        
        # HEALTH STATUS HEADER
        st.markdown(f"### Current Portfolio Rating: :{color}[{status}]")
        st.write("---")
        
        # Modern Look Executive Summary Metrics Block
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-box" style="border-left-color: #7f8c8d;"><div class="metric-title">📋 TOTAL PORTFOLIO</div><div class="metric-value">{total} Accounts</div></div>', unsafe_allow_html=True)
        with m2:
            critical_count = len(df[df['Autonomous_Action'].str.contains('BLOCK')])
            st.markdown(f'<div class="metric-box" style="border-left-color: #e74c3c;"><div class="metric-title">🚨 TOTAL CARDS BLOCKED</div><div class="metric-value">{critical_count} Cards</div></div>', unsafe_allow_html=True)
        with m3:
            growth_count = len(df[df['Autonomous_Action'] == "🌟 GROWTH"])
            st.markdown(f'<div class="metric-box" style="border-left-color: #f1c40f;"><div class="metric-title">💎 UPGRADE LEADS</div><div class="metric-value">{growth_count} Accounts</div></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-box" style="border-left-color: #3498DB;"><div class="metric-title">📊 AVG CREDIT UTILIZATION</div><div class="metric-value">{df["UTIL_RATE"].mean():.1%}</div></div>', unsafe_allow_html=True)

        st.write("")

        # Row 2: Distribution Chart & Policy Breakdown
        c1, c2 = st.columns([3, 2])
        
        with c1:
            st.subheader("Autonomous Distribution")
            
            # Clean object-oriented Matplotlib configuration to stop server-side cross-talk
            fig, ax = plt.subplots(figsize=(6, 4))
            labels = counts.index
            explode = [0.08 if 'BLOCK' in l or 'NUDGE' in l else 0.02 for l in labels]
            
            color_map = {
                '✅ STABLE': '#2ECC71', '📩 NUDGE': '#3498DB', 
                '🌟 GROWTH': '#F1C40F', '⛔ CRITICAL BLOCK': '#E74C3C', 
                '🛡️ SECURITY BLOCK': '#95A5A6'
            }
            colors = [color_map.get(label, '#bdc3c7') for label in labels]

            ax.pie(counts, labels=labels, autopct='%1.1f%%', shadow=False, 
                   startangle=140, explode=explode, colors=colors,
                   textprops={'fontsize': 9})
            ax.axis('equal')
            
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig) # Sanitizes runtime memory
        
        with c2:
            st.subheader("Active Rule Guide")
            st.info(f"**🌟 GROWTH Target:** No late payments & uses less than {growth_l*100:.0f}% of card limit.")
            st.warning(f"**📩 NUDGE Target:** Good history but using more than {util_l*100:.0f}% of card limit.")
            st.error(f"**⛔ BLOCK Target:** Customer has failed to make payments for {risk_t} or more months.")
            
            st.write("---")
            st.write("**Operational Counter:**")
            for action, count in counts.items():
                st.write(f"• **{action}**: {count} users calculated")

        # Row 3: Actionable Customer List Data Table
        st.write("---")
        st.subheader("Actionable Customer Registry")
        st.dataframe(df[['ID', 'UTIL_RATE', 'PAY_0', 'Autonomous_Action']].head(100), use_container_width=True)

        # File Export System
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Compiled Risk Report (CSV)", csv, "risk_report.csv", "text/csv")
        
    else:
        st.error("⚠️ Data Error: Missing required columns (BILL_AMT1, LIMIT_BAL, PAY_0).")
        st.info(f"Columns processed: {list(df.columns)}")
