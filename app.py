import streamlit as st
import time
import plotly.graph_objects as go

# 1. ตั้งค่าหน้าเว็บให้สวยงามและรองรับกราฟขนาดใหญ่
st.set_page_config(page_title="โปรแกรมประเมินความเสี่ยงโรคหัวใจ", layout="centered")

# 🌟 2. ใส่ CSS เพื่อเปลี่ยนสีตัวเว็บ พื้นหลังไล่เฉด และปรับแต่งช่องกรอกให้เหมือนแอปในรูปเป๊ะๆ
st.markdown("""
    <style>
    /* เปลี่ยนพื้นหลังของทั้งเว็บเป็นแบบไล่เฉดสีเขียว-ฟ้า (Gradient) */
    .stApp {
        background: linear-gradient(135deg, #a3e4d7 0%, #3498db 100%);
    }
    
    /* ปรับแต่ง Title และหัวข้อหลักให้เป็นสีเขียวเข้มพาสเทล */
    h1 {
        color: #114b5f !important;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: bold;
        text-align: center;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
    }
    
    p, label, .stMarkdown {
        color: #165b65 !important;
        font-weight: 600;
    }
    
    /* ทำกล่องอินพุตและปุ่มให้โค้ดมนสีขาวพรีเมียม */
    .stNumberInput div div input, .stSelectbox div div div {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 12px !important;
        border: 2px solid #64c4b6 !important;
        color: #114b5f !important;
    }
    
    /* ปรับแต่งปุ่ม "ประมวลผล" ให้เด่นสะดุดตา */
    .stButton>button {
        background: linear-gradient(90deg, #16a085 0%, #114b5f 100%) !important;
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 10px 0px !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 6px 15px rgba(0,0,0,0.2);
    }
    
    /* ปรับแต่งกล่องผลลัพธ์สีขาวโค้งมนลอยขึ้นมา (Card Style) */
    div[data-testid="stMetricWidget"] {
        background-color: white !important;
        border-radius: 16px !important;
        padding: 15px !important;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.1) !important;
        border: 1px solid rgba(255,255,255,0.8) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 แบบประเมินความเสี่ยงภาวะโรคหัวใจ")
st.write("กรอกข้อมูลสุขภาพด้านล่างเพื่อประมวลผลด้วยแบบจำลองคณิตศาสตร์")

# =================================================================
# ส่วนที่ 3: รับข้อมูลอินพุตจากผู้ใช้งาน และคำนวณ BMI อัตโนมัติ
# =================================================================

age = st.number_input("อายุ (ปี)", min_value=1, max_value=120, value=17)

# รับข้อมูลน้ำหนักและส่วนสูง เพื่อนำไปคำนวณ BMI อัตโนมัติ
weight = st.number_input("น้ำหนัก (กิโลกรัม)", min_value=1.0, max_value=200.0, value=60.0, step=0.1)
height_cm = st.number_input("ส่วนสูง (เซนติเมตร)", min_value=50.0, max_value=250.0, value=170.0, step=0.1)

# คำนวณค่า BMI อัตโนมัติด้วยสูตรคณิตศาสตร์
height_m = height_cm / 100
bmi = weight / (height_m ** 2)

# แสดงค่า BMI ที่คำนวณได้ให้ผู้ใช้เห็นบนหน้าจอ
st.write(f"💡 **ดัชนีมวลกาย (BMI) ของคุณคือ:** `{bmi:.2f}`")

# อินพุตปัจจัยเสี่ยงอื่นๆ
gender = st.selectbox("เพศ", ["ชาย", "หญิง"])
bp_sys = st.number_input("ความดันโลหิตตัวบน (mmHg)", min_value=50, max_value=250, value=120)
hr_rest = st.number_input("อัตราการเต้นของหัวใจขณะพัก (bpm)", min_value=30, max_value=200, value=75)
family_history = st.selectbox("มีประวัติคนในครอบครัวเป็นโรคหัวใจหรือไม่", ["ไม่มี", "มี"])


# =================================================================
# ส่วนที่ 4: ปุ่มประมวลผลและการคำนวณคะแนนพร้อมหน้าปัดดีไซน์พรีเมียม
# =================================================================

if st.button(label="ประมวลผล", use_container_width=True):
    
    # 🌟 อนิเมชั่นแถบเปอร์เซ็นต์สีฟ้าค่อยๆ วิ่งโหลด (Progress Bar) ตามรูปภาพเรฟของคุณ
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for percent_complete in range(100):
        time.sleep(0.012)  
        progress_bar.progress(percent_complete + 1)
        status_text.markdown(f"⏳ **กำลังประมวลผลด้วยแบบจำลองคณิตศาสตร์... {percent_complete + 1}%**")
        
    status_text.empty()
    progress_bar.empty()
    
    # คำนวณคะแนนพื้นฐานแยกตาม ช่วงอายุ และ ช่วง BMI
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

    # บวกเพิ่มจากปัจจัยเสี่ยงอื่นๆ
    extra_risk = 0.0
    if gender == "ชาย":          extra_risk += 5.0
    if bp_sys >= 140:           extra_risk += 10.0
    if hr_rest > 100:           extra_risk += 10.0
    if family_history == "มี":   extra_risk += 10.0
        
    risk_prob = min(base_risk + extra_risk, 100.0)

    if risk_prob <= 20:
        risk_level = "ต่ำมาก (Very Low)"
        gauge_color = "#2ecc71"
        advice = "🟢 **คำแนะนำการดูแลตนเอง:** สุขภาพอยู่ในเกณฑ์ดีเยี่ยม รักษาวินัยการรับประทานอาหารและการออกกำลังกายสม่ำเสมอต่อไปครับ"
    elif risk_prob <= 40:
        risk_level = "ต่ำ (Low)"
        gauge_color = "#27ae60"
        advice = "🟢 **คำแนะนำการดูแลตนเอง:** มีความเสี่ยงต่ำ ควรตรวจสุขภาพประจำปีอย่างสม่ำเสมอเพื่อเฝ้าระวังพฤติกรรมเสี่ยง"
    elif risk_prob <= 60:
        risk_level = "ปานกลาง (Medium)"
        gauge_color = "#f39c12"
        advice = "🟡 **คำแนะนำการดูแลตนเอง:** ความเสี่ยงระดับปานกลาง ควรเริ่มลดอาหารประเภท หวาน มัน เค็ม และออกกำลังกายอย่างน้อย 150 นาทีต่อสัปดาห์"
    elif risk_prob <= 80:
        risk_level = "สูง (High)"
        gauge_color = "#d35400"
        advice = "🟠 **คำแนะนำการดูแลตนเอง:** ความเสี่ยงระดับสูง! แนะนำให้เข้าพบแพทย์เพื่อตรวจเช็กระบบหัวใจและหลอดเลือดอย่างละเอียด"
    else:
        risk_level = "สูงมาก (Very High)"
        gauge_color = "#c0392b"
        advice = "🔴 **ข้อควรระวัง:** คุณมีความเสี่ยงสูงมาก! จำเป็นต้องปรับพฤติกรรมอย่างเข้มงวดและรีบเข้าพบแพทย์เฉพาะทางเพื่อรับการวินิจฉัยโดยเร็วที่สุด"

    # แสดงผลลัพธ์ในกล่องการ์ดสีขาวโค้งมน
    st.write("---")
    st.subheader("📊 สรุปผลการประเมินความเสี่ยง")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="ระดับความเสี่ยง", value=risk_level)
    with col2:
        st.metric(label="โอกาสเกิดภาวะเสี่ยง", value=f"{risk_prob:.0f}%")

    # 🌟 วาดหน้าปัดเกจวัดความเสี่ยงขนาดใหญ่เบิ้มให้เข้ากับธีมใหม่
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_prob,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "#114b5f"},
            'bar': {'color': gauge_color, 'thickness': 0.3},  
            'bgcolor': "rgba(255,255,255,0.5)",
            'borderwidth': 2,
            'bordercolor': "#114b5f",
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
        title={'text': "Mathematical Risk Gauge", 'y':0.85, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
        font={'color': "#114b5f", 'family': "Arial", 'size': 16},
        paper_bgcolor='rgba(0,0,0,0)',  # ทำให้พื้นหลังกราฟโปร่งใสกลืนไปกับเว็บ
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=60, b=20),
        height=450  
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.info(advice)
