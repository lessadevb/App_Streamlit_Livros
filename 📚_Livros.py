import pandas as pd
import plotly.express as px
import streamlit as st

from data import load_books, normalize_url

df_top100_books = load_books()

st.title("Catálogo em alta")
st.caption(
    "Escolha pelo menos um gênero na barra lateral para ver o catálogo. Depois use os outros filtros, gráficos e o atalho para reviews."
)

price_min = float(df_top100_books["book price"].min())
price_max = float(df_top100_books["book price"].max())
rating_min_data = float(df_top100_books["rating"].min())
rating_max_data = float(df_top100_books["rating"].max())

genres = sorted(df_top100_books["genre"].dropna().unique())

with st.sidebar:
    st.header("Filtros")
    max_price = st.slider(
        "Preço máximo (USD)",
        min_value=price_min,
        max_value=price_max,
        value=price_max,
        step=0.01,
    )
    selected_genres = st.multiselect(
        "Gêneros",
        options=genres,
        help="Selecione um ou mais gêneros. Nada é pré-selecionado: a lista só aparece após sua escolha.",
    )
    r_low, r_high = st.slider(
        "Faixa de rating do livro",
        min_value=rating_min_data,
        max_value=rating_max_data,
        value=(rating_min_data, rating_max_data),
        step=0.1,
    )
    search = st.text_input(
        "Buscar em título ou autor",
        placeholder="Ex.: fantasy, King…",
    ).strip()

    st.divider()
    st.subheader("Ir para reviews")
    st.caption("Escolha um livro da lista filtrada e abra a página Reviews.")

mask_price = df_top100_books["book price"] <= max_price
mask_genre = (
    df_top100_books["genre"].isin(selected_genres)
    if selected_genres
    else pd.Series(False, index=df_top100_books.index)
)
mask_rating = (df_top100_books["rating"] >= r_low) & (df_top100_books["rating"] <= r_high)
q = search.lower()
if q:
    mask_search = (
        df_top100_books["book title"].str.lower().str.contains(q, na=False)
        | df_top100_books["author"].str.lower().str.contains(q, na=False)
    )
else:
    mask_search = pd.Series(True, index=df_top100_books.index)

df_books = df_top100_books[mask_price & mask_genre & mask_rating & mask_search].copy()
df_books["_link"] = df_books["url"].map(normalize_url)

titles_filtered = sorted(df_books["book title"].unique().tolist())
default_pick = None
if "selected_book" in st.session_state and st.session_state["selected_book"] in titles_filtered:
    default_pick = st.session_state["selected_book"]
elif titles_filtered:
    default_pick = titles_filtered[0]

with st.sidebar:
    book_pick = (
        st.selectbox(
            "Livro",
            options=titles_filtered,
            index=titles_filtered.index(default_pick) if default_pick else 0,
            disabled=not titles_filtered,
        )
        if titles_filtered
        else None
    )
    go_reviews = st.button(
        "Abrir reviews deste livro",
        type="primary",
        disabled=not titles_filtered,
    )

if go_reviews and book_pick:
    st.session_state["selected_book"] = book_pick
    st.session_state["reviews_book_select"] = book_pick
    st.switch_page("✍️_Reviews.py")

if not selected_genres:
    st.info("Selecione **pelo menos um gênero** na barra lateral para carregar o catálogo.")
    st.stop()

if df_books.empty:
    st.warning("Nenhum livro com esses filtros. Afrouxe os critérios e tente de novo.")
    st.stop()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Livros na lista", len(df_books))
m2.metric("Preço médio", f"${df_books['book price'].mean():.2f}")
m3.metric("Rating médio", f"{df_books['rating'].mean():.2f}")
m4.metric("Gêneros distintos", df_books["genre"].nunique())

st.subheader("Tabela")
_display = df_books.copy()
_display["url"] = _display["_link"].map(lambda u: u if u else None)
_display = _display.drop(columns=["_link"])

st.dataframe(
    _display,
    column_config={
        "Rank": st.column_config.NumberColumn("Rank", format="%d"),
        "book title": st.column_config.TextColumn("Título", width="large"),
        "book price": st.column_config.NumberColumn("Preço", format="$%.2f"),
        "rating": st.column_config.NumberColumn("Rating", format="%.1f"),
        "author": st.column_config.TextColumn("Autor"),
        "year of publication": st.column_config.NumberColumn("Ano", format="%d"),
        "genre": st.column_config.TextColumn("Gênero"),
        "url": st.column_config.LinkColumn("Amazon", display_text="Abrir"),
    },
    hide_index=True,
    use_container_width=True,
)

csv_bytes = _display.to_csv(index=False).encode("utf-8")
st.download_button(
    "Baixar resultado filtrado (CSV)",
    data=csv_bytes,
    file_name="livros_filtrados.csv",
    mime="text/csv",
)

tab1, tab2, tab3 = st.tabs(["Distribuições", "Relações", "Por gênero"])

year_counts = df_books["year of publication"].value_counts().sort_index()
fig_year = px.bar(
    x=year_counts.index.astype(str),
    y=year_counts.values,
    labels={"x": "Ano de publicação", "y": "Quantidade de livros"},
    title="Livros por ano",
)
fig_year.update_layout(showlegend=False, xaxis_tickangle=-45)

fig_price = px.histogram(
    df_books,
    x="book price",
    nbins=20,
    title="Distribuição de preços",
    labels={"book price": "Preço (USD)", "count": "Livros"},
)

with tab1:
    c1, c2 = st.columns(2)
    c1.plotly_chart(fig_year, use_container_width=True)
    c2.plotly_chart(fig_price, use_container_width=True)

fig_scatter = px.scatter(
    df_books,
    x="book price",
    y="rating",
    hover_data={"book title": True, "author": True, "genre": True},
    title="Preço × rating",
    labels={"book price": "Preço (USD)", "rating": "Rating"},
)
fig_scatter.update_traces(marker=dict(size=10, opacity=0.75))

with tab2:
    st.plotly_chart(fig_scatter, use_container_width=True)

genre_counts = df_books["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]
fig_genre = px.bar(
    genre_counts,
    x="count",
    y="genre",
    orientation="h",
    title="Livros por gênero (lista filtrada)",
    labels={"count": "Livros", "genre": "Gênero"},
)
fig_genre.update_layout(yaxis={"categoryorder": "total ascending"}, height=max(400, len(genre_counts) * 28))

with tab3:
    st.plotly_chart(fig_genre, use_container_width=True)
