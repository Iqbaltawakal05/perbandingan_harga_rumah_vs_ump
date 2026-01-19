# Perbandingan Harga Rumah dengan UMP di Indonesia

Aplikasi berbasis **Streamlit** untuk menganalisis perbandingan harga rumah
dengan **Upah Minimum Provinsi (UMP)** di Indonesia, guna melihat tingkat
keterjangkauan hunian di berbagai wilayah.


## 🎯 Tujuan
- Menganalisis perbandingan harga rumah terhadap UMP
- Menyajikan data dalam bentuk grafik dan peta (GIS)
- Memberikan visualisasi yang mudah dipahami


## 📊 Sumber Data
- **Harga Rumah**: hasil web scraping dari situs properti
- **UMP**: data resmi Upah Minimum Provinsi Indonesia


## 🔄 Alur Pengolahan Data
1. **Scraping** – pengambilan data harga rumah
2. **Cleaning & Preprocessing** – pembersihan dan standarisasi data
3. **Analisis** – perbandingan harga rumah dengan UMP
4. **Visualisasi** – grafik dan tabel
5. **GIS** – peta keterjangkauan rumah
6. **Streamlit** – penyajian aplikasi interaktif

## ▶️ Cara Menjalankan Aplikasi
```bash
pip install -r requirements.txt
streamlit run app.py