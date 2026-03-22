# App Streamlit — Livros e Reviews

Aplicação interativa em **Streamlit** para explorar um ranking Top-100 de livros em alta, filtrar por vários critérios e ler reviews de clientes com filtros e leitura confortável.

## Páginas

- **Livros** (`📚_Livros.py`): catálogo filtrado, métricas, tabela com link para a Amazon, gráficos (Plotly) e atalho para a página de reviews.
- **Reviews** (`✍️_Reviews.py`): ficha do livro, link para a Amazon, comparação de preço/rating com o restante do ranking e lista de reviews com filtros.

A navegação entre páginas é feita por `st.navigation` no arquivo principal.

## Ponto de entrada

Execute sempre a partir de `streamlit_app.py`, que configura a aplicação (`st.set_page_config`) e registra as páginas com título e ícone.

## Dados

O módulo `data.py` carrega os CSV em `datasets/` com `@st.cache_data`:

- `Top-100 Trending Books.csv` — livros do ranking (preço, rating, autor, ano, gênero, URL).
- `customer reviews.csv` — reviews associadas ao nome do livro (texto, estrelas, verificação, data).

Os caminhos dos arquivos usam `pathlib` para funcionar bem no Windows e em outros sistemas.

## Página Livros — o que o app faz

- **Gênero**: multiselect **sem pré-seleção**. É obrigatório escolher pelo menos um gênero para a lista e os gráficos aparecerem; até lá, uma mensagem orienta o uso do filtro.
- **Outros filtros na barra lateral**: preço máximo (USD), faixa de rating do livro, busca por texto no título ou no autor.
- **Métricas**: quantidade de livros no recorte, preço médio, rating médio e quantidade de gêneros distintos (entre os livros filtrados).
- **Tabela**: colunas formatadas e coluna de link **Abrir** para a Amazon (URLs normalizadas com `https://` quando necessário).
- **Download**: botão para exportar o resultado filtrado em CSV.
- **Gráficos** (abas): livros por ano, histograma de preços, dispersão preço × rating, barras por gênero.
- **Ir para reviews**: escolha um livro na lista filtrada e use **Abrir reviews deste livro** para ir à outra página com o livro já selecionado (`st.switch_page` + `st.session_state`).

## Página Reviews — o que o app faz

- **Seleção de livro** na barra lateral, sincronizada com o botão vindo da página Livros.
- **Link** para a página do produto na Amazon, quando houver URL.
- **Métricas** com *delta*: preço em relação à **mediana** e rating em relação à **média** do Top-100.
- **Filtros de reviews**: estrelas mínimas e opção “só verificadas”.
- **Ordenação** por data da review quando a data está no formato esperado.
- **Textos longos**: trecho inicial e *expander* para ler a review completa.

## Tecnologias

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly Express](https://plotly.com/python/plotly-express/)

## Como rodar

Requisito: Python 3.

Instale as dependências:

```bash
pip install streamlit pandas plotly
```

Inicie o app:

```bash
streamlit run streamlit_app.py
```

## Estrutura útil do projeto

| Arquivo | Função |
|--------|--------|
| `streamlit_app.py` | Config global e `st.navigation` |
| `data.py` | Leitura em cache dos CSV e normalização de URL |
| `📚_Livros.py` | Catálogo e visualizações |
| `✍️_Reviews.py` | Detalhe do livro e reviews |
| `datasets/` | Arquivos de dados |
