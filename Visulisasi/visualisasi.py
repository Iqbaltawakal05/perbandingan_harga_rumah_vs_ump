import pandas as pd

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
    print(df_rumah['price'])
    hargaRumah = df_rumah['price'].apply(lambda x: mapppingPrice(x))
    print(hargaRumah)
    

main()