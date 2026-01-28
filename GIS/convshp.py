import geopandas as gpd

gdf = gpd.read_file("./GIS/Data/Batas Administrasi Indonesia/Kab_Kota.shp")

# Optional: reproject to WGS84 (Folium expects EPSG:4326)
gdf = gdf.to_crs(epsg=4326)

# Simplify geometry to reduce file size
gdf["geometry"] = gdf.geometry.simplify_coverage(tolerance=0.0005) #Semakin kecil semakin detail dan semakin lama Streamlit Folium untuk compute
gdf.to_file("./GIS/Data/Batas Administrasi Indonesia/Kab_Kotacheck.geojson", driver="GeoJSON")