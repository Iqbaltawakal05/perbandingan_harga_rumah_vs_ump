import streamlit as st
import pandas as pd

def render():

    df = pd.read_csv("Data/Clean/rumah123_clean.csv")
    df.columns = df.columns.str.strip().str.lower()

    display_df = df[["title", "price", "location", "link"]]

    st.caption(f"Total data: {len(display_df)}")

    st.dataframe(
        display_df,
        width="stretch",
        column_config={
            "link": st.column_config.LinkColumn(
                "Lihat Rumah"
            )
        }
    )
