import streamlit as st

st.set_page_config(page_title="Om tjänsten - Edvin", page_icon="ℹ️", layout="centered")

st.markdown("# ℹ️ Om Edvin")

st.markdown("""
## Vad är Edvin?
Edvin är en AI-driven chatbot som hjälper dig navigera i **Brottsbalken (1962:700)** - 
Sveriges centrala strafflag.

## Hur fungerar det?
Edvin använder **RAG (Retrieval-Augmented Generation)** - en teknik där AI:n söker 
i en kunskapsbas av lagtext och sedan formulerar ett svar baserat på den information den hittar.

## Datakällor
- Brottsbalken (SFS 1962:700), hämtad från [riksdagen.se](https://www.riksdagen.se)
- Senast uppdaterad: *4 maj 2026*

## Begränsningar
- Edvin kan göra fel - kontrollera alltid mot officiell lagtext
- Edvin tar inte hänsyn till praxis, förarbeten eller andra rättskällor
- Tjänsten är inte juridisk rådgivning

## Teknikstack
- **Frontend:** Streamlit
- **Backend:** FastAPI + RAG-pipeline
- **Röst:** ElevenLabs TTS
- **Hosting:** Azure (Docker)
""")

st.warning("⚠️ Edvin ersätter inte en jurist. Vid rättsliga frågor, kontakta alltid en kvalificerad juridisk rådgivare.")