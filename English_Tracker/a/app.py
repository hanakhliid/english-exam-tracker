import streamlit as st

# إعداد الصفحة وتغيير الأيقونة
st.set_page_config(
    page_title="نتيجة الامتحان الشامل - English House ",
    page_icon="📚",
    layout="centered",
)

# تنسيق CSS مخصص (كل الأزرار والصناديق بلون أحمر متناسق)
st.markdown(
    """
    <style>
    /* جعل خلفية الصفحة بالكامل بيضاء */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* تنسيق اسم المستر (خط أنيق ومميز) */
    .instructor-name {
        text-align: center;
        font-size: 22px;
        font-family: 'Brush Script MT', cursive, serif;
        font-weight: bold;
        color: #333333;
        margin-top: 5px;
        margin-bottom: 25px;
        letter-spacing: 1px;
    }
    
    /* تنسيق عنوان "الآن .. نتيجة الامتحان الشامل الاول" */
    .main-title {
        font-size: 32px !important;
        font-weight: 900 !important;
        color: #000000 !important;
        text-align: center;
        margin-bottom: 30px;
        font-family: 'Cairo', sans-serif;
    }
    
    /* تنسيق النصوص العامة بالأسود */
    h1, h2, h3, p, label {
        color: #000000 !important;
    }
    
    /* صندوق النتيجة بلون أحمر أنيق */
    .result-box {
        background-color: #FDEDEC;
        border: 2px solid #E74C3C;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0px 4px 10px rgba(231, 76, 60, 0.15);
    }
    
    /* تغيير زر "عرض النتيجة" ليكون باللون الأحمر بدل الأخضر */
    div.stButton > button {
        background-color: #E74C3C;
        color: white;
        font-weight: bold;
        font-size: 16px;
        border-radius: 8px;
        border: none;
        padding: 10px;
    }
    div.stButton > button:hover {
        background-color: #C0392B;
        color: white;
    }
    
    /* رسالة التنبيه باللون الأحمر */
    .custom-error {
        background-color: #FDEDEC;
        color: #C0392B !important;
        border: 1px solid #F5B7B1;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-top: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 1. وضع لوجو الأكاديمية في المنتصف
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("logo.png.jpeg", width=150)

# اسم المستر بخط أنيق
st.markdown(
    '<p class="instructor-name">~ Mr. Mohamed El Sayed ~</p>',
    unsafe_allow_html=True,
)

# 2. العنوان الرئيسي
st.markdown(
    '<p class="main-title">الآن .. نتيجة الامتحان الشامل الاول</p>',
    unsafe_allow_html=True,
)

# 3. اختيار الصف الدراسي
grade_level = st.selectbox(
    "اختر الصف الدراسي",
    ["الصف الثالث الثانوي", "الصف الثاني الثانوي", "الصف الأول الثانوي"],
)

# 4. إدخال رقم الجلوس
seat_no = st.text_input("أدخل رقم الجلوس", placeholder="مثلاً: 2212006")

# 5. زر عرض النتيجة
if st.button("عرض النتيجة", use_container_width=True):
    if seat_no.strip() == "":
        st.markdown(
            '<div class="custom-error">⚠️ الرجاء إدخال رقم الجلوس أولاً لعرض النتيجة!</div>',
            unsafe_allow_html=True,
        )
    else:
        # عرض النتيجة بالبيانات المحددة (هناء خالد سيد - الصف الثالث الثانوي - 55/60)
        st.markdown(
            f"""
            <div class="result-box">
                <h2 style="color: #922B21 !important; margin-bottom: 15px;">نتيجة الطالب</h2>
                <p style="font-size: 18px; margin: 5px 0;"><b>اسم الطالب:</b> هناء خالد سيد</p>
                <p style="font-size: 18px; margin: 5px 0;"><b>الصف الدراسي:</b> {grade_level}</p>
                <p style="font-size: 18px; margin: 5px 0;"><b>رقم الجلوس:</b> {seat_no}</p>
                <hr style="margin: 15px 0; border: 0; border-top: 1px solid #E6B0AA;">
                <p style="font-size: 22px; color: #C0392B !important; font-weight: bold;">درجة الامتحان: 55 / 60</p>
            </div>
            """,
            unsafe_allow_html=True,
        )