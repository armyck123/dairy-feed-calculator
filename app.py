import streamlit as st

# ตั้งค่า state สำหรับจัดเก็บรายการอาหาร
if "feeds" not in st.session_state:
    st.session_state.feeds = []

# ส่วนหัวของแอป
st.title("🐄 คำนวณต้นทุนอาหารโคนม")

# รับค่าจำนวนโครีด
A = st.number_input("🔢 จำนวนโครีด (ตัว)", min_value=1, value=10, step=1)

# รับค่าปริมาณนมที่ผลิตต่อวัน (kg)
B = st.number_input("🥛 ปริมาณนมรวมที่ได้ต่อวัน (kg)", min_value=0.0, value=100.0, step=0.1)

# รับค่าราคานมต่อกิโลกรัม
C = st.number_input("💰 ราคานมต่อกิโลกรัม (บาท)", min_value=0.0, value=20.0, step=0.1)

# คำนวณปริมาณนมเฉลี่ยต่อตัวต่อวัน
D = B / A
# คำนวณรายได้จากการขายนม
E = D * C

st.markdown("### 📊 รายได้จากการขายนม")
st.markdown(f"<h4 style='color: green;'>🔹 ปริมาณนมเฉลี่ยต่อตัว: <b>{D:.2f}</b> kg/วัน</h4>", unsafe_allow_html=True)
st.markdown(f"<h4 style='color: green;'>🔹 รายได้จากนมต่อวัน: <b>{E:.2f}</b> บาท</h4>", unsafe_allow_html=True)

# --- ส่วนของอาหารสัตว์ ---
st.markdown("## รายการอาหารสัตว์")

# เพิ่มข้อมูลอาหารสัตว์ใหม่
with st.form("add_feed_form", clear_on_submit=True):
    col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        name = st.text_input("📌 ชื่ออาหาร", placeholder="เช่น ข้าวโพดหมัก")
    with col2:
        F = st.number_input("📦 ปริมาณ (kg/ตัว/วัน)", min_value=0.0, value=0.0, step=0.1)
    with col3:
        G = st.number_input("💰 ราคา (บาท/kg)", min_value=0.0, value=0.0, step=0.1)
    
    submitted = st.form_submit_button("➕ เพิ่มอาหาร")
    if submitted and name:
        st.session_state.feeds.append({"name": name, "F": F, "G": G})

# แสดงรายการอาหารที่เพิ่ม
total_feed_cost = 0
to_remove = None

for i, feed in enumerate(st.session_state.feeds):
    H = feed["F"] * feed["G"]
    total_feed_cost += H
    
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    
    with col1:
        st.write(f"🍃 **{feed['name']}**")
    with col2:
        st.write(f"🔸 {feed['F']:.2f} kg")
    with col3:
        st.write(f"💰 {feed['G']:.2f} บาท/kg")
    with col4:
        if st.button("❌", key=f"remove_{i}"):
            to_remove = i

# ลบรายการที่กดลบ
if to_remove is not None:
    del st.session_state.feeds[to_remove]
    st.session_state.feeds = st.session_state.feeds

# แสดงผลรวมต้นทุนอาหาร
st.markdown("### 📉 ผลลัพธ์ต้นทุนอาหาร")
st.markdown(f"<h4 style='color: orange;'>📌 ต้นทุนอาหารรวมต่อวัน: <b>{total_feed_cost:.2f}</b> บาท</h4>", unsafe_allow_html=True)

# คำนวณเปอร์เซ็นต์ต้นทุนอาหารต่อรายได้จากนม
if E > 0:
    food_cost_percentage = (total_feed_cost / E) * 100
else:
    food_cost_percentage = 0

st.markdown(f"<h4 style='color: orange;'>📊 เปอร์เซ็นต์ต้นทุนอาหารเทียบกับรายได้: <b>{food_cost_percentage:.2f}%</b></h4>", unsafe_allow_html=True)