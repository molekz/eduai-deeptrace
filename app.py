import streamlit as st
import streamlit_authenticator as stauth
from openai import OpenAI
import uuid
import base64

# --- 1. KONFIGURACJA STRONY ---
if "page_config_set" not in st.session_state:
    st.set_page_config(page_title="EduAI DeepTrace", page_icon="🦖", layout="wide")
    st.session_state.page_config_set = True

# Funkcja do czytania obrazu przez AI
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

# --- 2. SYSTEM LOGOWANIA ---
credentials = {
    "usernames": {
        "klient1": {
            "name": "Klient Premium",
            "password": "rum2026"
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "eduai_cookie",
    "signature_key",
    cookie_expiry_days=30
)

authenticator.login(key='Login_Form_Unique')

# --- 3. STATUS PREMIUM ---
is_premium = False
if st.session_state.get("authentication_status"):
    is_premium = True # Zalogowany = Automatycznie Premium

# --- 4. GŁÓWNA LOGIKA EDUAI ---
if st.session_state.get("authentication_status"):
    
    # Stylizacja Jurassic
    st.markdown("""
        <style>
        .stApp { background: radial-gradient(circle at center, #1a1a1a, #050505); color: #e5e5e5; }
        [data-testid="stSidebar"] { background-color: #0a0a0a !important; border-right: 2px solid #fbbf24; }
        .main-title { font-family: 'Georgia', serif; font-size: 3.5rem; background: linear-gradient(90deg, #fbbf24, #d97706, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 20px; }
        .stButton>button { width: 100%; background: transparent; color: #fbbf24 !important; border: 1px solid #fbbf24 !important; border-radius: 4px; font-weight: bold; }
        .stButton>button:hover { background: #fbbf24 !important; color: #000 !important; box-shadow: 0 0 20px rgba(251, 191, 36, 0.4); }
        </style>
        """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.markdown("<h1 style='color: #fbbf24;'>🦖 EduAI PRO</h1>", unsafe_allow_html=True)
    st.sidebar.success(f"Witaj {st.session_state['name']}!")
    
    # NOWOŚĆ: Przesyłanie obrazów do DeepTrace
    uploaded_file = st.sidebar.file_uploader("🖼️ Prześlij notatki do analizy", type=["jpg", "png", "jpeg"])
    
    authenticator.logout('Wyloguj', 'sidebar')

    # Zarządzanie sesją
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {"DeepTrace Alpha": []}
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = "DeepTrace Alpha"

    client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=st.secrets["GROQ_API_KEY"] # TO JEST BEZPIECZNE
)

    st.markdown(f'<h1 class="main-title">{st.session_state.current_chat}</h1>', unsafe_allow_html=True)
    messages = st.session_state.chat_history.get(st.session_state.current_chat, [])
    
    for msg in messages:
        with st.chat_message(msg["role"]):
            # Obsługa wyświetlania historii z obrazami
            if isinstance(msg["content"], list):
                st.markdown(msg["content"][0]["text"])
            else:
                st.markdown(msg["content"])

    if prompt := st.chat_input("Zadaj pytanie DeepTrace..."):
        # Przygotowanie promptu (tekst + opcjonalnie obraz)
        user_content = [{"type": "text", "text": prompt}]
        
        if uploaded_file:
            base64_image = encode_image(uploaded_file)
            user_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            })

        messages.append({"role": "user", "content": user_content})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("DeepTrace skanuje wzorce błędów..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.2-90b-vision-preview",
                        messages=[{
                            "role": "system",
                            "content": "Jesteś Architektem EduAI DeepTrace. Twoim celem jest optymalizacja ludzkiego intelektu. Analizuj błędy na zdjęciach i w tekście, nie podawaj gotowych odpowiedzi, zmuszaj do myślenia sokratejskimi pytaniami. Bądź wizjonerski i luksusowy w komunikacji."
                        }] + messages
                    )
                    full_res = response.choices[0].message.content
                    st.markdown(full_res)
                    messages.append({"role": "assistant", "content": full_res})
                    st.session_state.chat_history[st.session_state.current_chat] = messages
                except Exception as e:
                    st.error(f"Problem techniczny: {e}")

elif st.session_state.get("authentication_status") is False:
    st.error('Błędny login lub hasło')
elif st.session_state.get("authentication_status") is None:
    st.warning('Zaloguj się, aby zacząć budować swoje imperium.')