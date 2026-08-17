import streamlit as st
import requests
import json

# Sayfa Yapılandırması ve Yan Menü Ayarı
st.set_page_config(
    page_title="Yapay Zeka Koçum", 
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🤖 Yapay Zeka Koçum")
st.write("Hedefine ulaşmak için buradayım kanki!")

# Senin anahtarın
API_KEY = "AQ.Ab8RN6KRexcrYqSo9LJDDyUTgR4MWlRdSC66l5RBgf5IGLqR2w"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmiş mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan mesaj al
if prompt := st.chat_input("Bugün ne çalışıyoruz?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Doğrudan Google Generative Language REST API uç noktası (SDK hatalarını bypass eder)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            
            headers = {'Content-Type': 'application/json'}
            
            # Sohbet geçmişini API formatına dönüştür
            contents = []
            for m in st.session_state.messages:
                role = "user" if m["role"] == "user" else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": m["content"]}]
                })
            
            payload = {"contents": contents}
            
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            res_json = response.json()
            
            if response.status_code == 200:
                bot_reply = res_json['candidates'][0]['content']['parts'][0]['text']
                st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            else:
                error_msg = res_json.get('error', {}).get('message', 'Bilinmeyen hata')
                st.error(f"API Hatası: {error_msg}")
                
        except Exception as e:
            st.error(f"Bağlantı hatası: {e}")
