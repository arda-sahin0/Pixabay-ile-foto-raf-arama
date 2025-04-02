import streamlit as st
import requests
from PIL import Image
from io import BytesIO

API_KEY = "49631544-8162acdec9dab50e4506e6623"
BASE_URL = "https://pixabay.com/api/"

KATEGORILER = {
    "Tümü": "all",
    "Doğa": "nature",
    "Bilim": "science",
    "Eğitim": "education",
    "İnsanlar": "people",
    "Hayvanlar": "animals",
    "Seyahat": "travel"
}

RENKLER = {
    "Tümü": "all",
    "Kırmızı": "red",
    "Mavi": "blue",
    "Yeşil": "green",
    "Sarı": "yellow",
    "Siyah": "black",
    "Beyaz": "white"
}

st.title("Pixabay Görsel Arama ve İndirme")
query = st.text_input("Aranacak kelime:", "")
kategori_turkce = st.selectbox("Kategori Seçin:", list(KATEGORILER.keys()))
renk_turkce = st.selectbox("Renk Seçin:", list(RENKLER.keys()))
safe_search = st.checkbox("Güvenli Arama (Yetişkin İçeriği Gizle)", value=True)

kategori = KATEGORILER[kategori_turkce]
renk = RENKLER[renk_turkce]

if st.button("Ara"):
    params = {
        "key": API_KEY,
        "q": query,
        "category": kategori if kategori != "all" else "",
        "colors": renk if renk != "all" else "",
        "safesearch": str(safe_search).lower(),
        "per_page": 20
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "hits" in data:
        for image_data in data["hits"]:
            image_url = image_data["webformatURL"]
            st.image(image_url, caption=f'ID: {image_data["id"]}', use_container_width=True)
            st.markdown(f'[Görseli İndir]({image_url})', unsafe_allow_html=True)
    else:
        st.error("Sonuç bulunamadı.")