import streamlit as st
from openai import OpenAI

# 1. KONFIGURACJA STRONY
st.set_page_config(page_title="EduAI DeepTrace", page_icon="🦖", layout="centered")

# 2. TYMCZASOWE LOGOWANIE (Bez psujących się bibliotek)
# Skoro Firebase sprawia problemy techniczne, zrobimy proste hasło, 
# żebyś mógł DZISIAJ zacząć testować.
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 EduAI DeepTrace - Autoryzacja")
    password = st.text_input("Podaj hasło dostępowe:", type="password")
    if st.button("Wejdź do systemu"):
        if password == "rum2026": # Twoje hasło z poprzedniego kodu
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Błędne hasło.")
else:
    # --- TUTAJ ZACZYNA SIĘ TWÓJ CAŁY SYSTEM ---
    st.title("🦖 EduAI DeepTrace - System Aktywny")
    
    # Konfiguracja klienta OpenAI (Groq)
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["GROQ_API_KEY"]
    )

    # Prosty czat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Zadaj pytanie DeepTrace..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Jesteś Architektem EduAI DeepTrace. Pomagaj użytkownikowi optymalizować intelekt."}] + st.session_state.messages
            )
            res = response.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
