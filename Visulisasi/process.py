import pandas as pd
import matplotlib.pyplot as plt

df_processed = pd.read_csv("./Data/processed/visualisasi.csv", dtype={"UpahMinimum": int, "price": int})

def keterjangkauan(arg_df_processed):
    tahun_menabung = arg_df_processed['price'] / arg_df_processed['UpahMinimum'] * 12
    return tahun_menabung.astype(int)

def main():
    df_final = df_processed.copy()
    
    #analisis lama menabung     
    df_final['lama_menabung'] = keterjangkauan(df_final)
    
    # analisis harga per provinsi dan lama menabung
    hargaStatPerProv = df_final.groupby(by='provinsi')['price'].agg(['min', 'max', 'mean']).reset_index()
    lamaMenabungStatPerProv = df_final.groupby(by='provinsi')['lama_menabung'].agg(['min', 'max', 'mean']).reset_index()

    # analisis lama menabung per kabupaten dan lama menabung
    hargastatPerKab = df_final.groupby(by='kabupaten')['price'].agg(['min', 'max', 'mean']).reset_index()
    lamaMenabungStatPerKab = df_final.groupby(by='kabupaten')['lama_menabung'].agg(['min', 'max', 'mean']).reset_index()
    
    result = {
        'hargaStatPerProv': hargaStatPerProv,
        'lamaMenabungStatPerProv': lamaMenabungStatPerProv,
        'hargastatPerKab': hargastatPerKab,
        'lamaMenabungStatPerKab': lamaMenabungStatPerKab
    }
    
    return result
    