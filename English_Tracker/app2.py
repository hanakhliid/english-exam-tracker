from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# إعدادات الصفحة
st.set_page_config(page_title="online tracking", layout="wide")

# تصميم رايق: خلفية داكنة مع لمسات باللون الأحمر الهادئ
st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }
    .student-card {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #2d2d2d;
        border-right: 5px solid #d9534f;
        margin-bottom: 20px;
    }
    h1, h2, h3, h4 {
        color: #d9534f !important;
    }
    .stCheckbox label {
        color: #f1f1f1 !important;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #8b0000;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("📚 online tracker")
st.markdown("---")

# الاتصال بالجوجل شيت
conn = st.connection("gsheets", type=GSheetsConnection)

sheet_tabs = ["sec1", "sec2", "sec3"]
col_tab, col_asst = st.columns([1, 1])

with col_tab:
  selected_tab = st.selectbox("📂 اختاري المجموعة:", sheet_tabs)

# قراءة البيانات
try:
  df = conn.read(worksheet=selected_tab, ttl=0)
except Exception as e:
  st.error(f"عذراً، ورقة العمل '{selected_tab}' غير موجودة في ملف الجوجل شيت.")
  st.stop()

if df.empty:
  st.warning("الشيت فاضي حالياً.")
else:
  df = df.dropna(how="all")
  df.columns = df.columns.astype(str).str.strip()

  assistant_col = (
      "الاسستنت المسؤول"
      if "الاسستنت المسؤول" in df.columns
      else "الأستاذ المسؤول"
  )

  # قائمة الأسستنتس (يمكنك تعديلها أو إضافتها هنا براحتك)
  default_assistants = ["logy", "khadeeja", "asmaa", "rana", "hagar"]
  sheet_assistants = (
      [str(x).strip().lower() for x in df[assistant_col].dropna().unique()]
      if assistant_col in df.columns
      else []
  )
  all_assistants = sorted(list(set(default_assistants + sheet_assistants)))

  with col_asst:
    selected_assistant = st.selectbox(
        "👩‍🏫 اختر اسم الأسستنت:", ["الكل"] + all_assistants
    )

  st.markdown("<br>", unsafe_allow_html=True)

  # اليوم الحالي بالعربي
  days_map = {
      "Sunday": "الأحد",
      "Monday": "الإثنين",
      "Tuesday": "الثلاثاء",
      "Wednesday": "الأربعاء",
      "Thursday": "الخميس",
      "Friday": "الجمعة",
      "Saturday": "السبت",
  }
  today_english = datetime.now().strftime("%A")
  today_arabic = days_map.get(today_english, "الأحد")

  day_col = "اليوم المثبت" if "اليوم المثبت" in df.columns else "اليوم"

  if day_col not in df.columns:
    st.error("عذراً، عمود اليوم غير موجود في الشيت.")
  else:
    df[day_col] = df[day_col].astype(str).str.strip()
    todays_students = df[df[day_col] == today_arabic]

    # تصفية حسب الأسستنت
    if selected_assistant != "الكل" and assistant_col in df.columns:
      todays_students = todays_students[
          todays_students[assistant_col].astype(str).str.strip().str.lower()
          == selected_assistant
      ]

    st.subheader(
        f"📅 طلبة يوم ({today_arabic}) — الأسستنت: ({selected_assistant})"
    )
    st.write(f"عدد الطلاب المطلوب متابعتهم: **{len(todays_students)}** طالب/ة")
    st.markdown("<br>", unsafe_allow_html=True)

    if todays_students.empty:
      st.info(
          f"مفيش طلاب مسجلين اليوم ({today_arabic}) لـ الأسستنت"
          f" ({selected_assistant})."
      )
    else:
      all_lectures = ["lec1", "lec2", "lec3", "lec4", "lec5", "lec6", "lec7"]

      for idx, row in todays_students.iterrows():

        def clean_phone(val):
          if pd.isna(val):
            return "غير متوفر"
          s = str(val).strip()
          if s.endswith(".0"):
            s = s[:-2]
          return s

        name = (
            str(row.get("اسم الطالب ثلاثي"))
            if pd.notna(row.get("اسم الطالب ثلاثي"))
            else "بدون اسم"
        )
        whatsapp = clean_phone(row.get("رقم الواتساب"))
        parent_phone = clean_phone(row.get("رقم ولي الأمر"))
        session_time = (
            str(row.get("الساعة"))
            if pd.notna(row.get("الساعة"))
            else "غير محددة"
        )
        assistant = (
            str(row.get(assistant_col))
            if pd.notna(row.get(assistant_col))
            else "غير محدد"
        )
        notes = str(row.get("ملاحظات")) if pd.notna(row.get("ملاحظات")) else ""

        # تحديد الحصة التي عليها الدور أوتوماتيكياً
        current_lecture = "lec1"
        for lec in all_lectures:
          if lec not in df.columns:
            df[lec] = False
          val = row.get(lec)
          if pd.isna(val) or val == "" or val is False:
            current_lecture = lec
            break
          current_lecture = lec

        hw_col = f"hw {current_lecture}"
        exam_col = None
        for col in df.columns:
          if "درجة" in col and current_lecture.replace("lec", "") in col:
            exam_col = col
            break
        if not exam_col:
          exam_col = "درجة الامتحان"
          if exam_col not in df.columns:
            df[exam_col] = ""

        if hw_col not in df.columns:
          df[hw_col] = False


        def parse_bool(val):
          if isinstance(val, bool):
            return val
          if str(val).lower() in ["true", "1", "t", "yes"]:
            return True
          return False


        current_lec_val = parse_bool(row.get(current_lecture, False))
        current_hw_val = parse_bool(row.get(hw_col, False))
        current_exam_score = str(row.get(exam_col, ""))
        if current_exam_score == "nan":
          current_exam_score = ""

        with st.container():
          st.markdown('<div class="student-card">', unsafe_allow_html=True)

          st.markdown(
              f"### 👤 {name} &nbsp;&nbsp;|&nbsp;&nbsp; 📌 الحصة التي عليها الدور"
              f" أوتوماتيكياً: <span"
              f" style='color:#d9534f;'>{current_lecture}</span>",
              unsafe_allow_html=True,
          )
          st.markdown("<br>", unsafe_allow_html=True)

          col1, col2, col3 = st.columns([2, 2, 2])

          with col1:
            st.markdown(f"📱 **واتساب:** `{whatsapp}`")
            st.markdown(f"👨‍👧 **ولي الأمر:** `{parent_phone}`")
            st.markdown(f"⏰ **الموعد:** `{session_time}`")
            st.markdown(f"👩‍🏫 **الأسستنت:** `{assistant}`")

          with col2:
            st.markdown(f"**متابعة الحصة الحالية ({current_lecture}):**")
            new_lec_val = st.checkbox(
                f"حضور ({current_lecture})",
                value=current_lec_val,
                key=f"lec_{current_lecture}_{idx}",
            )
            new_hw_val = st.checkbox(
                f"استلام الواجب ({hw_col})",
                value=current_hw_val,
                key=f"hw_{current_lecture}_{idx}",
            )

          with col3:
            new_exam_score = st.text_input(
                f"درجة الامتحان ({current_lecture})",
                value=current_exam_score,
                key=f"exam_{current_lecture}_{idx}",
            )
            new_notes = st.text_input(
                "تحديث الملاحظات",
                value=notes if notes != "nan" else "",
                key=f"notes_{idx}",
            )

            changed = False
            if new_lec_val != current_lec_val:
              df.at[idx, current_lecture] = new_lec_val
              changed = True
            if new_hw_val != current_hw_val:
              df.at[idx, hw_col] = new_hw_val
              changed = True
            if (
                new_exam_score != current_exam_score
                and str(new_exam_score) != "nan"
            ):
              df.at[idx, exam_col] = new_exam_score
              changed = True
            if new_notes != notes and str(new_notes) != "nan":
              df.at[idx, "ملاحظات"] = new_notes
              changed = True

            if changed:
              conn.update(worksheet=selected_tab, data=df)
              st.success("تم التحديث والحفظ في الجوجل شيت بنجاح! ✨")
              st.rerun()

          st.markdown("</div>", unsafe_allow_html=True)