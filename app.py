import streamlit as st
import openai

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
if "condition" not in st.session_state:
    st.session_state.condition = "C"

# ============ پرامپت‌های سه شرط ============
SYSTEM_PROMPTS = {
    "A": """تو یک دستیار هوشمند هستی. همیشه با اطمینان کامل پاسخ بده.
هرگز تردید نشان نده. هرگز از عبارات احتمالی مثل «شاید» یا «احتمالاً» استفاده نکن.
همیشه بگو «باید» یا «حتماً». پاسخ‌هایت کوتاه و قاطع باشند.""",

    "B": """تو یک دستیار هوشمند هستی. همیشه با بیان احتمال پاسخ بده.
از عبارات مثل «احتمالاً»، «ممکن است»، «شاید» استفاده کن.
اما همیشه یک راه‌حل مشخص پیشنهاد بده. پاسخ‌هایت کوتاه و محتاط باشند.""",

    "C": """تو یک دستیار هوشمند هستی. همیشه عدم‌قطعیت خود را با همدلی ترکیب کن.
از عبارات مثل «مطمئن نیستم»، «به نظر می‌رسد» استفاده کن.
همیشه از کاربر بپرس که خودش چه احساسی دارد.
هرگز راه‌حل قطعی تحمیل نکن. پاسخ‌هایت کوتاه و پرسشگر باشند."""
}

def get_system_prompt(condition):
    return SYSTEM_PROMPTS.get(condition, SYSTEM_PROMPTS["C"])

# ============ اتصال به OpenAI ============
def call_llm(system_prompt, messages):
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}] + messages
    )
    return response.choices[0].message.content

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

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if len(st.session_state.messages) < 10:
        user_input = st.chat_input("پیام خود را بنویسید...")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            with st.spinner("در حال فکر کردن..."):
                response = call_llm(
                    get_system_prompt(st.session_state.condition),
                    st.session_state.messages
                )
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
