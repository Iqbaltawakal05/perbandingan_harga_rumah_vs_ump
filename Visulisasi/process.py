import pandas as pd
import mapping_rumah_ump

df_processed = pd.read_csv("./Data/processed/preprocessed.csv", dtype={"UpahMinimum": int, "price": int})
df_ump = pd.read_csv("./Data/support/Data_UMP.csv")

def keterjangkauan(arg_df_processed):
    tahun_menabung = arg_df_processed['price'] / arg_df_processed['UpahMinimum'] * 12
    return tahun_menabung.astype(int)

def main():
    mapping_rumah_ump.main()
    df_final = df_processed.copy()
    dataUMP = df_ump.copy()
    
    #analisis lama menabung     
    df_final['lama_menabung'] = keterjangkauan(df_final)
    
    # analisis harga per provinsi dan lama menabung
    hargaStatPerProv = df_final.groupby(by='provinsi')['price'].agg(['min', 'max', 'mean']).reset_index()
    lamaMenabungStatPerProv = df_final.groupby(by='provinsi')['lama_menabung'].agg(['min', 'max', 'mean']).reset_index()

    # analisis lama menabung per kabupaten dan lama menabung
    hargastatPerKab = df_final.groupby(by='kabupaten')['price'].agg(['min', 'max', 'mean']).reset_index()
    lamaMenabungStatPerKab = df_final.groupby(by='kabupaten')['lama_menabung'].agg(['min', 'max', 'mean']).reset_index()
    
    dataUMP['UpahMinimum'] = dataUMP['UpahMinimum'].str.replace('.', '').astype(int)
    
    result = {
        'hargaStatPerProv': hargaStatPerProv,
        'lamaMenabungStatPerProv': lamaMenabungStatPerProv,
        'hargastatPerKab': hargastatPerKab,
        'lamaMenabungStatPerKab': lamaMenabungStatPerKab,
        'dataUMP2020': dataUMP
    }
    
    return result
    