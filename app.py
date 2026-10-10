import streamlit as st

# ============ تنظیمات اولیه ============
st.set_page_config(
    page_title="پژوهش همدلی",
    page_icon="🤝",
    layout="centered"
)

# ============ راست‌چین کردن کل برنامه ============
st.markdown("""
<style>
    .stApp, .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label, div {
        direction: rtl;
        text-align: right;
    }
    input, textarea, select {
        direction: rtl;
        text-align: right;
    }
    .stButton button {
        direction: rtl;
        text-align: right;
    }
    .stChatMessage {
        direction: rtl;
        text-align: right;
    }
    div[data-testid="stSlider"] {
        direction: ltr !important;
    }
    div[data-testid="stSlider"] > label {
        direction: rtl !important;
        text-align: right !important;
        display: block !important;
    }
</style>
""", unsafe_allow_html=True)

# ============ مدیریت وضعیت ============
if "stage" not in st.session_state:
    st.session_state.stage = "welcome"
if "demographics" not in st.session_state:
    st.session_state.demographics = {}
if "messages" not in st.session_state:
    st.session_state.messages = []

# ============ تابع پاسخ موقت (بدون LLM) ============
def get_mock_response(user_message, message_count):
    """
    پاسخ موقت برای تست ساختار چت.
    در قدم بعدی، این تابع با LLM واقعی جایگزین می‌شود.
    """
    responses = [
        "می‌شنوم. می‌تونی بیشتر توضیح بدی؟",
        "این چیزیه که گفتی. چطور احساس می‌کنی؟",
        "جالبه. از چه زمانی این حس رو داری؟",
        "من اینجا هستم تا کمکت کنم. ادامه بده.",
        "چه چیزی الان بیشتر از همه اذیتت می‌کنه؟"
    ]
    return responses[message_count % len(responses)]

# ============ صفحه ۱: خوش‌آمد ============
if st.session_state.stage == "welcome":
    st.title("🤝 پژوهش درباره همدلی در دستیارهای هوشمند")
    st.write("""
     از اینکه در این پژوهش شرکت می‌کنید سپاسگزارم مهندس دانشفر.

   این آزمایش حدود ۱۰ تا ۱۵ دقیقه زمان می‌برد,
   اطلاعات شما به‌صورت ناشناس ذخیره می‌شود.
    """)

    if st.button("موافقم، شروع کن", type="primary"):
        st.session_state.stage = "demographics"
        st.rerun()

# ============ صفحه ۲: اطلاعات پایه ============
elif st.session_state.stage == "demographics":
    st.header("اطلاعات پایه")

    age = st.number_input("سن:", min_value=18, max_value=80, value=25)
    gender = st.selectbox("جنسیت:", ["زن", "مرد", "ترجیح می‌دهم نگویم"])
    field = st.text_input("رشته تحصیلی:")
    job = st.text_input("شغل:")
    ai_familiarity = st.slider("میزان آشنایی با AI:", 1, 5, 3)

    st.divider()

    if st.button("ادامه", type="primary"):
        st.session_state.demographics = {
            "age": age,
            "gender": gender,
            "field": field,
            "job": job,
            "ai_familiarity": ai_familiarity
        }
        st.session_state.stage = "scenario"
        st.rerun()

# ============ صفحه ۳: سناریو ============
elif st.session_state.stage == "scenario":
    st.header("سناریو")

    st.write("""
    تصور کن در یک روز سخت، احساس خستگی و سردرگمی می‌کنی.
    نمی‌دانی باید به کارت ادامه بدهی یا استراحت کنی.
    تصمیم می‌گیری با یک دستیار هوشمند درباره این موضوع صحبت کنی.
    """)

    st.divider()

    if st.button("شروع گفتگو", type="primary"):
        st.session_state.stage = "chat"
        st.session_state.messages = []
        st.rerun()

# ============ صفحه ۴: چت ============
elif st.session_state.stage == "chat":
    st.header("گفتگو با دستیار هوشمند")

    # نمایش پیام‌های قبلی
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # اگر کمتر از ۱۰ پیام است، ورودی نمایش بده
    if len(st.session_state.messages) < 10:
        user_input = st.chat_input("پیام خود را بنویسید...")
        if user_input:
            # اضافه کردن پیام کاربر
            st.session_state.messages.append({"role": "user", "content": user_input})

            # پاسخ موقت (بدون LLM)
            response = get_mock_response(user_input, len(st.session_state.messages))
            st.session_state.messages.append({"role": "assistant", "content": response})

            st.rerun()
    else:
        st.info("گفتگو به پایان رسید.")
        if st.button("ادامه به پرسشنامه", type="primary"):
            st.session_state.stage = "survey"
            st.rerun()

# ============ صفحه ۵: پرسشنامه (فعلاً خالی) ============
elif st.session_state.stage == "survey":
    st.header("پرسشنامه")
    st.warning("این صفحه در قدم بعدی ساخته می‌شود.")

    if st.button("برگشت به چت"):
        st.session_state.stage = "chat"
        st.rerun()