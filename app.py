import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Yapay Zeka Koçum", page_icon="💪", layout="centered")

st.title("🤖 Yapay Zeka Koçum")
st.write("Hedefine ulaşmak için buradayım kanki, sorunu sor!")

# Şifreyi gizli kasadan (Streamlit Secrets) alıyoruz
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("⚠️ API anahtarı gizli kasada bulunamadı! Lütfen Streamlit ayarlarından ekle.")
    api_key = None

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Bugün ne çalışıyoruz veya ne soracaksın?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                formatted_history = [
                    {"role": m["role"] if m["role"] != "assistant" else "model", "parts": [m["content"]]} 
                    for m in st.session_state.messages[:-1]
                ]
                chat = model.start_chat(history=formatted_history)
                response = chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
