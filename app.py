import os
import streamlit as st
from google import genai

# Sayfa Yapılandırması
st.set_page_config(page_title="Yapay Zeka Koçum", page_icon="🤖", layout="centered")

st.title("🤖 Yapay Zeka Koçum")
st.write("Hedefine ulaşmak için buradayım kanki!")

# API ANAHTARIN (Google AI Studio'dan aldığın anahtar)
API_KEY = "AQ.Ab8RN6L6Qzu2nLNd9aumhpQpXy8CVG8M-R8yThy8LzxGLHl4ag"

if API_KEY == "AQ.Ab8RN6L6Qzu2nLNd9aumhpQpXy8CVG8M-R8yThy8LzxGLHl4ag":
    st.error("⚠️ Lütfen koddaki 'BURAYA_API_ANAHTARINI_YAZ' kısmına kendi Google Gemini API anahtarını yapıştır!")
else:
    try:
        # Yeni ve hatasız istemci başlatma yöntemi
        client = genai.Client(api_key=API_KEY)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Sohbet Geçmişini Ekrana Yazdır
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Kullanıcı Girişi
        if prompt := st.chat_input("Bir şeyler sor..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # Yeni SDK ile model çağrısı
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Hata oluştu: {e}")
