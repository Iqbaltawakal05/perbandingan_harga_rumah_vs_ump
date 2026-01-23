import pandas as pd

#baca data raw dan data ump
df_dataRumah = pd.read_csv("Data/clean/rumah123_clean.csv")
df_ump = pd.read_csv("Data/support/Data_UMP.csv")
df_kodeWilayah = pd.read_csv("Data/support/Data_KodeWilayah.csv", dtype={"kode": str})

def mappingKodeWilayah():
    df_prov = df_kodeWilayah[~ df_kodeWilayah['kode'].str.contains(r'\.')].copy()
    df_prov = df_prov.rename(columns={'namaWilayah': 'provinsi', 'kode': 'kode_prov'})

    df_kec = df_kodeWilayah[df_kodeWilayah['kode'].str.count(r'\.') == 2].copy()
    df_kec = df_kec.rename(columns={'namaWilayah': 'kecamatan', 'kode': 'kode_kec'})
    
    df_kabupaten = df_kodeWilayah[df_kodeWilayah['kode'].str.count(r'\.') == 1].copy()
    df_kabupaten = df_kabupaten.rename(columns={'namaWilayah': 'kabupaten', 'kode': 'kode_kab'})

    df_kec['kode_prov'] = df_kec['kode_kec'].str.slice(0, 2)
    df_kabupaten['kode_prov'] = df_kabupaten['kode_kab'].str.slice(0, 2)

    df_mapping = pd.merge(df_kec, df_prov, on='kode_prov', how='left')
    df_final = pd.merge(df_mapping, df_kabupaten, on='kode_prov', how='left')
    
    return df_final

def main():
    df_ump_local = df_ump.copy()
    df_ump_local['UpahMinimum'] = df_ump_local['UpahMinimum'].str.replace('.', '').astype(int)
    df_mapping = mappingKodeWilayah()
    
    df_ump_local['Provinsi'] = df_ump_local['Provinsi'].str.upper()
    df_mapping['kecamatan'] = df_mapping['kecamatan'].str.upper()

    df_ump_local = df_ump_local.rename(columns={'Provinsi': 'provinsi'})
    df_final = pd.merge(df_ump_local, df_mapping[['kecamatan', 'provinsi', 'kabupaten']], on='provinsi', how='left')

    df_final.to_csv("./Data/processed/mapping_ump.csv", index=False)

    return df_final

