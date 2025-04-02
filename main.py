import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv("apikey.env")

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

if not PIXABAY_API_KEY or not DEEPL_API_KEY:
    st.error("API anahtarları eksik! Lütfen .env dosyanızı kontrol edin.")
    st.stop()


def translate_to_english(text):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": "EN"
    }
    response = requests.post(url, data=params)
    result = response.json()

    if "translations" in result:
        return result["translations"][0]["text"]
    else:
        return None


st.title("Pixabay Görsel Arama ve İndirme")

query_turkce = st.text_input("Aranacak kelime:", "güneş batımı")

if query_turkce:
    query = translate_to_english(query_turkce)
    if not query:
        st.error("Çeviri başarısız oldu!")
        st.stop()
else:
    query = ""

st.write(f"İngilizce Çeviri: {query}")  # Debug için

KATEGORILER = {
    "Tümü": "all", "Doğa": "nature", "Bilim": "science",
    "Eğitim": "education", "İnsanlar": "people", "Hayvanlar": "animals", "Seyahat": "travel"
}

RENKLER = {
    "Tümü": "all", "Kırmızı": "red", "Mavi": "blue",
    "Yeşil": "green", "Sarı": "yellow", "Siyah": "black", "Beyaz": "white"
}

kategori_turkce = st.selectbox("Kategori Seçin:", list(KATEGORILER.keys()))
renk_turkce = st.selectbox("Renk Seçin:", list(RENKLER.keys()))
safe_search = st.checkbox("Güvenli Arama (Yetişkin İçeriği Gizle)", value=True)

kategori = KATEGORILER[kategori_turkce]
renk = RENKLER[renk_turkce]

if st.button("Ara") and query:
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "category": kategori if kategori != "all" else "",
        "colors": renk if renk != "all" else "",
        "safesearch": str(safe_search).lower(),
        "per_page": 10
    }

    response = requests.get("https://pixabay.com/api/", params=params)
    data = response.json()

    if "hits" in data:
        for image_data in data["hits"]:
            image_url = image_data["webformatURL"]
            st.image(image_url, caption=f'ID: {image_data["id"]}', use_container_width=True)
            st.markdown(f'[Görseli İndir]({image_url})', unsafe_allow_html=True)
    else:
        st.error("Sonuç bulunamadı.")
