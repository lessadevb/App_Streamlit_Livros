from pathlib import Path

import pandas as pd
import streamlit as st

_DATA_DIR = Path(__file__).resolve().parent / "datasets"


@st.cache_data
def load_books() -> pd.DataFrame:
    return pd.read_csv(_DATA_DIR / "Top-100 Trending Books.csv")


@st.cache_data
def load_reviews() -> pd.DataFrame:
    return pd.read_csv(_DATA_DIR / "customer reviews.csv")


def normalize_url(url: str) -> str:
    if pd.isna(url) or not str(url).strip():
        return ""
    u = str(url).strip()
    if u.startswith("http://") or u.startswith("https://"):
        return u
    return f"https://{u}"
