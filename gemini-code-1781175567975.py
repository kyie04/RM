import streamlit as st
import pandas as pd
import numpy as np
import time

# --- PAGE SETUP ---
st.set_page_config(page_title="Cyber-Physical Control Center", layout="wide")

# --- INDUSTRIAL UI MATRIX ---
st.markdown("""
    <style>
    .system-title { font-size: 34px; font-weight: 800; color: #1E293B; text-align: center; }
    .mode-container { background-color: #F8FAFC; padding: 15px; border-radius: 12px; border: 1px solid #E2E8F0; text-align: center; }
    .panel-box { background-color: #FFFFFF; padding: 20px; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); }
    .alarm-strip-red { background-color: #FEF2F2; border-left: 6px solid #EF4444; color: #991B1B; padding: 12px; border-radius: 6px; font-size: 13px; font-weight: 600; margin-top: 10px;}
    .alarm-strip-green { background-color: #F0FDF4; border-left: 6px solid #22C55E; color: #166534; padding: 12px; border-radius: 6px; font-size: 13px; font-weight: 600; margin-top: 10px;}
    .alarm-strip-blue { background-color: #EFF6FF; border-left: 6px solid #3B82F6; color: #1E40AF; padding: 12px; border-radius: 6px; font-size: 13px; font-weight: 600; margin-top: 10px;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='system-title'>🏭 Cyber-Physical Resource Management Matrix</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748B; font-size:13px;'>REAL-TIME SENSOR FEEDBACK SIMULATION</p>", unsafe_allow_html=True)

# --- SESSION INITIALIZATION FOR CONTINUOUS DATA ---
if 'time_steps' not in st.session_state:
    st.session_state.time_steps = list(range(10))
    st.session_state.haccp_data = [90.0] * 10
    st.session_state.qc_data = [4.6] * 10
    st.session_state.eng_data = [43.5] * 10

# --- CONTROL INTERFACE ---
st.markdown("<div class='mode-container'>", unsafe_allow_html=True)
col_m1, col_m2 = st.columns(2)
with col_m1:
    sys_mode = st.toggle("🤖 ENGAGE AUTOMATED FEEDBACK SYSTEM (AUTO-PILOT)", value=False)
with col_m2:
    stress_test = st.button("⚡ INJECT SYSTEM RISK ANOMALY (STRESS TEST)")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Handle Stress Test Spike Logic
if stress_test:
    st.session_state.haccp_data[-1] = 112.0  # Spikes past 95°C limit
    st.session_state.qc_data[-1] = 3.6      # Drops past 4.4 pH limit
    st.session_state.eng_data[-1] = 56.0    # Spikes past 45°C limit

# Handle Auto-Pilot Active Loop
if sys_mode:
    # If out of bounds, the feedback control loop calculates and applies immediate corrections
    if st.session_state.haccp_data[-1] > 95.0 or st.session_state.haccp_data[-1] < 85.0:
        st.session_state.haccp_data[-1] = 91.5 # Feedback loops force parameter back to optimum
    if st.session_state.qc_data[-1] > 4.8 or st.session_state.qc_data[-1] < 4.4:
        st.session_state.qc_data[-1] = 4.55
    if st.session_state.eng_data[-1] > 45.0 or st.session_state.eng_data[-1] < 42.0:
        st.session_state.eng_data[-1] = 43.2

# Get current snapshot values
curr_haccp = st.session_state.haccp_data[-1]
curr_qc = st.session_state.qc_data[-1]
curr_eng = st.session_state.eng_data[-1]

# --- LIVE WORKSTATIONS GRID ---
col1, col2, col3 = st.columns(3)

# ==========================================
# STATION 1: HACCP MANAGER
# ==========================================
with col1:
    st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
    st.subheader("🛡️ HACCP Station")
    st.caption("Target Control Band: 85.0°C – 95.0°C")
    
    # Live Real-Time Data Streaming Visualization
    df_haccp = pd.DataFrame({"Temperature (°C)": st.session_state.haccp_data})
    st.line_chart(df_haccp, height=180, y_label="Temp °C")
    
    st.metric("Live Core Sensor Reading", f"{curr_haccp} °C")
    
    if 85.0 <= curr_haccp <= 95.0:
        st.markdown("<div class='alarm-strip-green'>🟢 VALVE POSITION: OPEN<br>CCP is within safety criteria thresholds.</div>", unsafe_allow_html=True)
    else:
        if sys_mode:
            st.markdown("<div class='alarm-strip-blue'>🔵 AUTOMATION COUNTER-MEASURE EXECUTED<br>Inline data logging triggered flow diversion loop. System recovered safely.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='alarm-strip-red'>🚨 CRITICAL DEVIATION BREACH<br>Corrective Action Required: Immediately engage hold protocol on current batch line.</div>", unsafe_allow_html=True)
            # Interactive intervention slider for Manual Mode
            manual_haccp = st.slider("Manual Override Valve Adjuster:", 70.0, 110.0, float(curr_haccp), step=0.5, key="man_h")
            if st.button("🔧 Deploy Manual Adjustment Protocol", key="btn_h"):
                st.session_state.haccp_data[-1] = manual_haccp
                st.rerun()
                
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STATION 2: QC MANAGER
# ==========================================
with col2:
    st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
    st.subheader("🔬 QC Metrics Lab")
    st.caption("Target Control Band: pH 4.4 – 4.8")
    
    df_qc = pd.DataFrame({"Acidity Curve (pH)": st.session_state.qc_data})
    st.line_chart(df_qc, height=180, y_label="pH")
    
    st.metric("Live Inline Diagnostics", f"{curr_qc} pH")
    
    if 4.4 <= curr_qc <= 4.8:
        st.markdown("<div class='alarm-strip-green'>🟢 METRIC STABILITY: UNIFORM<br>Acidity configurations align with batch uniformity.</div>", unsafe_allow_html=True)
    else:
        if sys_mode:
            st.markdown("<div class='alarm-strip-blue'>🔵 AUTOMATION COUNTER-MEASURE EXECUTED<br>Inline diagnostics intercepted variation. Rapid self-correction completed.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='alarm-strip-red'>🚨 QUALITY BLOCK: ANOMALY<br>Corrective Action Required: Deploy rapid manual titration testing kits immediately.</div>", unsafe_allow_html=True)
            manual_qc = st.slider("Manual pH Acid Injector Calibration:", 3.5, 5.5, float(curr_qc), step=0.1, key="man_q")
            if st.button("🔧 Deploy Manual Adjustment Protocol", key="btn_q"):
                st.session_state.qc_data[-1] = manual_qc
                st.rerun()
                
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STATION 3: PROCESS ENGINEER
# ==========================================
with col3:
    st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
    st.subheader("⚙️ Engineering Thermal Loop")
    st.caption("Target Control Band: 42.0°C – 45.0°C")
    
    df_eng = pd.DataFrame({"Thermal Energy Matrix": st.session_state.eng_data})
    st.line_chart(df_eng, height=180, y_label="Temp °C")
    
    st.metric("Live Grid Thermal Load", f"{curr_eng} °C")
    
    if 42.0 <= curr_eng <= 45.0:
        st.markdown("<div class='alarm-strip-green'>🟢 HEAT RECOVERY LOOP: BALANCED<br>Closed-loop matrix operating at thermal equilibrium.</div>", unsafe_allow_html=True)
    else:
        if sys_mode:
            st.markdown("<div class='alarm-strip-blue'>🔵 AUTOMATION COUNTER-MEASURE EXECUTED<br>Closed-loop control grid engaged utility dampening. Energy flow optimized.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='alarm-strip-red'>🚨 ENERGY FOOTPRINT EXPANSION<br>Corrective Action Required: Manually vent heat systems or override heating utilities.</div>", unsafe_allow_html=True)
            manual_eng = st.slider("Manual Heat Exchanger Gate Valve:", 35.0, 55.0, float(curr_eng), step=0.5, key="man_e")
            if st.button("🔧 Deploy Manual Adjustment Protocol", key="btn_e"):
                st.session_state.eng_data[-1] = manual_eng
                st.rerun()
                
    st.markdown("</div>", unsafe_allow_html=True)

# Continuous background time-progression emulation 
time.sleep(0.3)
if not stress_test:
    # Continuously feed normal operations noise data if no anomaly is injected
    st.session_state.haccp_data = st.session_state.haccp_data[1:] + [float(np.random.normal(90.0, 0.4))]
    st.session_state.qc_data = st.session_state.qc_data[1:] + [float(np.random.normal(4.6, 0.03))]
    st.session_state.eng_data = st.session_state.eng_data[1:] + [float(np.random.normal(43.5, 0.2))]
    st.rerun()