import pandas as pd

df_mappingUmp = pd.read_csv("./Data/processed/mapping_ump.csv")
df_rumah = pd.read_csv("./Data/Clean/rumah123_clean.csv")

print(df_rumah['price'])