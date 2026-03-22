import pandas as pd
import streamlit as st

from data import load_books, load_reviews, normalize_url

df_top100_books = load_books()
df_reviews = load_reviews()

books = sorted(df_top100_books["book title"].unique().tolist())
if not books:
    st.error("Nenhum livro carregado.")
    st.stop()

if "selected_book" not in st.session_state or st.session_state["selected_book"] not in books:
    st.session_state["selected_book"] = books[0]

if (
    "reviews_book_select" not in st.session_state
    or st.session_state["reviews_book_select"] not in books
):
    st.session_state["reviews_book_select"] = st.session_state["selected_book"]

with st.sidebar:
    book = st.selectbox(
        "Livro",
        options=books,
        key="reviews_book_select",
    )
    st.session_state["selected_book"] = book

    min_review_rating = st.slider("Rating mínimo da review (estrelas)", 1, 5, 1)
    only_verified = st.checkbox("Só reviews verificadas", value=False)

rows = df_top100_books[df_top100_books["book title"] == book]
if rows.empty:
    st.error("Livro não encontrado na base.")
    st.stop()

row = rows.iloc[0]
book_url = normalize_url(row.get("url", ""))

avg_list_rating = float(df_top100_books["rating"].mean())
median_list_price = float(df_top100_books["book price"].median())
price_val = float(row["book price"])
rating_val = float(row["rating"])

delta_rating = round(rating_val - avg_list_rating, 2)
delta_price = round(price_val - median_list_price, 2)

st.title(row["book title"])
st.subheader(row["genre"])
if book_url:
    st.link_button("Ver na Amazon", book_url)

col1, col2, col3 = st.columns(3)
col1.metric(
    "Preço",
    f"${price_val:.2f}",
    delta=f"{delta_price:+.2f} vs mediana",
    help="Diferença em relação à mediana de preço do Top-100.",
)
col2.metric(
    "Rating do livro",
    f"{rating_val:.1f}",
    delta=f"{delta_rating:+.2f} vs média",
    help="Diferença em relação à média de ratings do Top-100.",
)
col3.metric("Ano de publicação", f"{int(row['year of publication'])}")

st.divider()

df_book_reviews = df_reviews[df_reviews["book name"] == book].copy()
df_book_reviews = df_book_reviews[df_book_reviews["reviewer rating"] >= min_review_rating]

if only_verified:
    df_book_reviews = df_book_reviews[
        df_book_reviews["is_verified"].astype(str).str.upper().isin(("TRUE", "1", "T"))
    ]

df_book_reviews["_sort_date"] = pd.to_datetime(
    df_book_reviews["date"],
    format="%d-%m-%Y",
    errors="coerce",
)
df_book_reviews = df_book_reviews.sort_values("_sort_date", ascending=False, na_position="last")

st.subheader("Reviews")
st.caption(f"{len(df_book_reviews)} review(s) com os filtros atuais.")

if df_book_reviews.empty:
    st.info("Nenhuma review encontrada com esses critérios.")
else:
    for _, r in df_book_reviews.iterrows():
        verified = str(r.get("is_verified", "")).upper() in ("TRUE", "1", "T")
        badge = " · Verificada" if verified else ""
        reviewer = str(r.get("reviewer", "Anônimo"))
        title = str(r.get("review title", "Sem título"))
        stars = int(r["reviewer rating"]) if pd.notna(r["reviewer rating"]) else "—"
        body = str(r.get("review description", ""))
        dt = str(r.get("date", ""))

        with st.chat_message("user"):
            st.markdown(f"**{title}**")
            st.caption(f"{reviewer} · {stars}★{badge} · {dt}")
            preview_len = 450
            if len(body) > preview_len:
                st.write(body[:preview_len].rstrip() + "…")
                with st.expander("Ler review completa"):
                    st.write(body)
            else:
                st.write(body)
