import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página para usar toda a largura
st.set_page_config(
    page_title="Dashboard de Filmes",
    page_icon="🎬",
    layout="wide",  # Isso faz usar toda a largura da tela
    initial_sidebar_state="expanded"
)

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

menu = st.sidebar.radio(
    "Navegação",
    ["Dashboard", "Indicadores"]
)

if menu == "Dashboard":
    st.title("📊 Dashboard de Filmes")
    
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
            
            # Configurações para ocupar mais espaço
            fig.update_layout(
                font=dict(size=14, color="#e5e5e5"),
                plot_bgcolor="#1c1c1c",
                title_font_size=20,
                height=600,  # Aumenta a altura do gráfico
                margin=dict(l=20, r=20, t=80, b=20),  # Reduz as margens
                showlegend=False  # Remove a legenda para mais espaço
            )
            
            # use_container_width=True + height fazem ocupar toda largura e mais altura
            st.plotly_chart(fig, use_container_width=True, height=600)
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
                title_font_size=20,
                height=600,  # Aumenta a altura do gráfico
                margin=dict(l=20, r=20, t=80, b=20),  # Reduz as margens
                showlegend=False  # Remove a legenda para mais espaço
            )
            
            st.plotly_chart(fig, use_container_width=True, height=600)
        else:
            st.write("Não há filmes com nota disponível para o seu filtro.")
    else:
        st.write("Não há dados para o filtro selecionado. Ajuste os filtros para ver os resultados.")

elif menu == "Indicadores":
    st.title("📊 Indicadores de Filmes")
    
    # Remove as colunas para que cada gráfico ocupe toda a largura
    # col1, col2 = st.columns(2)  # Comentado para usar toda largura

    if not df.empty:
        # 1) Quantidade de filmes lançados por ano - TELA CHEIA
        filmes_por_ano = df.groupby("year")["title"].count().reset_index()
        fig1 = px.line(
            filmes_por_ano,
            x="year",
            y="title",
            title=f"Quantidade de Filmes Lançados por Ano  ({genero_selecionado})",
            markers=True
        )
        fig1.update_layout(
            font=dict(size=16, color="#e5e5e5"),
            plot_bgcolor="#1c1c1c",
            title_font_size=24,
            height=500,  # Altura maior
            margin=dict(l=50, r=50, t=100, b=50)
        )
        st.plotly_chart(fig1, use_container_width=True, height=500)

        # 2) Média de notas por gênero - TELA CHEIA
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
            font=dict(size=16, color="#e5e5e5"),
            plot_bgcolor="#1c1c1c",
            title_font_size=24,
            height=500,  # Altura maior
            margin=dict(l=50, r=50, t=100, b=50)
        )
        st.plotly_chart(fig2, use_container_width=True, height=500)

# CSS customizado para remover padding/margin extras
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: none;
    }
    
    /* Remove espaçamento extra dos gráficos */
    .stPlotlyChart {
        background-color: transparent;
    }
</style>
""", unsafe_allow_html=True)