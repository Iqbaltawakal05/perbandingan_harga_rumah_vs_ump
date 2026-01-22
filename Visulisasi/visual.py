import pandas as pd

#baca data raw dan data ump
df_rawdata = pd.read_csv("Data/raw/rumah123_raw.csv")
df_ump = pd.read_csv("Data/support/Data_UMP.csv")
df_kodeWilayah = pd.read_csv("Data/support/Data_KodeWilayah.csv", dtype={"kode": str})

print("Kolom raw_data:", df_rawdata.columns)
print("Kolom df_ump:", df_ump.columns)
print("Kolom kode wilayah:", df_kodeWilayah.columns)

print(df_kodeWilayah.dtypes)