import streamlit as st
import httpx
import os
import re
import base64
from pathlib import Path
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000/rag/query")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "din-elevenlabs-nyckel")
VOICE_ID = os.getenv("VOICE_ID", "ditt-voice-id")

eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def preprocess_law_text(text: str) -> str:
    text = re.sub(r'\b(\d+)\s*§', r'paragraf \1', text)
    text = re.sub(r'§\s*(\d+)', r'paragraf \1', text)
    text = text.replace("§§", "paragrafer").replace("§", "paragraf").replace("kap.", "kapitel")
    return text

# ── ElevenLabs ────────────────────────────────────────────────────────────────

def speak_text(text):
    if not text:
        return
    try:
        clean_text = preprocess_law_text(text)  # 👈 förbehandla här
        audio_generator = eleven_client.text_to_speech.convert(
            voice_id=VOICE_ID,
            text=clean_text,
            model_id="eleven_multilingual_v2",
            voice_settings={"stability": 0.5, "similarity_boost": 0.75}
        )
        audio_bytes = b"".join(audio_generator)
        b64 = base64.b64encode(audio_bytes).decode()
        st.markdown(
            f'<audio autoplay controls><source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg"></audio>',
            unsafe_allow_html=True
        )
    except Exception as e:
        st.warning(f"Kunde inte läsa upp svaret: {e}")

# ── Streamlit-layout (oförändrad) ─────────────────────────────────────────────

def handle_submit():
    if st.session_state.widget_input.strip() != "":
        st.session_state.current_question = st.session_state.widget_input
        st.session_state.widget_input = ""
        st.session_state.last_answer = ""

def layout():
    st.markdown('<p style="font-size: 30px; color: lightblue;">Fråga Brottsbalken om du gjort något sus 👮‍♂️</p>', unsafe_allow_html=True)

    if "current_question" not in st.session_state:
        st.session_state.current_question = ""
    if "last_answer" not in st.session_state:
        st.session_state.last_answer = ""

    st.text_input(label="Skriv din fråga här", key="widget_input", on_change=handle_submit)

    if st.button("Fråga Edvin"):
        if st.session_state.widget_input.strip() != "":
            handle_submit()
            st.rerun()

    if st.session_state.current_question and not st.session_state.last_answer:
        image_placeholder = st.empty()
        with st.spinner('Edvin söker i Brottsbalken...'):
            image_path = Path(__file__).parent / "Edvin.png"
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

if __name__ == "__main__":
    layout()