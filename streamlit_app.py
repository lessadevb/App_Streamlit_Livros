import streamlit as st

pg = st.navigation([st.Page("📚_Livros.py"), st.Page("✍️_Reviews.py")])
pg.run()