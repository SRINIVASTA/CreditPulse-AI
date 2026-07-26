import time
import streamlit as st
from streamlit.web.server.websocket_headers import _get_websocket_headers

# Force Streamlit to completely hide the header bar, deployment buttons, and GitHub icons
st.markdown("""
    <style>
    header[data-testid="stHeader"] {
        visibility: hidden !important;
        display: none !important;
    }
    div[data-testid="stToolbar"] {
        visibility: hidden !important;
        display: none !important;
    }
    footer {
        visibility: hidden !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ========================================================================= 
# 🏷️ COPYRIGHT NOTICE 
# ========================================================================= 
st.sidebar.markdown(
    "<div style='text-align: center; color: #888888; font-size: 12px; margin-bottom: 20px;'>"
    "© 2026 CreditPulse-AI. All Rights Reserved by Srinivasta."
    "</div>", 
    unsafe_allow_html=True
)

# ========================================================================= 
# 🤖 AUTOMATION BYPASS DETECTION
# ========================================================================= 
is_automation_runner = False
try:
    headers = _get_websocket_headers()
    user_agent = headers.get("User-Agent", "")
    if "Chrome/120.0.0.0 Safari/537.36" in user_agent:
        is_automation_runner = True
except Exception:
    pass

# ========================================================================= 
# 🔑 INPUT CONFIGURATION FOR USER VS DEVELOPER
# ========================================================================= 
st.sidebar.title("🔒 Software Security Portal") 

if is_automation_runner:
    license_input = "DEV-ADMIN-99"  
    st.sidebar.text_input("Enter License Key:", value="••••••••••••", type="password", disabled=True)
else:
    license_input = st.sidebar.text_input("Enter License Key:", type="password") 

is_developer = (license_input == "DEV-ADMIN-99")

# ========================================================================= 
# 🧠 BROWSER-LEVEL TEST KEY LOCK (Keeps portal open for paid keys!)
# ========================================================================= 
# Hidden JavaScript to check if ONLY the test key is expired on this browser
if license_input == "TEST-KEY-1234":
    check_blacklist_js = """
    <script>
        const isTestExpired = localStorage.getItem("creditpulse_test_expired");
        if (isTestExpired === "true") {
            window.parent.document.body.innerHTML = `
                <div style="font-family:sans-serif; text-align:center; margin-top:100px; padding:20px;">
                    <h1 style="color:#E74C3C;">🔒 Sandbox Access Permanently Locked</h1>
                    <p style="font-size:18px; color:#555;">Your single-use 10-minute trial allocation for <b>TEST-KEY-1234</b> has fully elapsed.</p>
                    <p style="font-size:16px; color:#27AE60; font-weight:bold;">To unlock unlimited access, please refresh this browser page and enter your purchased Premium License Key!</p>
                    <p style="font-size:14px; color:#888; margin-top:30px;">Contact me on LinkedIn to upgrade your evaluation license.</p>
                </div>
            `;
        }
    </script>
    """
    st.components.v1.html(check_blacklist_js, height=0, width=0)

# Initialize runtime trial tracking clock
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "session_expired" not in st.session_state:
    st.session_state.session_expired = False

# ========================================================================= 
# 🔓 ACCESS VALIDATION MATRIX (Includes your new Premium Paid Keys!)
# ========================================================================= 
def verify_global_access(user_key):
    GLOBAL_MASTER_KEY = "TEST-KEY-1234"
    DEVELOPER_KEY = "DEV-ADMIN-99"
    
    # 🌟 YOU CAN ADD YOUR PAID CLIENT KEYS HERE:
    PAID_PREMIUM_KEYS = ["PREMIUM-KEY-8888", "CLIENT-ACCESS-XYZ"]
    
    if user_key == DEVELOPER_KEY:
        if is_automation_runner:
            return "System Health Ping Active"
        return "Developer Admin Mode (Unlimited)"
        
    elif user_key in PAID_PREMIUM_KEYS:
        return "Enterprise License Active (Unlimited Access) 👑"
        
    elif user_key == GLOBAL_MASTER_KEY:
        return "Global Sandbox Session (10 Min)"
        
    else:
        st.error("🚨 ACCESS DENIED: Invalid or Unpaid Software License Key.")
        st.stop()

if not license_input: 
    st.title("CreditPulse Autonomous ML Risk System") 
    st.warning("🔐 This system is protected by copyright. Enter a license key in the sidebar to run.") 
    st.stop() 

session_profile = verify_global_access(license_input)
st.sidebar.success(f"Status: {session_profile}") 

# Check if the session profile contains the word "Enterprise" to skip the timer
is_paid_user = "Enterprise" in session_profile

# ========================================================================= 
# ⏱️ 10-MINUTE TIMEOUT SYSTEM (Only runs for the free Test Key!)
# ========================================================================= 
if not is_developer and not is_paid_user:
    SESSION_LIMIT_SECONDS = 600  
    elapsed_time = time.time() - st.session_state.start_time

    if elapsed_time > SESSION_LIMIT_SECONDS or st.session_state.session_expired:
        st.session_state.session_expired = True
        
        # Lockout ONLY the test key marker inside browser storage
        trigger_lockout_js = """
        <script>
            localStorage.setItem("creditpulse_test_expired", "true");
            window.location.reload();
        </script>
        """
        st.components.v1.html(trigger_lockout_js, height=0, width=0)
        st.stop() 

    time_left_seconds = int(SESSION_LIMIT_SECONDS - elapsed_time)
    mins, secs = divmod(time_left_seconds, 60)
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### ⏳ Sandbox Timer:\n## `{mins:02d}:{secs:02d}`")
elif is_paid_user:
    st.sidebar.markdown("---")
    st.sidebar.info("👑 Unlimited Enterprise License Active. Enjoy the system!")
else:
    st.sidebar.markdown("---")
    if is_automation_runner:
        st.sidebar.warning("🤖 Core Engine Keep-Alive Loop Processing...")
        st.title("System Diagnostic Overview")
        st.write("Server connection verified successfully.")
    else:
        st.sidebar.info("⚡ Uncapped Developer Session Active. Timeout disabled.")

# ========================================================================= 
# 📊 CORE APP DATA ANALYSIS CONTINUES SAFELY BELOW
# ========================================================================= 

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc, accuracy_score

# ReportLab Layout Component Imports
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, whitesmoke, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# --- STREAMLIT PAGE CONFIGURATION ---
st.set_page_config(page_title="CreditPulse-AI (ML Engine)", layout="wide")

# --- CUSTOM CSS FOR HIGH-UTILITY EXECUTIVE METRICS ---
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

# --- DATA INTAKE & AUTOMATIC ML TRAINING ---
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
        np.random.seed(42)
        data_size = 1000  
        
        limit_bal = np.random.choice([10000, 20000, 50000, 100000], data_size)
        pay_0 = np.random.choice([-1, 0, 1, 2, 3], data_size, p=[0.3, 0.4, 0.15, 0.1, 0.05])
        bill_amt1 = np.random.uniform(500, 45000, data_size)
        bill_amt2 = bill_amt1 * np.random.uniform(0.5, 1.2, data_size)
        pay_amt1 = np.random.uniform(0, 5000, data_size)
        
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
    features = ['LIMIT_BAL', 'PAY_0', 'BILL_AMT1', 'BILL_AMT2', 'PAY_AMT1']
    target = 'default payment next month'
    X = data[features]
    y = data[target]
    
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=6)
    model.fit(X, y)
    return model

# --- REPORTLAB SINGLE STATEMENT GENERATION ENGINE ---
def generate_client_pdf(client_row, curr_symbol):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=HexColor('#2C3E50'), spaceAfter=4)
    subtitle_style = ParagraphStyle('DocSubtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=HexColor('#7F8C8D'), spaceAfter=18)
    section_heading = ParagraphStyle('SecHeading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=HexColor('#2C3E50'), spaceBefore=10, spaceAfter=6)
    cell_text = ParagraphStyle('CellText', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=HexColor('#34495E'))
    cell_text_bold = ParagraphStyle('CellTextBold', parent=cell_text, fontName='Helvetica-Bold')
    header_text_style = ParagraphStyle('HeaderText', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=13, textColor=whitesmoke)

    story.append(Paragraph("CreditPulse-AI Risk Statement", title_style))
    story.append(Paragraph("Automated Credit Risk Management Documentation", subtitle_style))
    story.append(Spacer(1, 5))
    
    story.append(Paragraph("Account Overview & Actions", section_heading))
    action_color = "#E74C3C" if "BLOCK" in str(client_row['Autonomous_Action']) else "#2ECC71"
    
    summary_data = [
        [Paragraph("Client Identification ID:", cell_text_bold), Paragraph(str(int(client_row['ID'])), cell_text)],
        [Paragraph("Autonomous Decision Strategy:", cell_text_bold), Paragraph(f"<font color='{action_color}'><b>{client_row['Autonomous_Action']}</b></font>", cell_text)],
        [Paragraph("AI Predictive Default Risk:", cell_text_bold), Paragraph(f"<b>{client_row['DEFAULT_PROBABILITY']:.2%}</b>", cell_text)]
    ]
    
    summary_table = Table(summary_data, colWidths=[200, 340])
    summary_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), HexColor('#F8F9FA')), ('PADDING', (0, 0), (-1, -1), 6), ('LINEBELOW', (0, 0), (-1, -1), 0.5, HexColor('#E2E8F0')), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    story.append(summary_table)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("Financial Exposure Metrics Ledger", section_heading))
    
    # Use clean standard labels for PDF safety across symbols
    pdf_curr = "Rs." if curr_symbol == "₹" else "$"
    
    ledger_data = [
        [Paragraph("Metric Feature Description", header_text_style), Paragraph("Calculated Statement Value", header_text_style)],
        [Paragraph("Total Allocated Credit Limit (LIMIT_BAL)", cell_text), Paragraph(f"{pdf_curr} {client_row['LIMIT_BAL']:,.2f}", cell_text)],
        [Paragraph("Current Statement Balance (BILL_AMT1)", cell_text), Paragraph(f"{pdf_curr} {client_row['BILL_AMT1']:,.2f}", cell_text)],
        [Paragraph("Calculated Credit Card Utilization (UTIL_RATE)", cell_text), Paragraph(f"{client_row['UTIL_RATE']:.1%}", cell_text)],
        [Paragraph("Payment Delay Status Matrix (PAY_0)", cell_text), Paragraph(f"{int(client_row['PAY_0'])} Months Overdue", cell_text)],
        [Paragraph("Prior Billing Statement Total (BILL_AMT2)", cell_text), Paragraph(f"{pdf_curr} {client_row['BILL_AMT2']:,.2f}", cell_text)],
        [Paragraph("Calculated Velocity Shift (SPENDING_JUMP)", cell_text), Paragraph(f"{client_row['SPENDING_JUMP']:.2f}x Scale Jump", cell_text)],
        [Paragraph("Most Recent Remittance Total (PAY_AMT1)", cell_text), Paragraph(f"{pdf_curr} {client_row['PAY_AMT1']:,.2f}", cell_text)]
    ]
    
    ledger_table = Table(ledger_data, colWidths=[300, 240])
    ledger_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), HexColor('#1F77B4')), ('PADDING', (0, 0), (-1, -1), 8), ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#CBD5E1')), ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#F8F9FA')]), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    story.append(ledger_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer
# --- STREAMLIT UI SIDEBAR CONTROLS ---
st.sidebar.header("📁 Data Intake")
user_file = st.sidebar.file_uploader("Upload Credit CSV/Excel", type=["csv", "xls", "xlsx"])
df = get_data(user_file)

st.sidebar.header("⚙️ Localization Engine")
# Added interactive core toggle switch layout element
currency_mode = st.sidebar.selectbox("Select Operational Currency:", ["INR (₹)", "USD ($)"])
currency_symbol = "₹" if "INR" in currency_mode else "$"

st.sidebar.header("🤖 ML Control Panel")
ml_threshold = st.sidebar.slider("Risk Decision Cut-off", 0.1, 0.9, 0.50)

# --- MAIN APP LAYOUT CONTROLLER ---
if df is not None:
    required = ['LIMIT_BAL', 'PAY_0', 'BILL_AMT1', 'BILL_AMT2', 'PAY_AMT1', 'default payment next month']
    if all(col in df.columns for col in required):
        
        ml_model = train_ml_model(df)
        
        # Safe Mathematical Transformations
        df['UTIL_RATE'] = df['BILL_AMT1'] / np.clip(df['LIMIT_BAL'], 1, None)
        df['SPENDING_JUMP'] = np.where(df['BILL_AMT2'] > 0, df['BILL_AMT1'] / df['BILL_AMT2'], 1.0)
        
        # Inference Generation
        features_list = ['LIMIT_BAL', 'PAY_0', 'BILL_AMT1', 'BILL_AMT2', 'PAY_AMT1']
        df['DEFAULT_PROBABILITY'] = ml_model.predict_proba(df[features_list])[:, 1]

        # Strategic Priority Waterfall Rules Engine
        def ai_auditor(row):
            if row['DEFAULT_PROBABILITY'] >= ml_threshold: return "⛔ AI RISK BLOCK"
            if row['SPENDING_JUMP'] >= 5: return "🛡️ SECURITY BLOCK"
            if row['PAY_0'] <= 0 and row['UTIL_RATE'] > 0.80: return "📩 NUDGE"
            if row['PAY_0'] <= 0 and row['UTIL_RATE'] < 0.25: return "🌟 GROWTH"
            return "✅ STABLE"

        df['Autonomous_Action'] = df.apply(ai_auditor, axis=1)
        counts = df['Autonomous_Action'].value_counts()

        # Dynamic Status Evaluation Block
        total = len(df)
        block_pct = (len(df[df['Autonomous_Action'] == '⛔ AI RISK BLOCK']) / total) * 100
        growth_pct = (len(df[df['Autonomous_Action'] == '🌟 GROWTH']) / total) * 100

        if block_pct > 25:
            status, color = "🚨 CRITICAL RISK", "red"
        elif block_pct > 12:
            status, color = "⚠️ CAUTION REQUIRED", "orange"
        elif growth_pct > 25:
            status, color = "🚀 EXPANSION ZONE", "blue"
        else:
            status, color = "🟢 HEALTHY PORTFOLIO", "green"

        st.title("🚀 CreditPulse Autonomous ML Risk System")
        st.caption("Predictive artificial intelligence portfolio auditor & card control switcher")
        st.markdown(f"### Current Portfolio Status: :{color}[{status}]")
        st.write("---")
        # =========================================================================
        # BLOCK 1: EXECUTIVE PERFORMANCE METRICS & ACTIVE POLICY ANALYSIS
        # =========================================================================
        with st.expander("📊 BLOCK 1: Executive Portfolio Metrics & Policy Breakdown", expanded=True):
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
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Autonomous Distribution")
                fig, ax = plt.subplots(figsize=(6, 4))
                labels = counts.index
                explode = [0.08 if 'BLOCK' in l or 'NUDGE' in l else 0.02 for l in labels]
                color_map = {'✅ STABLE': '#2ECC71', '📩 NUDGE': '#3498DB', '🌟 GROWTH': '#F1C40F', '⛔ AI RISK BLOCK': '#E74C3C', '🛡️ SECURITY BLOCK': '#95A5A6'}
                colors = [color_map.get(label, '#bdc3c7') for label in labels]
                ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140, explode=explode, colors=colors, textprops={'fontsize': 9})
                ax.axis('equal')
                st.pyplot(fig)
                plt.close(fig)
            with c2:
                st.subheader("Active AI Policy Engine Guide")
                st.error(f"**⛔ AI RISK BLOCK:** ML Model calculated risk probability is higher than **{ml_threshold:.0%}**.")
                st.info("**🛡️ SECURITY BLOCK:** Fraud protection triggered due to sudden 5x spending spikes.")
                st.warning("**📩 NUDGE Target:** Safe history, but account card utilization is high (>80%).")
                st.success("**🌟 GROWTH Target:** Safe history with clear open spending capacity (<25% used).")

        # =========================================================================
        # BLOCK 2: SYSTEM CUSTOMER REGISTRY & SINGLE STATEMENT DOCUMENT EXPORTS
        # =========================================================================
        with st.expander("📋 BLOCK 2: Actionable Customer Registry & Document Center", expanded=True):
            
            # Interactive Text Matching Entry Box
            search_query = st.text_input("🔍 Search Customer Registry by Client ID:", placeholder="Type Client ID number...")
            
            if search_query.strip():
                try:
                    filtered_df = df[df['ID'].astype(str).str.contains(search_query.strip())]
                except Exception:
                    filtered_df = df.copy()
            else:
                filtered_df = df.copy()
            
            # Formatted table rendering structure matching chosen currency sign configurations
            table_display = filtered_df.copy()
            table_display['LIMIT_BAL'] = table_display['LIMIT_BAL'].map(lambda x: f"{currency_symbol}{x:,.2f}")
            table_display['UTIL_RATE'] = table_display['UTIL_RATE'].map(lambda x: f"{x:.1%}")
            table_display['DEFAULT_PROBABILITY'] = table_display['DEFAULT_PROBABILITY'].map(lambda x: f"{x:.1%}")
            
            display_cols = ['ID', 'LIMIT_BAL', 'UTIL_RATE', 'PAY_0', 'DEFAULT_PROBABILITY', 'Autonomous_Action']
            st.dataframe(table_display[display_cols], use_container_width=True)
            
            # CSV Data Export Button
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Compiled Risk Report (CSV)", csv, "ml_risk_report.csv", "text/csv", use_container_width=True)
            
            st.write("---")
            st.subheader("🎯 Individual Client Report Compiler")
            
            selected_id = st.selectbox("Select Client ID to extract individual statement:", options=filtered_df['ID'].tolist())
            if selected_id:
                client_profile = filtered_df[filtered_df['ID'] == selected_id].iloc[0]
                pdf_data = generate_client_pdf(client_profile, currency_symbol)
                
                st.download_button(
                    label=f"🖨️ Download Official PDF Statement for Account #{int(selected_id)} ({currency_mode})", 
                    data=pdf_data, 
                    file_name=f"CreditPulse_Statement_ID_{int(selected_id)}.pdf", 
                    mime="application/pdf"
                )

        # =========================================================================
        # BLOCK 3: ML PERFORMANCE & EXPLAINABILITY GRAPHS
        # =========================================================================
        with st.expander("📊 BLOCK 3: AI Model Performance & Explainability Metrics", expanded=False):
            y_true = df['default payment next month']
            y_scores = df['DEFAULT_PROBABILITY']
            y_pred = (y_scores >= ml_threshold).astype(int)
            
            acc = accuracy_score(y_true, y_pred)
            fpr, tpr, _ = roc_curve(y_true, y_scores)
            roc_auc = auc(fpr, tpr)
            
            v1, v2, v3 = st.columns([1, 1.2, 1.2])
            with v1:
                st.markdown(f"**Current Model Accuracy:** `{acc:.1%}`")
                st.markdown(f"**Area Under ROC Curve (AUC):** `{roc_auc:.2f}`")
                st.info("💡 **How to read AUC:**\n• **0.90+** = Excellent Prediction\n• **0.70 - 0.89** = Good Portfolio Sorting\n• **0.50** = Random Guessing")
                
            with v2:
                st.markdown("**Receiver Operating Characteristic (ROC)**")
                fig_roc, ax_roc = plt.subplots(figsize=(5, 3.5))
                ax_roc.plot(fpr, tpr, color='#1f77b4', lw=2, label=f'ROC Curve (AUC = {roc_auc:.2f})')
                ax_roc.plot([0, 1], [0, 1], color='#7f8c8d', linestyle='--')
                ax_roc.set_xlim([0.0, 1.0])
                ax_roc.set_ylim([0.0, 1.05])
                ax_roc.set_xlabel('False Positive Rate', fontsize=8)
                ax_roc.set_ylabel('True Positive Rate', fontsize=8)
                ax_roc.legend(loc="lower right", fontsize=8)
                ax_roc.tick_params(axis='both', labelsize=8)
                fig_roc.tight_layout()
                st.pyplot(fig_roc)
                plt.close(fig_roc)

            with v3:
                st.markdown("**Feature Importance (Driver Weights)**")
                importances = ml_model.feature_importances_
                feat_imp_df = pd.DataFrame({'Feature': features_list, 'Importance': importances}).sort_values(by='Importance', ascending=True)
                fig_imp, ax_imp = plt.subplots(figsize=(5, 3.5))
                ax_imp.barh(feat_imp_df['Feature'], feat_imp_df['Importance'], color='#2ecc71')
                ax_imp.set_xlabel('Relative Structural Weight', fontsize=8)
                ax_imp.tick_params(axis='both', labelsize=8)
                fig_imp.tight_layout()
                st.pyplot(fig_imp)
                plt.close(fig_imp)
    else:
        st.error("⚠️ Data Error: Uploaded file missing required target/features.")
        st.info(f"Columns processed: {list(df.columns)}")
