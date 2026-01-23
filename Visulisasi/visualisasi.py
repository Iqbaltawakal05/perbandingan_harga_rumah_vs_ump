import pandas as pd
import mapping_ump

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
        
def main():
    hargaRumah = df_rumah.copy()
    hargaRumah['price'] = df_rumah['price'].apply(lambda x: mapppingPrice(x))
    print(hargaRumah.columns)
    print(mapping_ump.main().columns)

    

main()