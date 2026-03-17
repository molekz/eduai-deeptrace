import streamlit as st
from openai import OpenAI
import base64

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="EduAI DeepTrace", page_icon="🦖", layout="centered")

# --- 2. TWÓJ LUKSUSOWY CSS ---
st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at center, #1a1a1a, #050505); 
        color: #e5e5e5; 
    }
    .main-title { 
        font-family: 'Georgia', serif; 
        font-size: 3.5rem; 
        background: linear-gradient(90deg, #fbbf24, #d97706, #fbbf24); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        text-align: center; 
        margin-bottom: 20px; 
    }
    .stButton>button { 
        width: 100%; 
        background: transparent; 
        color: #fbbf24 !important; 
        border: 1px solid #fbbf24 !important; 
        border-radius: 10px; 
        height: 3em;
        font-weight: bold;
    }
    .stButton>button:hover { 
        background: #fbbf24 !important; 
        color: #000 !important; 
        box-shadow: 0 0 20px rgba(251, 191, 36, 0.4); 
    }
    /* Stylizacja inputu */
    .stTextInput>div>div>input {
        background-color: #121212;
        color: #fbbf24;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BRAMKA DOSTĘPU (Zamiast Firebase) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<h1 class="main-title">DEEPTRACE ALPHA</h1>', unsafe_allow_html=True)
    st.write("Wprowadź klucz dostępu do swojego imperium:")
    
    password = st.text_input("PASSWORD", type="password", label_visibility="collapsed")
    
    if st.button("AUTORYZACJA"):
        if password == "rum2026":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Dostęp zabroniony. Nieprawidłowy klucz.")
else:
    # --- 4. GŁÓWNY INTERFEJS DEEPTRACE ---
    st.markdown('<h1 class="main-title">DeepTrace PRO</h1>', unsafe_allow_html=True)
    
    # Zarządzanie sesją
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Klient API
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["GROQ_API_KEY"]
    )

    # Wyświetlanie czatu
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Czat input
    if prompt := st.chat_input("Zadaj pytanie DeepTrace..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analizuję wzorce..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{
                            "role": "system", 
                            "content": "Jesteś Architektem EduAI DeepTrace. Twoim celem jest optymalizacja ludzkiego intelektu. Bądź wizjonerski i luksusowy w komunikacji."
                        }] + st.session_state.messages
                    )
                    res = response.choices[0].message.content
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                except Exception as e:
                    st.error(f"Błąd techniczny: {e}")
