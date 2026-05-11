import re, base64, os
import streamlit as st
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
VOICE_ID = os.getenv("VOICE_ID", "")
API_URL = os.getenv("API_URL", "http://localhost:8000/rag/query")

eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def preprocess_law_text(text: str) -> str:
    text = re.sub(r'\b(\d+)\s*§', r'paragraf \1', text)
    text = re.sub(r'§\s*(\d+)', r'paragraf \1', text)
    return text.replace("§§", "paragrafer").replace("§", "paragraf").replace("kap.", "kapitel")

def speak_text(text):
    if not text:
        return
    try:
        clean_text = preprocess_law_text(text)
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