import streamlit as st
import time
import plotly.graph_objects as go

# 1. ตั้งค่า Layout และบังคับหน้าเว็บจำลองทรงมือถือด้วย CSS
st.set_page_config(page_title="โปรแกรมประเมินความเสี่ยงโรคหัวใจ", layout="centered")

# 🎨 ส่วนตกแต่งสไตล์แอปพลิเคชันมือถือโทนสีน้ำเงินการแพทย์
st.markdown("""
    <style>
    /* บีบหน้าจอหลักให้กว้างเท่าหน้าจอมือถือเพื่อความสมจริง */
    .block-container {
        max-width: 420px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        background-color: #ffffff;
        border-radius: 30px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: auto;
    }
    /* ปรับปุ่มประมวลผลเป็นสีน้ำเงินเข้มขอบมน */
    div.stButton > button:first-child {
        background-color: #1e3d59;
        color: white;
        border-radius: 12px;
        border: none;
        height: 45px;
        font-weight: bold;
        font-size: 16px;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #17b978;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# หัวข้อแอปใช้สีน้ำเงินกรมท่า น่าเชื่อถือ
st.markdown("<h2 style='text-align: center; color: #1e3d59;'>🏥 แอปประเมินโรคหัวใจ</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>กรอกข้อมูลสุขภาพเพื่อคำนวณผ่านโมเดลคณิตศาสตร์</p>", unsafe_allow_html=True)

# =================================================================
# ส่วนรับข้อมูลอินพุต
# =================================================================
age = st.number_input("อายุ (ปี)", min_value=1, max_value=120, value=17)
weight = st.number_input("น้ำหนัก (กิโลกรัม)", min_value=1.0, max_value=200.0, value=60.0, step=0.1)
height_cm = st.number_input("ส่วนสูง (เซนติเมตร)", min_value=50.0, max_value=250.0, value=170.0, step=0.1)

height_m = height_cm / 100
bmi = weight / (height_m ** 2)
st.write(f"💡 **ดัชนีมวลกาย (BMI) คือ:** `{bmi:.2f}`")

gender = st.selectbox("เพศ", ["ชาย", "หญิง"])
bp_sys = st.number_input("ความดันโลหิตตัวบน (mmHg)", min_value=50, max_value=250, value=120)
hr_rest = st.number_input("อัตราการเต้นของหัวใจขณะพัก (bpm)", min_value=30, max_value=200, value=75)
family_history = st.selectbox("มีประวัติคนในครอบครัวเป็นโรคหัวใจหรือไม่", ["ไม่มี", "มี"])

# =================================================================
# ปุ่มประมวลผลแอนิเมชัน % วิ่งโหลด และเกจวัดความเสี่ยง
# =================================================================
if st.button(label="ประมวลผล", use_container_width=True):
    
    # 🌟 1. อนิเมชั่นแถบเปอร์เซ็นต์สีฟ้าวิ่งโหลด (Progress Bar) 
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for percent_complete in range(100):
        time.sleep(0.012)  
        progress_bar.progress(percent_complete + 1)
        status_text.markdown(f"<p style='text-align:center; color:#17b978;'>⏳ <b>กำลังประมวลผลด้วยแบบจำลองคณิตศาสตร์... {percent_complete + 1}%</b></p>", unsafe_allow_html=True)
        
    status_text.empty()
    progress_bar.empty()
    
    # 2. คำนวณคะแนนตามตารางเงื่อนไขโครงงาน
    base_risk = 0.0
    if age < 30:
        if bmi < 18.5:            base_risk = 10.0
        elif 18.5 <= bmi <= 22.9: base_risk = 10.0
        elif 23.0 <= bmi <= 24.9: base_risk = 20.0
        elif 25.0 <= bmi <= 29.9: base_risk = 35.0
        else:                     base_risk = 50.0
    elif 30 <= age <= 39:
        if bmi < 18.5:            base_risk = 20.0
        elif 18.5 <= bmi <= 22.9: base_risk = 20.0
        elif 23.0 <= bmi <= 24.9: base_risk = 35.0
        elif 25.0 <= bmi <= 29.9: base_risk = 50.0
        else:                     base_risk = 65.0
    elif 40 <= age <= 49:
        if bmi < 18.5:            base_risk = 35.0
        elif 18.5 <= bmi <= 22.9: base_risk = 35.0
        elif 23.0 <= bmi <= 24.9: base_risk = 50.0
        elif 25.0 <= bmi <= 29.9: base_risk = 65.0
        else:                     base_risk = 80.0
    elif 50 <= age <= 59:
        if bmi < 18.5:            base_risk = 50.0
        elif 18.5 <= bmi <= 22.9: base_risk = 50.0
        elif 23.0 <= bmi <= 24.9: base_risk = 65.0
        elif 25.0 <= bmi <= 29.9: base_risk = 80.0
        else:                     base_risk = 90.0
    else:
        if bmi < 18.5:            base_risk = 65.0
        elif 18.5 <= bmi <= 22.9: base_risk = 65.0
        elif 23.0 <= bmi <= 24.9: base_risk = 75.0
        elif 25.0 <= bmi <= 29.9: base_risk = 90.0
        else:                     base_risk = 100.0

    extra_risk = 0.0
    if gender == "ชาย":           extra_risk += 5.0
    if bp_sys >= 140:            extra_risk += 10.0
    if hr_rest > 100:            extra_risk += 10.0
    if family_history == "มี":     extra_risk += 10.0
        
    risk_prob = min(base_risk + extra_risk, 100.0)

    # กำหนดระดับความเสี่ยงตามเกณฑ์สีไฟจราจร
    if risk_prob <= 20:
        risk_level = "ต่ำมาก (Very Low)"
        gauge_color = "#2ecc71"
        advice = "🟢 **คำแนะนำ:** สุขภาพอยู่ในเกณฑ์ดีเยี่ยม รักษาวินัยการรับประทานอาหารและการออกกำลังกายสม่ำเสมอต่อไปครับ"
    elif risk_prob <= 40:
        risk_level = "ต่ำ (Low)"
        gauge_color = "#27ae60"
        advice = "🟢 **คำแนะนำ:** มีความเสี่ยงต่ำ ควรตรวจสุขภาพประจำปีอย่างสม่ำเสมอเพื่อเฝ้าระวังพฤติกรรมเสี่ยง"
    elif risk_prob <= 60:
        risk_level = "ปานกลาง (Medium)"
        gauge_color = "#f39c12"
        advice = "🟡 **คำแนะนำ:** ความเสี่ยงระดับปานกลาง ควรเริ่มลดอาหารประเภท หวาน มัน เค็ม และออกกำลังกายต่อเนื่อง"
    elif risk_prob <= 80:
        risk_level = "สูง (High)"
        gauge_color = "#d35400"
        advice = "🟠 **คำแนะนำ:** ความเสี่ยงระดับสูง! แนะนำให้เข้าพบแพทย์เพื่อตรวจเช็กระบบหัวใจและหลอดเลือดอย่างละเอียด"
    else:
        risk_level = "สูงมาก (Very High)"
        gauge_color = "#c0392b"
        advice = "🔴 **ข้อควรระวัง:** คุณมีความเสี่ยงสูงมาก! จำเป็นต้องปรับพฤติกรรมอย่างเข้มงวดและรีบพบแพทย์เฉพาะทาง"

    # แสดงผลลัพธ์ข้อมูลสรุป
    st.markdown("<h3 style='text-align: center; color: #1e3d59;'>📊 สรุปผลการประเมิน</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
         st.markdown(f"<p style='text-align:center; font-size:14px; margin-bottom:0;'>ระดับความเสี่ยง</p><h4 style='text-align:center; color:{gauge_color}; margin-top:0;'>{risk_level}</h4>", unsafe_allow_html=True)
    with col2:
         st.markdown(f"<p style='text-align:center; font-size:14px; margin-bottom:0;'>โอกาสเกิดภาวะเสี่ยง</p><h2 style='text-align:center; margin-top:0;'>{risk_prob:.0f}%</h2>", unsafe_allow_html=True)

    # 🌟 2. วาดหน้าปัดเกจวัดความเสี่ยงขนาดใหญ่ตามเฉดสีผลลัพธ์
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_prob,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#888888"},
            'bar': {'color': gauge_color, 'thickness': 0.25},
            'bgcolor': "white",
            'steps': [
                {'range': [0, 20], 'color': "#e8f8f5"},
                {'range': [20, 40], 'color': "#eafaf1"},
                {'range': [40, 60], 'color': "#fef9e7"},
                {'range': [60, 80], 'color': "#fdf2e9"},
                {'range': [80, 100], 'color': "#fdedec"}
            ]
        }
    ))
    
    fig.update_layout(
        font={'color': "#1e3d59", 'family': "Arial", 'size': 14},
        margin=dict(l=10, r=10, t=10, b=10),
        height=280  
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.info(advice)
