import streamlit as st
from openai import OpenAI
import firebase_admin
from firebase_admin import credentials, auth

# Sprawdzenie, czy Firebase już działa, żeby nie wywaliło błędu przy odświeżaniu
if not firebase_admin._apps:
    # Tutaj docelowo wrzucimy Twoje klucze, ale na razie chcemy, żeby aplikacja WSTAŁA
    pass 

st.title("EduAI DeepTrace - System Aktywny")
st.write("Jeśli to widzisz, to znaczy, że pokonaliśmy błąd instalacji!")

# --- 1. KONFIGURACJA STRONY (Musi być na samej górze!) ---
st.set_page_config(page_title="EduAI DeepTrace", page_icon="🦖", layout="centered")

# --- CUSTOM CSS DLA TELEFONU ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    .stApp { background: radial-gradient(circle at center, #1a1a1a, #050505); color: #e5e5e5; }
    .main-title { font-family: 'Georgia', serif; font-size: 3rem; background: linear-gradient(90deg, #fbbf24, #d97706, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    .stButton>button { width: 100%; height: 3em; background: transparent; color: #fbbf24 !important; border: 1px solid #fbbf24 !important; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Funkcja do obrazów
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

# --- 2. KONFIGURACJA FIREBASE ---
config = {
    "apiKey": "AIzaSyA_3uiR7tjzhh8RV34UXhSf4e1fgfQV4Hs",
    "authDomain": "eduai-pl.firebaseapp.com",
    "projectId": "eduai-pl",
    "storageBucket": "eduai-pl.firebasestorage.app",
    "messagingSenderId": "197620737284",
    "appId": "1:197620737284:web:406ed906d7e0194d4bdc51"
}

# ODPALAMY LOGOWANIE
user_data = firebase_auth(config)

if user_data:
    # --- 3. GŁÓWNA LOGIKA PO ZALOGOWANIU ---
    st.sidebar.markdown("<h1 style='color: #fbbf24;'>🦖 EduAI PRO</h1>", unsafe_allow_html=True)
    st.sidebar.success(f"Witaj!")
    
    # Przesyłanie obrazów
    uploaded_file = st.sidebar.file_uploader("🖼️ Prześlij notatki", type=["jpg", "png", "jpeg"])

    # Zarządzanie sesją czatu
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

    # Czat
    if prompt := st.chat_input("Zadaj pytanie DeepTrace..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("DeepTrace skanuje wzorce..."):
                try:
                    # Tutaj możesz dodać obsługę obrazu w user_content jeśli chcesz rozwinąć o wizję
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{
                            "role": "system",
                            "content": "Jesteś Architektem EduAI DeepTrace. Twoim celem jest optymalizacja ludzkiego intelektu. Analizuj błędy, nie podawaj gotowych odpowiedzi, zmuszaj do myślenia pytaniami sokratejskimi."
                        }] + st.session_state.chat_history
                    )
                    full_res = response.choices[0].message.content
                    st.markdown(full_res)
                    st.session_state.chat_history.append({"role": "assistant", "content": full_res})
                except Exception as e:
                    st.error(f"Problem techniczny: {e}")
else:
    # Widok dla niezalogowanego
    st.markdown('<h1 class="main-title">EduAI DeepTrace</h1>', unsafe_allow_html=True)
    st.warning("Zaloguj się panelem obok, aby wejść do systemu.")
