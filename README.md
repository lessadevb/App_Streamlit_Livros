# App Streamlit - Livros e Reviews

Aplicação interativa desenvolvida com **Streamlit** para explorar um ranking de livros e visualizar reviews de usuários.

O projeto possui duas páginas:
- **Livros**: filtros e visualizações sobre os livros em alta.
- **Reviews**: detalhes de um livro selecionado e exibição dos comentários associados.

## Como o projeto funciona

O ponto de entrada é o arquivo `streamlit_app.py`, que cria a navegação entre duas páginas:

- `📚_Livros.py`
- `✍️_Reviews.py`

### Página 1: `📚_Livros.py`

Nesta página, o app:
- Carrega os datasets com `pandas`.
- Cria um filtro lateral de preço máximo (`slider`).
- Filtra os livros com base no preço escolhido.
- Exibe a tabela de livros filtrados.
- Mostra dois gráficos com `plotly.express`:
  - quantidade de livros por ano de publicação (gráfico de barras),
  - distribuição dos preços dos livros (histograma).

### Página 2: `✍️_Reviews.py`

Nesta página, o app:
- Carrega os mesmos datasets.
- Permite selecionar um livro no menu lateral (`selectbox`).
- Exibe informações principais do livro:
  - Título,
  - Gênero,
  - Preço,
  - Rating,
  - Ano de Publicação.
- Lista as reviews relacionadas ao livro em formato de mensagens de chat.

## Tecnologias utilizadas

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly Express](https://plotly.com/python/plotly-express/)

## Requisitos

- Python

Instale as dependências:

```bash
pip install streamlit pandas plotly
```

Rode a aplicação:

```bash
streamlit run streamlit_app.py
```

## Pontos importantes do projeto

- **Navegação multipágina** simples e clara com `st.navigation`.
- **Análise exploratória** dos livros via filtro de preço e gráficos.
- **Visualização de reviews** de forma amigável com componentes de chat.
- **Separação por responsabilidades**: cada página em um arquivo diferente.
- **Base pronta para evolução**, podendo incluir novos filtros, métricas e dashboards.
