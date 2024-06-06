import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt
#######################
# Page configuration
st.set_page_config(
    page_title="Top Musics Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

with open('style.css') as fp:
    st.markdown(f"<style>{fp.read()}</style>", unsafe_allow_html=True)

col1, col2, = st.columns(2)

df_music1 = pd.read_csv("data/spotify_data.csv") # lê o csv das músicas 
df_music = df_music1.dropna()#Tira os elementos nulos do csv (Coloquei um "ano" que chama "Todos")
#df_ordenado = df_music.sort_values(by=['streams'], ascending=True, inplace=False)
#Organização 
released_year_1 = df_music1['released_year'].sort_values(ascending=False) #coloca todos os anos em ordem de maior para o menor

meses_map = { #Dá um nome para os mêses no csv porque lá está apenas numerado
    0: "Todos",
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}
##################################################################### Meu dataset possui músicas com mais de 1 artista então a função abaixo divide os artistas dessas músicas para o filtro por artista funcionar direitinho
#Fazer a filtragem por artista 
def split_artists(artist_string):
    if isinstance(artist_string, str):  # Checa se é uma string
        return artist_string.split(",")
    else:
        return []  # volta uma lista vazia se não for
artist_map = {}
for index, row in df_music.iterrows():
    track_name = row["track_name"]
    artist_names = split_artists(row["artist(s)_name"])
    artist_map[track_name] = artist_names

# Filtrar por artistas únicos
artist_options_unique = []
temporary_list = []
for artist_name in df_music["artist(s)_name"].unique():  # Use the column directly
    if artist_name not in temporary_list:
        temporary_list.append(artist_name)
        artist_options_unique.append(artist_name)

# Filter songs by artists
def filter_by_artists(selected_artists):
    if selected_artists:  # Check se o artista está selecionado
        filtered_songs = []
        for index, row in df_music.iterrows():
            track_name = row["track_name"]
            artist_names = artist_map[track_name]
            for selected_artist in selected_artists:
                if selected_artist in artist_names:
                    filtered_songs.append(row)
                    break
        return filtered_songs
    else:  # Se não tiver artista selecionado, volta a lista toda
        return df_music.copy()  # Faz uma cópia pra não modificar o df original

df_solo = df_music[df_music["artist_count"] == 1] #Deixa apenas os artistas solo, aparecerem no multiselect para não bugar
############################################
#Sidebar
with st.sidebar: 
    st.title('🎶Musicas mais escutadas Spotify')#Título da página
    
    selected_year = st.sidebar.selectbox('Filtrar por ano',released_year_1.unique()) #Deixa o usúario escolher um ano pra filtrar as músicas
    
    opcoes_meses = list(meses_map.values()) # #Deixa o usúario escolher um mês pra filtrar as músicas
    mes_selecionado = st.selectbox("Filtrar por mês:", opcoes_meses)

    artistas_selecionados = st.multiselect("Selecione artistas:",df_solo['artist(s)_name'].unique(), default=[]) #deixa o usúario filtrar músicas por vários artistas
    st.text('Rafael Pastor Pereira')
    st.text('PDITA 009')
    st.image('spotify.png', width=150)

#############################################

df_filtrado = filter_by_artists(artistas_selecionados)#aplica o filtro por artista
df_filtrado = pd.DataFrame(df_filtrado).sort_values(by="streams", ascending= False, )#ordena o dataframe por ordem de mais tocado

if selected_year != 'Todos':#se o ano não for todos vai filtrar pelo ano selecionado
    df_filtrado = df_filtrado[df_filtrado['released_year'] == selected_year]
    
if mes_selecionado != 'Todos':# Se o mês nao for Todos vai filtrar pelo mês selecionado
    df_filtrado = df_filtrado[df_filtrado['released_month'] == opcoes_meses.index(mes_selecionado)]

###########################################
df_energetica = df_filtrado.sort_values(by='energy_%', ascending=False).head(10) #Filtra o dataset pelas 10 músicas mais enérgicas
nome_musica1 = df_energetica['track_name']#Somente a colúna das músicas
energia = df_energetica['energy_%']#somente a coluna da energia
#############################################
df_playlists = df_filtrado.sort_values(by = 'in_spotify_playlists')
nome_musica2 = df_playlists['track_name']
spotify_playlist = df_playlists['in_spotify_playlists']
 #############################################

soma_músicas100 = len(df_filtrado)# Verifica se o dataset esta vazio senão da erro de dividir por zero
if soma_músicas100 == 0:
    st.write('Nenhuma música encontrada')
else: # Se não estiver vazio pode executar a conta que modifica o gráfico de Donut
    porcentagem = 812 / soma_músicas100 * 100
    #############################################




def make_donut(input_response, input_text,):#Grafico de donut
  # Escolha de cores
  chart_color = ['#1ed760', '#2f4538']
    # Criaçao da lista utilizada para o grafico
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })

  plot = alt.Chart(source).mark_arc(innerRadius=80, cornerRadius=35).encode( #Criação do Grafico de donut
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          domain=[input_text, ''],
                          range=chart_color),
                      legend=None),
  ).properties(width=300, height=300)
    # Formataçao do Texto do Grafico
  text = plot.mark_text(align='center', color="#29b5e8", font="lato", fontSize=32, fontWeight=700, fontStyle="").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=80, cornerRadius=30).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # select color theme
                      legend=None),
  ).properties(width=300, height=300)
  return plot_bg + plot + text

 ##############################################
with col1: 
    st.title('Mais escutadas :fire:') #Título
    st.dataframe(df_filtrado,#Mostra o dataframe com algumas colunas apenas e esconde o número do index
            column_order=("streams", "track_name","artist(s)_name", "released_year",'released_month'),
            hide_index=True,)
    st.title("Em playlists")
    if len(df_playlists) == 0:#Se o dataset está vazio    
        st.write("O dataset está vazio. Nenhum gráfico pode ser criado.") #vai printar issom porque se o grafico estiver vazio da erro
    else:
        fig2 = px.bar(#faz o gráfico de barras
    x=nome_musica2,
    y=spotify_playlist,
    title="Em quantas playlists do spotify as músicas se encontram",
    labels={"x": "Nome da música", "y": "Quantidade"},
    width=600,
    color_discrete_sequence=[('#1ed760')])
        st.plotly_chart(fig2)
    
with col2:
    st.title('Músicas mais enérgicas :zap:')#Título
    if len(df_energetica) == 0:#Se o dataset está vazio    
        st.write("O dataset está vazio. Nenhum gráfico pode ser criado.") #vai printar issom porque se o grafico estiver vazio da erro
    else:
        fig = px.bar(#faz o gráfico de barras
    x=nome_musica1,
    y=energia,
    title="Em (%)",
    labels={"x": "Nome da música", "y": "Nível de Energia da música em(%)"},
    width=600,
    color_discrete_sequence=[('#1ed760')])#define a cor verde
        
        st.plotly_chart(fig)#imprime o grafico
        b = round((soma_músicas100 / 812*100), 2)#numero do grafico donut
        a=make_donut(b, 'Músicas ')#chamando a função do grafico donut
        cols1 = st.columns((3,4,3))
        with cols1[1]:
            st.title('Músicas')
            st.altair_chart(a)#imprimindo o donut

    




