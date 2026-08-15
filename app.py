import streamlit as st
import google.generativeai as genai

# Sayfa Yapılandırması
st.set_page_config(page_title="Yapay Zeka Koçum", page_icon="🤖", layout="centered")

st.title("🤖 Yapay Zeka Koçum")
st.write("Hedefine ulaşmak için buradayım kanki!")

# API ANAHTARIN (Google AI Studio'dan aldığın o uzun kod)
# Lütfen tırnakları silmeden kendi anahtarını buraya yapıştır:
API_KEY = "AQ.Ab8RN6KRexcrYqSo9LJDDyUTgR4MWlRdSC66l5RBgf5IGLqR2w"

if API_KEY == "AQ.Ab8RN6L6Qzu2nLNd9aumhpQpXy8CVG8M-R8yThy8LzxGLHl4ag":
    st.error("⚠️ API anahtarını koddaki tırnakların arasına yapıştırmamışsın! Lütfen düzenle.")
else:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Sohbet Geçmişi
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Kullanıcı Girişi
        if prompt := st.chat_input("Bir şeyler sor..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # Mesajı gönder
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Hata oluştu: {e}")
