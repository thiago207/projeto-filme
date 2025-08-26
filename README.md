Análise Interativa de Filmes e Séries 🍿🎬
Este projeto é uma aplicação interativa desenvolvida com o objetivo de demonstrar a capacidade de tratar, filtrar e visualizar dados de forma dinâmica e intuitiva. A aplicação utiliza dados de filmes e séries, permitindo que o usuário explore o conteúdo e encontre os títulos de maior avaliação em um determinado período e gênero.

O projeto é construído em torno das bibliotecas Pandas, Streamlit e Plotly, cada uma desempenhando um papel crucial no pipeline de análise e visualização. 📊

Funcionalidades ✨
Filtros Dinâmicos: A interface da barra lateral (sidebar) permite ao usuário ajustar o período de lançamento e o gênero dos filmes e séries. ⚙️

Visualização Interativa: Um gráfico de barras exibe os 5 títulos com as maiores notas (ratings) de acordo com os filtros selecionados, utilizando a biblioteca Plotly para uma visualização rica e interativa. 📈

Tratamento de Dados: O código realiza a leitura do arquivo CSV, a conversão de tipos de dados (rating para numérico, ano para data), e a manipulação da coluna de gêneros (explode) para uma análise precisa. 🧹

Design Responsivo: A aplicação foi estilizada para ter uma aparência moderna, com um tema escuro e elementos visuais que melhoram a experiência do usuário. 🎨

Tecnologias Utilizadas 🛠️
Pandas: A base do projeto para o tratamento e manipulação dos dados. É usado para carregar o arquivo CSV, limpar dados ausentes e transformar colunas para análise. 🐼

Streamlit: Framework de código aberto que permitiu a criação de um painel (dashboard) de análise interativo de forma rápida e com poucas linhas de código Python. 🚀

Plotly Express: Uma biblioteca de visualização de dados de alto nível que gera gráficos interativos. Foi escolhida para criar o gráfico de barras devido à sua capacidade de adicionar interatividade e estilo. 📊
