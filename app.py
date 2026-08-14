import streamlit as st
import google.generativeai as genai

# --- Sayfa Yapılandırması ---
st.set_page_config(
    page_title="Yapay Zeka Koçum",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Güvenli Yapılandırma ---
API_KEY = "AQ.Ab8RN6KrahxjyF4-Sy6e9d2UC9sQLascPALWdMQ-3TctNUH5Iw"

try:
    genai.configure(api_key=API_KEY)
except Exception:
    pass

# --- Oturum Durumu (State) Başlatma ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "isim": "Ömercan", 
        "hedef": "YKS / Tıp", 
        "seviye": "Orta"
    }

# --- Sol Panel (Sidebar) ---
with st.sidebar:
    st.markdown("### 🎨 Tema Seçimi")
    secilen_tema = st.selectbox(
        "Arayüz Teması:", 
        ["Mat Siyah (Dark)", "Neon Gece (Cyberpunk)", "Temiz Beyaz (Light)"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 👤 Kullanıcı Profili")
    isim_input = st.text_input("Adın:", value=st.session_state.user_profile["isim"])
    hedef_input = st.text_input("Hedefin:", value=st.session_state.user_profile["hedef"])
    seviye_input = st.selectbox("Seviyen:", ["Başlangıç", "Orta", "İleri"], index=1)
    
    if st.button("Bilgileri Kaydet"):
        st.session_state.user_profile.update({
            "isim": isim_input, 
            "hedef": hedef_input, 
            "seviye": seviye_input
        })
        st.success("Profil güncellendi!")
    
    st.markdown("---")
    secim = st.sidebar.radio("Mod Seçimi:", [
        "💬 Serbest Sohbet", 
        "📚 Ders & Eğitim", 
        "🏋️ Spor & Egzersiz", 
        "🧠 Psikoloji & Rüyalar", 
        "📅 Akıllı Planlayıcı", 
        "🎨 Görsel Oluşturma", 
        "🔊 Ses Oluşturma"
    ])

# --- Tema Renk Paletleri ---
if secilen_tema == "Mat Siyah (Dark)":
    bg_color, sidebar_bg, text_color, user_bg, ai_bg, border_color = "#0e1117", "#161b22", "#e6edf3", "#1f6feb", "#21262d", "#30363d"
elif secilen_tema == "Neon Gece (Cyberpunk)":
    bg_color, sidebar_bg, text_color, user_bg, ai_bg, border_color = "#0b0c10", "#1f2833", "#66fcf1", "#45a29e", "#1f2833", "#c5c6c7"
else: 
    bg_color, sidebar_bg, text_color, user_bg, ai_bg, border_color = "#ffffff", "#f0f2f6", "#262730", "#0066cc", "#f1f3f6", "#d1d5db"

# --- CSS Enjeksiyonu ---
st.markdown(f"""
<style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    [data-testid='stSidebar'] {{ background-color: {sidebar_bg}; border-right: 1px solid {border_color}; }}
    .user-msg {{
        background-color: {user_bg}; color: white; padding: 12px 16px;
        border-radius: 12px 12px 2px 12px; margin: 8px 0; max-width: 80%;
        margin-left: auto; text-align: right; font-family: sans-serif;
    }}
    .ai-msg {{
        background-color: {ai_bg}; color: {text_color}; padding: 12px 16px;
        border-radius: 12px 12px 12px 2px; margin: 8px 0; max-width: 80%;
        border: 1px solid {border_color}; font-family: sans-serif;
    }}
    .stButton>button {{
        background-color: #238636; color: white; border-radius: 8px; border: none; font-weight: bold;
    }}
    .stButton>button:hover {{ background-color: #2ea043; }}
</style>
""", unsafe_allow_html=True)

# --- Kesin Çözüm: Otomatik Çalışan Model Bulucu ---
def ai_yanit_al(prompt):
    try:
        # SDK üzerinden desteklenen tüm modelleri dinamik olarak listeler ve generateContent destekleyeni seçer
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                try:
                    model_isim = m.name.replace("models/", "")
                    model = genai.GenerativeModel(model_isim)
                    response = model.generate_content(prompt)
                    if response and hasattr(response, "text") and response.text:
                        return response.text
                except Exception:
                    continue
    except Exception as e:
        return f"⚠️ API Bağlantı Hatası: {str(e)}"
        
    return "⚠️ Hata: Hesabınızda içerik üretimine uygun model bulunamadı."

# --- Ana Ekran Başlığı ---
st.title("🤖 Yapay Zeka Kişisel Koçum")
profil = st.session_state.user_profile
st.caption(f"Aktif Kullanıcı: **{profil['isim']}** | Hedef: **{profil['hedef']}** | Seviye: **{profil['seviye']}**")
st.markdown("---")

# --- 1. Serbest Sohbet ---
if secim == "💬 Serbest Sohbet":
    st.subheader("💬 Koçunla Genel Sohbet")
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg"><b>{profil["isim"]}:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-msg"><b>Koç:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
            
    user_input = st.chat_input("Genel koçuna bir şeyler yaz...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.markdown(f'<div class="user-msg"><b>{profil["isim"]}:</b><br>{user_input}</div>', unsafe_allow_html=True)
        prompt = f"Kullanıcı: {profil['isim']}, Hedef: {profil['hedef']}, Seviye: {profil['seviye']}. Mesaj: {user_input}. Samimi, direkt ve profesyonel koç tarzında yanıt ver."
        with st.spinner("Koç düşünüyor..."):
            cevap = ai_yanit_al(prompt)
        st.session_state.messages.append({"role": "assistant", "content": cevap})
        st.rerun()

# --- 2. Ders & Eğitim ---
elif secim == "📚 Ders & Eğitim":
    st.subheader("📚 Akademik Eğitim & Ders Çalışma Alanı")
    col1, col2 = st.columns(2)
    with col1:
        ders = st.selectbox("Çalışılacak Ders:", ["Matematik", "Geometri", "Fizik", "Kimya", "Biyoloji", "Türkçe"])
    with col2:
        calisma_turu = st.selectbox("Çalışma Türü:", ["Konu Anlatımı & Özet", "Soru Çözüm Taktiği", "Hata Analizi", "Formül / Pratik Yol"])
        
    soru = st.text_area("Takıldığın soru metni veya anlamadığın konu:", height=130, placeholder="Örn: Limit sonsuzluk belirsizliğini L'Hopital olmadan nasıl çözerim?")
    
    if st.button("Ders Asistanına Çözdür", type="primary"):
        if soru:
            st.markdown(f'<div class="user-msg"><b>Soru / Konu:</b><br>{soru}</div>', unsafe_allow_html=True)
            with st.spinner(f"Uzman {ders} hocası inceliyor..."):
                prompt = f"Sen profesyonel bir {ders} öğretmenisin. Öğrencinin hedefi: {profil['hedef']}, Seviyesi: {profil['seviye']}. Çalışma türü: {calisma_turu}. Soru/Konu: {soru}. Konuyu net, anlaşılır ve adım adım açıkla. En sonda öğrenciyi test etmek için 2 tane pratik soru sor."
                cevap = ai_yanit_al(prompt)
                st.markdown(f'<div class="ai-msg"><b>{ders} Hocasının Yanıtı:</b><br>{cevap}</div>', unsafe_allow_html=True)
        else:
            st.warning("Lütfen bir soru veya konu belirt.")

# --- 3. Spor & Egzersiz ---
elif secim == "🏋️ Spor & Egzersiz":
    st.subheader("🏋️ Fitness & Beslenme Koçu")
    col1, col2 = st.columns(2)
    with col1:
        spor_hedefi = st.selectbox("Antrenman Hedefi:", ["Kilo Verme & Yağ Yakımı", "Kas Kazanımı (Hipertrofi)", "Güç & Dayanıklılık", "Formu Koruma"])
    with col2:
        ekipman = st.selectbox("Çalışma Alanı:", ["Ev (Ekipmansız)", "Ev (Dambıl/Direnç Bandı)", "Tam Donanımlı Spor Salonu (Gym)"])
        
    detay = st.text_area("Vücut durumun, günlük programın veya beslenme/suplement sorunun:", height=110, placeholder="Örn: Günlük 1 saatim var, kilo verip kas yapmak istiyorum...")
    
    if st.button("Antrenman Programı Oluştur", type="primary"):
        if detay:
            st.markdown(f'<div class="user-msg"><b>Antrenman İsteği:</b><br>{detay}</div>', unsafe_allow_html=True)
            with st.spinner("Pro Fitness Antrenörü program hazırlıyor..."):
                prompt = f"Sen sertifikalı profesyonel bir fitness koçu ve beslenme uzmanısın. Kullanıcı bilgileri -> Hedef: {spor_hedefi}, Alan: {ekipman}, Detay/Durum: {detay}. Kullanıcıya motive edici, nokta atışı bir antrenman ve beslenme tavsiyesi ver."
                cevap = ai_yanit_al(prompt)
                st.markdown(f'<div class="ai-msg"><b>Antrenörün Tavsiyesi:</b><br>{cevap}</div>', unsafe_allow_html=True)
        else:
            st.warning("Lütfen detay yaz kanki.")

# --- 4. Psikoloji & Rüyalar ---
elif secim == "🧠 Psikoloji & Rüyalar":
    st.subheader("🧠 Ruh Hali, Stres Yönetimi & Rüya Yorumcusu")
    kategori = st.selectbox("Paylaşım Türü:", ["Stres / Sınav Kaygısı", "Rüya Tabiri & Analizi", "Motivasyon Düşüklüğü", "Günlük İç Dökme"])
    metin = st.text_area("Aklındakileri veya gördüğün rüyayı detaylıca anlat:", height=120, placeholder="Örn: Sınav yaklaştıkça stresim artıyor, odaklanamıyorum...")
    
    if st.button("Analiz Et ve Tavsiye Al", type="primary"):
        if metin:
            st.markdown(f'<div class="user-msg"><b>Paylaşımın:</b><br>{metin}</div>', unsafe_allow_html=True)
            with st.spinner("Yaşam koçu empati kuruyor..."):
                prompt = f"Sen sakin, anlayışlı ve bilge bir yaşam koçu ve psikolojik danışmansın. Kategori: {kategori}. Kullanıcının hedefi: {profil['hedef']}. Kullanıcının mesajı: {metin}. Ona dostane, rahatlatıcı ve yapıcı tavsiyelerde bulun."
                cevap = ai_yanit_al(prompt)
                st.markdown(f'<div class="ai-msg"><b>Yaşam Koçunun Yanıtı:</b><br>{cevap}</div>', unsafe_allow_html=True)
        else:
            st.warning("Lütfen duygularını veya rüyanı yaz.")

# --- 5. Akıllı Planlayıcı ---
elif secim == "📅 Akıllı Planlayıcı":
    st.subheader("📅 Günlük / Haftalık Program Planlayıcı")
    gun_tipi = st.selectbox("Plan Türü:", ["Yoğun Çalışma Günü", "Dinlenme & Tekrar Günü", "Haftalık Genel Program"])
    p = st.text_area("Bugünkü ders/spor saatlerin veya müsaitlik durumun:", height=110, placeholder="Örn: Sabah 10:00'da başlıyorum, arada 1 saat spor/yemek molam var...")
    
    if st.button("Programı Oluştur", type="primary"):
        if p:
            st.markdown(f'<div class="user-msg"><b>Müsaitlik:</b><br>{p}</div>', unsafe_allow_html=True)
            with st.spinner("Planlayıcı saatleri ayarlıyor..."):
                prompt = f"Sen profesyonel bir zaman ve eğitim planlayıcısısın. Hedef: {profil['hedef']}, Plan Türü: {gun_tipi}, Bilgi: {p}. Saat saat verimli, uygulanabilir ve sürdürülebilir bir program hazırla."
                cevap = ai_yanit_al(prompt)
                st.markdown(f'<div class="ai-msg"><b>Özel Programın:</b><br>{cevap}</div>', unsafe_allow_html=True)
        else:
            st.warning("Lütfen saatlerini yaz.")

# --- 6. Görsel Oluşturma ---
elif secim == "🎨 Görsel Oluşturma":
    st.subheader("🎨 Midjourney / AI Görsel Prompt Üreticisi")
    tarz = st.selectbox("Görsel Tarzı:", ["Sinematik / Gerçekçi", "Cyberpunk / Neon", "Minimalist / Flat", "Anime / Manga"])
    g = st.text_area("Hayalindeki görseli Türkçe anlat:", height=110, placeholder="Örn: Geleceğin tıp laboratuvarında çalışan akıllı robot...")
    
    if st.button("Profesyonel Prompt Üret", type="primary"):
        if g:
            st.markdown(f'<div class="user-msg"><b>İstek:</b><br>{g}</div>', unsafe_allow_html=True)
            with st.spinner("Görsel sanatlar koçu prompt yazıyor..."):
                prompt = f"Sen uzman bir AI görsel sanatlar ve Midjourney prompt mühendisisin. Tarz: {tarz}. Kullanıcının fikri: {g}. Bu fikri İngilizce olarak en kaliteli, detaylı ve estetik Midjourney prompt haline getir ve kullanım ipuçları ekle."
                cevap = ai_yanit_al(prompt)
                st.markdown(f'<div class="ai-msg"><b>Görsel Promptun:</b><br>{cevap}</div>', unsafe_allow_html=True)
        else:
            st.warning("Lütfen görseli tarif et.")

# --- 7. Ses Oluşturma ---
elif secim == "🔊 Ses Oluşturma":
    st.subheader("🔊 Dış Ses & Sunum Metni Düzenleyici")
    ses_tipi = st.selectbox("Metin Amacı:", ["YouTube Video Girişi", "Ders Sunumu / Podcast", "Motivasyon / Reklam Metni"])
    s = st.text_area("Seslendirilmesini istediğin ham metin:", height=110, placeholder="Örn: Arkadaşlar bugün sizlerle YKS hazırlık sürecinde...")
    
    if st.button("Metni Dış Sese Uyarla", type="primary"):
        if s:
            st.markdown(f'<div class="user-msg"><b>Ham Metin:</b><br>{s}</div>', unsafe_allow_html=True)
            with st.spinner("Ses yönetmeni metni parlatıyor..."):
                prompt = f"Sen profesyonel bir seslendirme yönetmeni ve YouTube metin yazarısın. Amacın: {ses_tipi}. Ham metin: {s}. Bu metni vurgular, duraksama [nefes] komutları ve heyecan tonları ekleyerek seslendirmeye hazır kusursuz bir senaryoya dönüştür."
                cevap = ai_yanit_al(prompt)
                st.markdown(f'<div class="ai-msg"><b>Ses Senaryon:</b><br>{cevap}</div>', unsafe_allow_html=True)
        else:
            st.warning("Lütfen metin gir kanki.")