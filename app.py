import streamlit as st
import pyrebase
from openai import OpenAI
import base64

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="DeepTrace", page_icon="🦖", layout="centered")

# --- 2. DESIGN MOBILE-FIRST (ZŁOTO I CZIEŃ) ---
st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at top, #1a1a1a, #000000) !important; 
        color: #ffffff !important; 
    }
    .stChatMessage, .stChatMessage div, .stChatMessage p {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }
    .main-title { 
        font-family: 'Inter', sans-serif; 
        font-size: clamp(1.8rem, 10vw, 3.5rem);
        background: linear-gradient(180deg, #fbbf24, #d97706); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        text-align: center; 
        font-weight: 900;
        margin-bottom: 15px; 
    }
    [data-testid="stChatMessageAssistant"] {
        background-color: #111111 !important;
        border: 1px solid #d97706 !important;
        border-radius: 15px !important;
    }
    [data-testid="stChatMessageUser"] {
        background-color: #262626 !important;
        border: 1px solid #444444 !important;
        border-radius: 15px !important;
    }
    .stButton>button { 
        width: 100%; 
        background: #fbbf24 !important; 
        color: #000000 !important; 
        border: none !important;
        border-radius: 12px !important; 
        font-weight: 800 !important;
        height: 50px !important;
    }
    .stChatInput textarea {
        color: #ffffff !important;
        background-color: #1a1a1a !important;
        border: 1px solid #333 !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KONFIGURACJA FIREBASE ---
firebase_config = {
    "apiKey": "AIzaSyA_3uiR7tjzhh8RV34UXhSf4e1fgfQV4Hs",
    "authDomain": "eduai-pl.firebaseapp.com",
    "projectId": "eduai-pl",
    "storageBucket": "eduai-pl.firebasestorage.app",
    "messagingSenderId": "197620737284",
    "appId": "1:197620737284:web:406ed906d7e0194d4bdc51",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

if "user" not in st.session_state:
    st.session_state.user = None

# --- 4. LOGIKA AUTORYZACJI ---
if st.session_state.user is None:
    st.markdown('<h1 class="main-title">DEEPTRACE ALPHA</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Logowanie", "Rejestracja"])
    
    with tab1:
        email_log = st.text_input("E-mail", key="log_email")
        pass_log = st.text_input("Hasło", type="password", key="log_pass")
        if st.button("ZALOGUJ"):
            try:
                user = auth.sign_in_with_email_and_password(email_log, pass_log)
                st.session_state.user = user
                st.rerun()
            except:
                st.error("Błędne dane logowania.")
                
    with tab2:
        st.write("Użyj e-maila z zakupu na Naffy:")
        email_reg = st.text_input("E-mail", key="reg_email")
        pass_reg = st.text_input("Wymyśl hasło (min. 6 znaków)", type="password", key="reg_pass")
        if st.button("STWÓRZ KONTO"):
            try:
                auth.create_user_with_email_and_password(email_reg, pass_reg)
                st.success("Konto stworzone! Możesz się teraz zalogować w zakładce obok.")
            except Exception as e:
                st.error(f"Błąd: {e}")

else:
    # --- 5. INTERFEJS CZATU (ZALOGOWANY) ---
    st.sidebar.markdown("<h1 style='color: #fbbf24;'>🦖 EduAI PRO</h1>", unsafe_allow_html=True)
    st.sidebar.info(f"Aktywny: {st.session_state.user['email']}")
    
    if st.sidebar.button("Wyloguj"):
        st.session_state.user = None
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
            with st.spinner("DeepTrace analizuje..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": "Jesteś Architektem EduAI DeepTrace. Bądź luksusowy, mądry i konkretny."}] + st.session_state.chat_history
                    )
                    res = response.choices[0].message.content
                    st.markdown(res)
                    st.session_state.chat_history.append({"role": "assistant", "content": res})
                except Exception as e:
                    st.error(f"Błąd techniczny: {e}")
