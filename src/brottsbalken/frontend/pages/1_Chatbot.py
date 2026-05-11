import streamlit as st
import httpx
from pathlib import Path
from utils import speak_text, API_URL

st.set_page_config(page_title="Chatbot - Edvin", page_icon="💬", layout="centered")

st.markdown('<p style="font-size: 30px; color: lightblue;">Fråga Brottsbalken om du gjort något sus 👮‍♂️</p>', unsafe_allow_html=True)

if "current_question" not in st.session_state:
    st.session_state.current_question = ""
if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""

def handle_submit():
    if st.session_state.widget_input.strip():
        st.session_state.current_question = st.session_state.widget_input
        st.session_state.widget_input = ""
        st.session_state.last_answer = ""

st.text_input("Skriv din fråga här", key="widget_input", on_change=handle_submit)

if st.button("Fråga Edvin"):
    if st.session_state.widget_input.strip():
        handle_submit()
        st.rerun()

if st.session_state.current_question and not st.session_state.last_answer:
    image_placeholder = st.empty()
    with st.spinner("Edvin söker i Brottsbalken..."):
        image_path = Path(__file__).parent.parent / "Edvin.png"
        if image_path.exists():
            image_placeholder.image(str(image_path), caption="Edvin letar svar...", width=250)
        try:
            response = httpx.post(API_URL, json={"prompt": st.session_state.current_question}, timeout=30)
            st.session_state.last_answer = response.json()["answer"]
            image_placeholder.empty()
            st.rerun()
        except Exception as e:
            image_placeholder.empty()
            st.error(f"Kunde inte hämta svar: {e}")

if st.session_state.last_answer:
    st.markdown("---")
    st.markdown(f"### Fråga:\n{st.session_state.current_question}")
    st.markdown(f"### Svar:\n{st.session_state.last_answer}")
    if st.button("🔊 Läs upp svar"):
        speak_text(st.session_state.last_answer)