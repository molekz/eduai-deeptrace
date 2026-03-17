import streamlit as st
from openai import OpenAI
import base64

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="DeepTrace", page_icon="🦖", layout="centered")

# --- 2. POPRAWIONY DESIGN MOBILE-FIRST ---
st.markdown("""
    <style>
    /* Usuwamy gigantyczne marginesy Streamlit na telefonie */
    .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }
    
    /* Tło z głębokim gradientem */
    .stApp { background: radial-gradient(circle at top, #1a1a1a, #000000); color: #e5e5e5; }
    
    /* Napis DeepTrace dopasowany do ekranu telefonu */
    .main-title { 
        font-family: 'Inter', sans-serif; 
        font-size: clamp(2rem, 8vw, 3.5rem); /* Skaluje się zależnie od ekranu */
        background: linear-gradient(180deg, #fbbf24, #d97706); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        text-align: center; 
        font-weight: 900;
        letter-spacing: -1px;
        margin-bottom: 10px; 
    }
    
    /* Naprawiamy wygląd inputów na mobile */
    .stTextInput>div>div>input {
        background-color: #121212 !important;
        color: #fbbf24 !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        height: 45px;
    }

    /* Luksusowy przycisk - pełna szerokość na telefonie */
    .stButton>button { 
        width: 100%; 
        background: #fbbf24 !important; 
        color: #000 !important; 
        border: none !important;
        border-radius: 12px !important; 
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        height: 50px !important;
        transition: 0.3s;
    }
    
    /* Ukrywamy zbędne elementy Streamlit, żeby nie było widać, że to darmowy hosting */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Styl bąbelków czatu - mniejsza czcionka na telefon */
    .stChatMessage { 
        background-color: #1a1a1a !important; 
        border: 1px solid #333 !important;
        border-radius: 15px !important;
        font-size: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIKA DOSTĘPU (NAFFY SYNC) ---
VIP_DATABASE = {
    "admin@eduai.pl": "RUM2026",
    "igorskubis1@gmail.com": "dinozaur",  # Dopisujesz siebie
    "klient@naffy.pl": "VIP-7788"
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
