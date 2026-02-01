import streamlit as st
from Pages import visualisasi, gis, list_hargaRumah

def main():
    halaman = st.sidebar.radio(
        "Navigasi",
        ("Daftar Harga Rumah", "Visualisasi", "GIS")
    )

    if halaman == "Daftar Harga Rumah":
        list_hargaRumah.render()
    elif halaman == "Visualisasi":
        visualisasi.render()
    else:
        gis.render()

if __name__ == "__main__":
    main()
