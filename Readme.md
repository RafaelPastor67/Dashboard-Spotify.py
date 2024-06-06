# Dashboard de Músicas do Spotify 🎶
Este repositório foi criado como desafio do Projeto Desenvolve, ele contém diversos dados sobre músicas do Spotify. Sendo possível filtrar por Ano e Mês de lançamento e também por Artista.

## Instruções de uso

Este projeto foi desenvolvido na versão 3.10.6 do Python. Para executar basta executar o seguinte comando no console do arquivo `Dashboard.py`: 
```
streamlit run Dashboards.py
```
## Bibliotecas necessárias
- Streamlit, version 1.35.0
- Pandas, Version: 2.2.2
- Altair Version: 5.3.0
- Plotly Version: 5.22.0
 
## Dataset
`spotify.csv` É o arquivo de dataset onde contém todos os dados sobre as músicas. os dados são:

- Nome da música 
- Nome do artista
- Playlists e paradas do Spotify
- Streams
- Presença da Apple Music
- Presença do Deezer
- Gráficos Shazam
- Vários recursos de áudios
 
 O dataset foi retirado do site Kaggle: https://www.kaggle.com/datasets/arnavvvvv/spotify-music
 mas alguns dados precisaram ser modificados
