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

coluna_esquerda, coluna_direita = st.columns([1, 1])

# Verifica se o DataFrame não está vazio ANTES de continuar
if not df.empty:
    # Pega os 5 filmes com maior 'mean_rating' 
    top_5_filmes = (
        df
        .sort_values(by='mean_rating', ascending=False)
        .head(5)
    )

    top_5_PIORES_filmes = (
        df
        .sort_values(by='mean_rating', ascending=True)
        .head(5)
    )

    # Verifica novamente se a tabela top_5_filmes não está vazia
    if not top_5_filmes.empty:
        # Cria o gráfico de barras usando Plotly Express
        fig = px.bar(
            top_5_filmes,
            x='title',
            y='mean_rating',
            title=f'Top 5 (MELHORES) Filmes/Séries de {genero_selecionado.upper()} com Maiores Ratings Durante o {intervalo_data[0].year} e {intervalo_data[1].year}',
            labels={'title': 'Título do Filme/Série', 'mean_rating': 'Média de Nota'},
            color='title'
        )
        fig.update_layout(
            font=dict(size=14, color="#e5e5e5"),
            plot_bgcolor="#1c1c1c",
            title_font_size=20,
            
        )
        # Exiba o gráfico no Streamlit
        coluna_esquerda.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Não há filmes com nota disponível para o seu filtro.")
    
    if not top_5_PIORES_filmes.empty:
        # Cria o gráfico de barras usando Plotly Express
        fig = px.bar(
            top_5_PIORES_filmes,
            x='title',
            y='mean_rating',
            title=f'Top 5 (PIORES) Filmes/Séries de {genero_selecionado.upper()} com Maiores Ratings Durante o {intervalo_data[0].year} e {intervalo_data[1].year}',
            labels={'title': 'Título do Filme/Série', 'mean_rating': 'Média de Nota'},
            color='title'
        )
        fig.update_layout(
            font=dict(size=14, color="#e5e5e5"),
            plot_bgcolor="#1c1c1c",
            title_font_size=20
        )
        # Exiba o gráfico no Streamlit
        coluna_direita.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Não há filmes com nota disponível para o seu filtro.")
else:
    st.write("Não há dados para o filtro selecionado. Ajuste os filtros para ver os resultados.")




menu = st.sidebar.radio(
    "Navegação",
    ["Dashboard", "Indicadores"]
)

if menu == "Dashboard":
    st.title("📊 Dashboard de Filmes")
    # aqui fica o código da parte principal
    st.write("Gráficos principais...")

elif menu == "Indicadores":
    st.title("📊 Indicadores de Filmes")
    

    col1, col2 = st.columns(2)

    # 1) Quantidade de filmes lançados por ano
    with col1:
        filmes_por_ano = df.groupby("year")["title"].count().reset_index()
        fig1 = px.line(
            filmes_por_ano,
            x="year",
            y="title",
            title=f"Quantidade de Filmes Lançados por Ano  ({genero_selecionado})",
            markers=True
        )
        fig1.update_layout(
            font=dict(size=14, color="#e5e5e5"),
            plot_bgcolor="#1c1c1c",
            title_font_size=20
        )
        st.plotly_chart(fig1, use_container_width=True)

    # 2) Média de notas por gênero
    with col2:
        media_genero = df.groupby("genres")["mean_rating"].mean().reset_index()
        fig2 = px.bar(
            media_genero,
            x="genres",
            y="mean_rating",
            title=f"Média de Notas   ({genero_selecionado})",
            labels={"genres": "Gênero", "mean_rating": "Nota Média"},
            color="mean_rating"
        )
        fig2.update_layout(
            font=dict(size=14, color="#e5e5e5"),
            plot_bgcolor="#1c1c1c",
            title_font_size=20
        )
        st.plotly_chart(fig2, use_container_width=True)
