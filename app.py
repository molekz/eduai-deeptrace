import streamlit as st
from openai import OpenAI
import base64

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="DeepTrace", page_icon="🦖", layout="centered")

# --- 2. TWÓJ LUKSUSOWY CSS ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    .stApp { background: radial-gradient(circle at center, #1a1a1a, #050505); color: #e5e5e5; }
    [data-testid="stSidebar"] { background-color: #0a0a0a !important; border-right: 2px solid #fbbf24; }
    .main-title { font-family: 'Georgia', serif; font-size: 3.5rem; background: linear-gradient(90deg, #fbbf24, #d97706, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 20px; }
    .stButton>button { width: 100%; height: 3em; background: transparent; color: #fbbf24 !important; border: 1px solid #fbbf24 !important; border-radius: 10px; font-weight: bold; }
    .stButton>button:hover { background: #fbbf24 !important; color: #000 !important; box-shadow: 0 0 20px rgba(251, 191, 36, 0.4); }
    .stChatMessage { font-size: 14px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# Funkcja do obrazów
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

# --- 3. SYSTEM LOGOWANIA I REJESTRACJI (FIREBASE) ---
from streamlit_firebase import firebase_auth

config = {
    "apiKey": "AIzaSyA_3uiR7tjzhh8RV34UXhSf4e1fgfQV4Hs",
    "authDomain": "eduai-pl.firebaseapp.com",
    "projectId": "eduai-pl",
    "storageBucket": "eduai-pl.firebasestorage.app",
    "messagingSenderId": "197620737284",
    "appId": "1:197620737284:web:406ed906d7e0194d4bdc51"
}

# Wyświetla formularz logowania/rejestracji
user_data = firebase_auth(config)

if user_data:
    # --- 4. GŁÓWNA LOGIKA EDUAI PO ZALOGOWANIU ---
    st.sidebar.markdown("<h1 style='color: #fbbf24;'>🦖 EduAI PRO</h1>", unsafe_allow_html=True)
    st.sidebar.success(f"Zalogowano: {user_data['email']}")
    
    if st.sidebar.button("Wyloguj"):
        # Firebase automatycznie obsłuży sesję, ale to odświeży stronę
        st.rerun()

    uploaded_file = st.sidebar.file_uploader("🖼️ Prześlij notatki do analizy", type=["jpg", "png", "jpeg"])

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["GROQ_API_KEY"]
    )

    st.markdown('<h1 class="main-title">DeepTrace Alpha</h1>', unsafe_allow_html=True)
    
    # Wyświetlanie historii
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Zadaj pytanie DeepTrace..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("DeepTrace skanuje wzorce błędów..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{
                            "role": "system",
                            "content": "Jesteś Architektem EduAI DeepTrace. Twoim celem jest optymalizacja ludzkiego intelektu. Analizuj błędy, zmuszaj do myślenia pytaniami sokratejskimi. Bądź wizjonerski i luksusowy."
                        }] + st.session_state.chat_history
                    )
                    full_res = response.choices[0].message.content
                    st.markdown(full_res)
                    st.session_state.chat_history.append({"role": "assistant", "content": full_res})
                except Exception as e:
                    st.error(f"Problem techniczny: {e}")
else:
    # Widok dla niezalogowanego
    st.markdown('<h1 class="main-title">DeepTrace Alpha</h1>', unsafe_allow_html=True)
    st.info("System wymaga autoryzacji. Zaloguj się lub załóż konto, aby kontynuować budowę imperium.")

    # --- 4. GŁÓWNA LOGIKA EDUAI (TWÓJ DESIGN) ---
    st.sidebar.markdown("<h1 style='color: #fbbf24;'>🦖 EduAI PRO</h1>", unsafe_allow_html=True)
    st.sidebar.success("Witaj w systemie, Architekcie!")
    
    if st.sidebar.button("Wyloguj"):
        st.session_state.authenticated = False
        st.rerun()

    uploaded_file = st.sidebar.file_uploader("🖼️ Prześlij notatki do analizy", type=["jpg", "png", "jpeg"])

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["GROQ_API_KEY"]
    )

    st.markdown('<h1 class="main-title">DeepTrace Alpha</h1>', unsafe_allow_html=True)
    
    # Wyświetlanie historii
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Zadaj pytanie DeepTrace..."):
        user_content = [{"type": "text", "text": prompt}]
        
        if uploaded_file:
            base64_image = encode_image(uploaded_file)
            user_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            })

        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("DeepTrace skanuje wzorce błędów..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{
                            "role": "system",
                            "content": "Jesteś Architektem EduAI DeepTrace. Twoim celem jest optymalizacja ludzkiego intelektu. Analizuj błędy, zmuszaj do myślenia pytaniami sokratejskimi. Bądź wizjonerski i luksusowy."
                        }] + st.session_state.chat_history
                    )
                    full_res = response.choices[0].message.content
                    st.markdown(full_res)
                    st.session_state.chat_history.append({"role": "assistant", "content": full_res})
                except Exception as e:
                    st.error(f"Problem techniczny: {e}")
