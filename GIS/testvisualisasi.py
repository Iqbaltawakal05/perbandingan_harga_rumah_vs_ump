import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd

st.set_page_config(layout="wide")
st.title("Peta Kabupaten Indonesia beserta Harga Properti perKabupaten")

# Data Processing (Inner Join)
@st.cache_data
def get_filtered_data(geojson_path, csv_path):
    
    gdf = gpd.read_file(geojson_path)
    # Uppercase
    gdf['KAB_KOTA'] = gdf['KAB_KOTA'].str.upper().str.strip()
    
    summary_df = pd.read_csv(csv_path)
    # Menghapus "Kab." pada CSV
    summary_df['kabupaten'] = summary_df['kabupaten'].str.replace(
        r'(?i)Kab\.\s*', '', regex=True
    ).str.upper().str.strip()
    
    # INNER JOIN
    merged_gdf = gdf.merge(summary_df, left_on="KAB_KOTA", right_on="kabupaten", how="inner")
    
    return merged_gdf


geojson_path = "./GIS/Data/Kab_Kota.geojson"
csv_path = "./GIS/Data/grouped.csv"

merged_gdf = get_filtered_data(geojson_path, csv_path)

# Map Config
# Default center (will be overridden by fit_bounds)
m = folium.Map(location=[-2.5489, 118.0149], zoom_start=5)
if not merged_gdf.empty:
    folium.GeoJson(
        merged_gdf,
        style_function=lambda feature: {
            "fillColor": "#3186cc",
            "color": "black",
            "weight": 1.5,
            "fillOpacity": 0.6,
        },
        highlight_function=lambda feature: {
            "fillColor": "#ff4800", 
            "color": "white", 
            "weight": 3,
            "fillOpacity": 0.8,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["KAB_KOTA", "UpahMinimum", "min_price", "max_price", "average_price", "total_entries"],
            aliases=["Kabupaten:", "Upah Minimum Provinsi:", "Harga Minimum:", "Harga Maksimum:", "Rata-rata:", "Total Listing Penjualan"],
            localize=True,
            sticky=True,
            style="font-family: sans-serif; font-size: 12px; padding: 10px;"
        )
    ).add_to(m)

    # AUTO-ZOOM: Fit the map view to only the areas with data
    sw = merged_gdf.total_bounds[[1, 0]].tolist() # South-West corner
    ne = merged_gdf.total_bounds[[3, 2]].tolist() # North-East corner
    m.fit_bounds([sw, ne])
else:
    st.error("No matches found between CSV and GeoJSON. Check your Kabupaten names!")

# Display
st_folium(
    m, 
    width="100%", 
    height=600,
    returned_objects=[], # Keeps map from reloading on every interaction (Biar Optimized)
)