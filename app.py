import streamlit as st
from openai import OpenAI
import base64

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="DeepTrace", page_icon="🦖", layout="centered")

# --- 2. TWÓJ LUKSUSOWY CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #1a1a1a, #050505); color: #e5e5e5; }
    .main-title { font-family: 'Georgia', serif; font-size: 3.5rem; background: linear-gradient(90deg, #fbbf24, #d97706, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 20px; }
    .stButton>button { width: 100%; height: 3em; background: transparent !important; color: #fbbf24 !important; border: 1px solid #fbbf24 !important; border-radius: 10px; font-weight: bold; }
    .stButton>button:hover { background: #fbbf24 !important; color: #000 !important; box-shadow: 0 0 20px rgba(251, 191, 36, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIKA DOSTĘPU (NAFFY SYNC) ---
# Tutaj ręcznie lub półautomatycznie dodajesz klientów z Naffy
VIP_DATABASE = {
    "admin@eduai.pl": "RUM2026",
    "klient@naffy.pl": "VIP-7788" # Przykładowy klient
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<h1 class="main-title">DEEPTRACE ALPHA</h1>', unsafe_allow_html=True)
    st.info("System aktywny. Zaloguj się danymi, które otrzymałeś po zakupie na Naffy.")
    
    email = st.text_input("TWÓJ E-MAIL")
    password = st.text_input("KLUCZ DOSTĘPU", type="password")
    
    if st.button("ODBLOKUJ ARCHITEKTA"):
        if email in VIP_DATABASE and VIP_DATABASE[email] == password:
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.rerun()
        else:
            st.error("Brak dostępu. Sprawdź e-mail lub kup subskrypcję.")
else:
    # --- 4. INTERFEJS CZATU (ZALOGOWANY) ---
    st.sidebar.markdown("<h1 style='color: #fbbf24;'>🦖 EduAI PRO</h1>", unsafe_allow_html=True)
    st.sidebar.success(f"Aktywny: {st.session_state.user_email}")
    
    if st.sidebar.button("Wyloguj"):
        st.session_state.authenticated = False
        st.rerun()

    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["GROQ_API_KEY"]
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.markdown('<h1 class="main-title">DeepTrace Alpha</h1>', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Zadaj pytanie DeepTrace..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analizuję..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": "Jesteś Architektem EduAI DeepTrace. Bądź luksusowy i mądry."}] + st.session_state.chat_history
                    )
                    res = response.choices[0].message.content
                    st.markdown(res)
                    st.session_state.chat_history.append({"role": "assistant", "content": res})
                except Exception as e:
                    st.error(f"Błąd: {e}")
