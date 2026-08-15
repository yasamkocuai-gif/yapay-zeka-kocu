import streamlit as st
from google import genai

# Sayfa Yapılandırması
st.set_page_config(page_title="Yapay Zeka Koçum", page_icon="🤖", layout="centered")

st.title("🤖 Yapay Zeka Koçum")
st.write("Hedefine ulaşmak için buradayım kanki!")

# API Anahtarın doğrudan buraya işlendi
API_KEY = "AQ.Ab8RN6KRexcrYqSo9LJDDyUTgR4MWlRdSC66l5RBgf5IGLqR2w"

try:
    client = genai.Client(api_key=API_KEY)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Bir şeyler sor..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
except Exception as e:
    st.error(f"Hata oluştu: {e}")
