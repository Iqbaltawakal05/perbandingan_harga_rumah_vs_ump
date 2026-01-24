import pandas as pd
import mapping_ump
import re

df_mappingUmp = pd.read_csv("./Data/processed/mapping_ump.csv")
df_rumah = pd.read_csv("./Data/Clean/rumah123_clean.csv")

def mapppingPrice(text_harga):
    try:
        parts = text_harga.split(' ')
    
        angka_string = parts[1].replace(',', '.')
        angka = float(angka_string)
        satuan = parts[2].lower()
        
        if 'm' in satuan: 
            nominal = angka * 1_000_000_000
        elif 'j' in satuan: 
            nominal = angka * 1_000_000
        else:
            nominal = angka 
            
        return int(nominal) 
        
    except Exception:
        return 0

# bersihin nama lokasi dari kata kab, kota, adm dari data mapping
def bersihkan_nama_kota(text):
    clean = re.sub(r'^(KAB\.?|KOTA|KABUPATEN|ADM\.?)\s+', '', str(text).upper())
    return clean     

# buat cari nama lokasi ke data mapping
def cari_kabupaten(lokasi_raw, map_keyword_to_real):
    lokasi_upper = str(lokasi_raw).upper()
    
    for keyword, nama_asli in map_keyword_to_real.items():
        if keyword in lokasi_upper:
            return nama_asli 
    
    return None 
     
def main():
    df_mappingUMP = mapping_ump.main()
    hargaRumah = df_rumah.copy()
    hargaRumah['price'] = df_rumah['price'].apply(lambda x: mapppingPrice(x))

    ref_ump = df_mappingUMP[['kabupaten', 'provinsi', 'UpahMinimum']].drop_duplicates()
    ref_ump['keyword'] = ref_ump['kabupaten'].apply(bersihkan_nama_kota)
    ref_ump = ref_ump.sort_values(by='keyword', key=lambda x: x.str.len(), ascending=False)
    
    # bikin dicitonary biar bisa search nama lokasinya
    map_keyword_to_real = dict(zip(ref_ump['keyword'], ref_ump['kabupaten']))
    
    hargaRumah['kabupaten_terdeteksi'] = hargaRumah['location'].apply(lambda x: cari_kabupaten(x, map_keyword_to_real))
    
    df_final = pd.merge(
        hargaRumah,
        ref_ump[['kabupaten', 'UpahMinimum', 'provinsi']],
        left_on='kabupaten_terdeteksi',
        right_on='kabupaten',
        how='left'
    )
    
    df_final.drop_duplicates(inplace=True)
    df_final.dropna(inplace=True)
    df_final = df_final.drop(columns=['kabupaten_terdeteksi'])
    df_final.to_csv("./Data/processed/visualisasi.csv", index=False)
    

main()