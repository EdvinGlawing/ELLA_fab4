import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Edvin - Brottsbalken", page_icon="⚖️", layout="centered")

st.markdown("# ⚖️ Välkommen till Edvin")
st.markdown("### Din AI-guide genom Brottsbalken")

st.markdown("""
Edvin hjälper dig att snabbt hitta relevant information i **Brottsbalken (BrB)**.  
Ställ en fråga på vanlig svenska - Edvin söker igenom lagen och ger dig ett svar.
""")

col1, col2 = st.columns([1, 2])
with col1:
    image_path = Path(__file__).parent / "edvin_lagbok.png"
    if image_path.exists():
        st.image(str(image_path), width=1000)

with col2:
    st.markdown("""
    **Exempel på frågor du kan ställa:**
    - *Vad räknas som grov misshandel?*
    - *Hur definieras bedrägeri i lagen?*
    - *Vad är straffet av förfalskning av ID?*
    """)

st.info("⚠️ Edvin ersätter inte juridisk rådgivning. Konsultera alltid en jurist vid behov.")

if st.button("💬 Gå till chatboten →", type="primary"):
    st.switch_page("pages/1_Chatbot.py")