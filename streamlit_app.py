import streamlit as st

st.set_page_config(
    page_title="Explorador de livros",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

pg = st.navigation(
    [
        st.Page("📚_Livros.py", title="Livros", icon="📚"),
        st.Page("✍️_Reviews.py", title="Reviews", icon="✍️"),
    ]
)
pg.run()
