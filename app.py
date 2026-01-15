import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import os

# --- 1. CONFIG & SYSTEM ARCHITECTURE ---
st.set_page_config(page_title="VitalStream Intelligence", page_icon="💠", layout="wide")

# Advanced CSS: Neumorphism & Glassmorphism Fusion
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&family=Plus+Jakarta+Sans:wght@300;400;700&display=swap');
    
    :root {
        --primary-glow: conic-gradient(from 180deg at 50% 50%, #16abff33 0deg, #0885ff33 55deg, #54d6ff33 120deg, #0071ff33 160deg, transparent 360deg);
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #050505;
    }

    /* KPI Glow Cards */
    .stMetric {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 20px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .stMetric:hover {
        border: 1px solid #0071ff;
        box-shadow: 0 0 20px rgba(0, 113, 255, 0.2);
        transform: scale(1.02);
    }

    /* Custom Data Table styling */
    .styled-table {
        border-radius: 15px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA INTELLIGENCE ENGINE ---
DATA_FILE = "health_data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df
    return pd.DataFrame(columns=["Date", "Coding Hours", "Water (L)", "Steps"])

def get_status_message(data):
    if data.empty: return "Awaiting Signal...", "Gray"
    latest = data.iloc[-1]
    score = 0
    if latest['Coding Hours'] >= 6: score += 1
    if latest['Water (L)'] >= 2: score += 1
    if latest['Steps'] >= 8000: score += 1
    
    if score == 3: return "SYSTEM OPTIMIZED", "#00FFC2"
    if score == 2: return "STABLE PERFORMANCE", "#0071ff"
    return "MAINTENANCE REQUIRED", "#FF4B4B"

data = load_data()

# --- 3. DYNAMIC SIDEBAR INTERFACE ---
with st.sidebar:
    st.markdown("<h2 style='letter-spacing: -1px;'>💠 VITAL-INTEL</h2>", unsafe_allow_html=True)
    st.caption("v2.1.0 Enterprise Edition")
    
    with st.expander("📥 Manual Data Entry", expanded=True):
        with st.form("entry_form", clear_on_submit=True):
            d = st.date_input("Timestamp", date.today())
            c = st.slider("Deep Work (h)", 0.0, 16.0, 6.0)
            w = st.slider("Hydration (L)", 0.0, 5.0, 2.5)
            s = st.number_input("Movement (Steps)", 0, 30000, 10000)
            if st.form_submit_button("COMMIT TO LEDGER"):
                new_row = pd.DataFrame([[d, c, w, s]], columns=data.columns)
                data = pd.concat([data, new_row], ignore_index=True)
                data.to_csv(DATA_FILE, index=False)
                st.toast("Block Synchronized", icon="🛰️")
                st.rerun()

    st.divider()
    # Data Export Tool
    if not data.empty:
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button("EXPORT SYSTEM DATA", data=csv, file_name="vital_intel_export.csv", mime="text/csv")

# --- 4. ANALYTICAL FRONTEND ---
status_msg, status_color = get_status_message(data)

header_col, status_col = st.columns([4, 1])
with header_col:
    st.title("System Intelligence Overview")
    st.caption("Real-time biometric and performance analysis engine.")

with status_col:
    st.markdown(f"<p style='color:{status_color}; font-weight:bold; font-family:JetBrains Mono; padding-top:20px;'>{status_msg}</p>", unsafe_allow_html=True)

if not data.empty:
    latest = data.iloc[-1]
    
    # 4.1 Real-time KPI Matrix
    st.markdown("### Biometric Node Status")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    # Calculate deltas (Difference from previous day)
    if len(data) > 1:
        c_delta = round(latest['Coding Hours'] - data.iloc[-2]['Coding Hours'], 1)
        w_delta = round(latest['Water (L)'] - data.iloc[-2]['Water (L)'], 1)
        s_delta = int(latest['Steps'] - data.iloc[-2]['Steps'])
    else:
        c_delta = w_delta = s_delta = 0

    kpi1.metric("DEEP WORK", f"{latest['Coding Hours']}h", f"{c_delta}h")
    kpi2.metric("HYDRATION", f"{latest['Water (L)']}L", f"{w_delta}L")
    kpi3.metric("MOVEMENT", f"{latest['Steps']:,}", f"{s_delta}")
    
    efficiency = int((latest['Steps'] / 10000) * 100) if latest['Steps'] > 0 else 0
    kpi4.metric("SYSTEM LOAD", f"{efficiency}%", "Dynamic")

    # 4.2 Interactive Analytics
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Multi-metric selection tool
    chart_view = st.multiselect("Select Analytical Layers", 
                               ['Coding Hours', 'Water (L)', 'Steps'], 
                               default=['Coding Hours', 'Water (L)'])
    
    tab_viz, tab_table = st.tabs(["Neural Mapping", "Log Ledger"])
    
    with tab_viz:
        st.area_chart(data.set_index("Date")[chart_view], use_container_width=True)
        
        # Anomaly Detection / Insights
        st.markdown("### System Insights")
        col_ins1, col_ins2 = st.columns(2)
        with col_ins1:
            if latest['Water (L)'] < 2:
                st.error("⚠️ Hydration Deficit Detected: Increase intake by 0.5L immediately.")
            else:
                st.success("✅ Fluid levels within optimal range.")
        with col_ins2:
            if latest['Steps'] < 5000:
                st.warning("⚠️ Low Mobility: Standing desk or brief walk recommended.")
            else:
                st.success("✅ Kinetic activity targets met.")

    with tab_table:
        st.dataframe(data.sort_values(by="Date", ascending=False), use_container_width=True, hide_index=True)

else:
    st.info("System Offline. Feed data through the manual entry node to begin analysis.")