import streamlit as st
import httpx
import os 
from pathlib import Path

# Inställningar för API
API_URL = os.getenv("API_URL", "http://localhost:8000/rag/query")

def speak_text(text):
    """Läs upp texten via webbläsaren."""
    if text:
        clean_text = text.replace('"', "'").replace('\n', ' ')
        js_code = f"""
            <script>
            var msg = new SpeechSynthesisUtterance("{clean_text}");
            msg.lang = 'sv-SE';
            window.speechSynthesis.speak(msg);
            </script>
        """
        st.components.v1.html(js_code, height=0)

def handle_submit():
    """Hanterar inskickad fråga."""
    if st.session_state.widget_input.strip() != "":
        st.session_state.current_question = st.session_state.widget_input
        st.session_state.widget_input = ""
        st.session_state.last_answer = ""
        # Vi sätter en flagga för att veta att det är en ny fråga som ska läsas upp
        st.session_state.should_speak = True

def layout(): 
    st.markdown('<p style="font-size: 30px; color: lightblue;">Fråga Brottsbalken om du gjort något sus 👮‍♂️</p>', unsafe_allow_html=True)
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = ""
    if "last_answer" not in st.session_state:
        st.session_state.last_answer = ""
    if "should_speak" not in st.session_state:
        st.session_state.should_speak = False

    st.text_input(label="Skriv din fråga här", key="widget_input", on_change=handle_submit)

    if st.button("Fråga Edvin"):
        if st.session_state.widget_input.strip() != "":
            handle_submit()
            st.rerun()

    # Logik för laddning (Bild + API)
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

    # Visa resultatet OCH kör rösten
    if st.session_state.last_answer:
        st.markdown("---")
        st.markdown(f"### Fråga:\n{st.session_state.current_question}")
        st.markdown(f"### Svar:\n{st.session_state.last_answer}")
        
        # Kör rösten bara en gång per svar
        if st.session_state.should_speak:
            speak_text(st.session_state.last_answer)
            st.session_state.should_speak = False

if __name__ == "__main__":
    layout()
