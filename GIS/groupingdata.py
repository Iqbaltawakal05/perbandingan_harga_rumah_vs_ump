import pandas as pd

df = pd.read_csv("./Data/processed/preprocessed.csv")

# Groupby Kabupaten dan hitung min, max, rata-rata, dan jumlah listing (UpahMinimum tetap per kabupaten)
summary_df = df.groupby('kabupaten').agg(
    min_price=('price', 'min'),
    max_price=('price', 'max'),
    average_price=('price', 'mean'),
    total_entries=('price', 'count'),
    UpahMinimum=('UpahMinimum', 'first')
).reset_index()

# Rounding
summary_df['average_price'] = summary_df['average_price'].round(2)

summary_df.to_csv("./GIs/Data/grouped.csv", index=False)
print("Done")