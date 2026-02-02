import streamlit as st
from Pages import visualisasi, gis, list_hargaRumah
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Affordability Index Indonesia", layout="wide")
with st.sidebar:
    selected = option_menu(
        menu_title="Dashboard", 
        options=["Beranda", "Daftar Harga", "Visualisasi", "Peta GIS"],  
        icons=["house", "list-task", "bar-chart-line", "geo-alt-fill"],  
        menu_icon="grid-fill", 
        default_index=0,
        styles={
           "container": {
                "padding": "5px", 
                "background-color": "transparent"
            }, 
            "icon": {
                "color": "var(--text-color)", 
                "font-size": "20px"
            },       
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "0px", 
                "--hover-color": "#3e4149"                                 
            },
            "nav-link-selected": {"background-color": "#007bff"},          
        }
    )
    
    st.sidebar.divider()
    st.sidebar.caption("📊 **Data Source:**")
    st.sidebar.caption("- Scraping Properti (2025-2026)")
    st.sidebar.caption("- Data UMP Resmi Pemerintah")
    
if selected == "Beranda":
    st.title("🏡 Perbandingan Harga Rumah dengan UMP di Indonesia")
    st.markdown("""
    Aplikasi berbasis **Streamlit** untuk menganalisis perbandingan harga rumah dengan **Upah Minimum Provinsi (UMP)** di Indonesia, 
    guna melihat tingkat keterjangkauan hunian di berbagai wilayah.
    """)
    
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 Tujuan")
        st.markdown("""
        * Menganalisis perbandingan harga rumah terhadap UMP.
        * Menyajikan data dalam bentuk grafik dan peta (GIS).
        * Memberikan visualisasi yang mudah dipahami bagi masyarakat luas.
        """)

    with col2:
        st.markdown("### 📊 Sumber Data")
        st.markdown("""
        * **Harga Rumah**:  hasil web scraping dari situs properti
        * **UMP**: data resmi Upah Minimum Provinsi Indonesia
        """)

    st.divider()

    st.markdown("### 🔄 Alur Pengolahan Data")
    
    a1, a2, a3, a4, a5, a6 = st.columns(6)
    
    with a1:
        st.info("**1. Scraping**")
        st.caption("Pengambilan data harga rumah dari web.")
        
    with a2:
        st.info("**2.Cleaning & Preprocessing**")
        st.caption("Pembersihan dan standarisasi data.")
        
    with a3:
        st.info("**3. Analisis**")
        st.caption("Komparasi harga rumah vs UMP.")
        
    with a4:
        st.info("**4. Visualisasi**")
        st.caption("Pembuatan grafik dan tabel interaktif.")
        
    with a5:
        st.info("**5. GIS**")
        st.caption("Pemetaan tingkat keterjangkauan rumah.")
        
    with a6:
        st.info("**6.Streamlit**")
        st.caption("penyajian aplikasi interaktif")
    st.markdown("---")
    
    
    
if selected == "Daftar Harga":
    
    st.title("🏠 Database Harga Rumah & UMP")
   
    st.divider()
    list_hargaRumah.render()

elif selected == "Visualisasi":
    st.title("📈 Analisis Harga Rumah VS UMP")
    st.info("Visualisasi ini membantu Anda melihat seberapa jauh gap antara kenaikan gaji (UMP) dengan kenaikan harga properti.")
    st.divider()
    visualisasi.render()
    
elif selected == "Peta GIS":
    st.title("📍 Peta Keterjangkauan Hunian")
    st.divider()
    gis.render()