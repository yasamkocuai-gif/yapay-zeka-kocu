import streamlit as st
import google.generativeai as genai

# Sayfa Yapılandırması ve Geniş Mod (Yan menü ve arayüzün tam oturması için)
st.set_page_config(
    page_title="Yapay Zeka Koçum", 
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# API Anahtarını doğrudan tanımlıyoruz (401 hatasını bitiren kesin çözüm)
API_KEY = "AQ.Ab8RN6KRexcrYqSo9LJDDyUTgR4MWlRdSC66l5RBgf5IGLqR2w"

# Google Gemini Yapılandırması
genai.configure(api_key=API_KEY)

# Arayüz Başlığı
st.title("🤖 Yapay Zeka Koçum")
st.write("Hedefine ulaşmak için buradayım kanki, sorunu sor!")

try:
    # Kararlı ve hatasız model tanımı
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Sohbet geçmişi yönetimi
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Geçmiş mesajları ekranda tut
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Kullanıcıdan mesaj al
    if prompt := st.chat_input("Bugün ne çalışıyoruz?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Sohbet oturumu başlat ve yanıt al
            chat = model.start_chat(history=[
                {"role": m["role"] if m["role"] != "assistant" else "model", "parts": [m["content"]]} 
                for m in st.session_state.messages[:-1]
            ])
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"Bir hata oluştu: {e}")
