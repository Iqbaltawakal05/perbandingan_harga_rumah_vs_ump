import streamlit as st
from Visualisasi import visualisasi

st.set_page_config(page_title="Visualisasi", layout="wide")

def load_figures():
    return visualisasi.main()

def render():
    st.title("Visualisasi Harga Rumah vs UMP")

    pilihan = st.selectbox(
        "Pilih visualisasi",
        (
            "Harga Rumah per Provinsi",
            "Lama Menabung per Provinsi",
            "Harga Rumah per Kabupaten",
            "Lama Menabung per Kabupaten",
            "UMP per Provinsi"
        )
    )

    figs = load_figures()

    mapping = {
        "Harga Rumah per Provinsi": "hargaStatPerProv",
        "Lama Menabung per Provinsi": "lamaMenabungStatPerProv",
        "Harga Rumah per Kabupaten": "hargastatPerKab",
        "Lama Menabung per Kabupaten": "lamaMenabungStatPerKab",
        "UMP per Provinsi": "dataUMP2020"
    }

    st.pyplot(figs[mapping[pilihan]])