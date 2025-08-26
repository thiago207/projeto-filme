import streamlit as st
import pandas as pd
import plotly.express as px

#CARREGANDO DADOS
def carregar_dados():
    filmes = pd.read_csv(r"C:\Users\Pichau\Documents\estudos\projeto-filme\projeto-filme\movie.csv")
    return filmes
df = carregar_dados()


df['mean_rating'] = pd.to_numeric(df['mean_rating'], errors='coerce')



# transforma ano em datetime
df['year'] = pd.to_datetime(df['year'], format="%Y", errors="coerce")
df = df.dropna(subset=['year'])


# -------- FILTRO PERÍODO --------
data_inicial = df['year'].min().to_pydatetime()
data_final = df['year'].max().to_pydatetime()

intervalo_data = st.sidebar.slider(
    'Selecione o período de lançamento do filme',
    min_value=data_inicial,
    max_value=data_final,
    value=(data_inicial, data_final),
    format="Y"
)

df = df[(df['year'] >= intervalo_data[0]) & (df['year'] <= intervalo_data[1])]
df['year'] = df['year'].dt.year
# -------- FILTRO GÊNERO --------
lista_generos = ['Drama', 'Action', 'Animation', 'Children', 'Fantasy', 
                 'Musical', 'Adventure','Western', 'Thriller', 
                 'Romance', 'Horror', 'Mystery']

genero_selecionado = st.sidebar.selectbox(
    'Selecione o gênero do filme',
    options=lista_generos
)

# explode gêneros
df['genres'] = df['genres'].str.split('|')
df = df.explode('genres')

if genero_selecionado:
    df = df[df['genres'] == genero_selecionado]




tabela_media = (
    df
    .groupby(['year'])['mean_rating'] # Agrupa por 'year' e seleciona 'mean_rating'
    .mean()                           # Calcula a média de cada ano
    .sort_values(ascending=False)     # Ordena os resultados da maior para a menor média
)



# Verifica se o DataFrame não está vazio ANTES de continuar
if not df.empty:
    # Pega os 5 filmes com maior 'mean_rating' 
    top_5_filmes = (
        df
        .sort_values(by='mean_rating', ascending=False)
        .head(5)
    )

    # Verifica novamente se a tabela top_5_filmes não está vazia
    if not top_5_filmes.empty:
        # Cria o gráfico de barras usando Plotly Express
        fig = px.bar(
            top_5_filmes,
            x='title',
            y='mean_rating',
            title=f'Top 5 Filmes/Séries de {genero_selecionado.upper()} com Maiores Ratings Durante o {data_inicial.year} e {data_final.year}',
            labels={'title': 'Título do Filme/Série', 'mean_rating': 'Média de Nota'},
            color='title'
        )
        fig.update_layout(
            font=dict(size=14, color="#e5e5e5"),
            plot_bgcolor="#1c1c1c",
            title_font_size=20
        )
        # Exiba o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Não há filmes com nota disponível para o seu filtro.")
else:
    st.write("Não há dados para o filtro selecionado. Ajuste os filtros para ver os resultados.")
