import pandas as pd
import re
import os

importPath = "../Data/Raw/rumah123_raw.csv"
exportPath = "../Data/Clean/rumah123_clean.csv"

os.makedirs(os.path.dirname(exportPath), exist_ok=True)

df = pd.read_csv(importPath)
df = df.drop_duplicates()
df = df.dropna(subset=["title", "price"])

df["title"] = (
     df["title"] 
     .astype(str) 
     .str.replace("\n", " ", regex=False) 
     .str.replace('"', "", regex=False) 
     .str.replace("'", "", regex=False) 
     .str.strip() )

df["price"] = df["price"].astype(str)

df["price"] = df["price"].str.split("-").str[0]

df["price"] = (
    df["price"]
    .str.replace("\n", " ", regex=False)
    .str.replace('"', "", regex=False)
    .str.replace(",", ".", regex=False)
    .str.strip()
)

df = df[df["price"].str.contains(r"^Rp\s*\d", case=False, na=False)]

df["price"] = df["price"].str.extract(
    r"(Rp\s*\d+(?:\.\d+)?\s*(?:m|miliar|jt|juta))",
    flags=re.IGNORECASE
)[0]

df.to_csv(exportPath, index=False, encoding="utf-8-sig")

print("\nCleaning selesai")
print("Total data bersih:", len(df))
