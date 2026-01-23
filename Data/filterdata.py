import pandas as pd

importPath = "./Data/Raw/rumah123_raw.csv"
exportPath = "./Data/Clean/rumah123_clean.csv"
df = pd.read_csv(importPath)

print(df.head())
print(df.columns)

df = df.drop_duplicates()

print(df.isnull().sum())
df = df.dropna(subset=['title'])

df['price'] = df['price'].astype(str)

df = df[df['price'].str.contains(r'^Rp *\d', na=False)]

df.to_csv(exportPath, index=False)

