import streamlit as st
import pandas as pd
import plotly.express as px


st.title('SkiForAll')

st.write('aquí encontrarás información detallada de las estaciones de la península.')

st.markdown('---')

df = pd.read_csv('data_infonieve.csv')

df = df.drop('id', axis=1)

logo_infonieve = 'logo_infonieve.jpg'

with st.sidebar:
    
    st.image(logo_infonieve, caption='Logo infonieve', width=125) 
    
    estacion = st.selectbox('Estación',sorted(df.name.unique()))
    
    
estacion_data = df[df['name'] == estacion].iloc[0]

# tarjetas de debajo del titulo

col1, col2, col3 = st.columns(3)

col1.metric("Kms de la estación", estacion_data['km_total'])
col2.metric("Telesillas de la estación", estacion_data['lifts_total'])
col3.metric("Precio forfait", estacion_data['forfait'])

# grafico colores pistas

fig = px.pie(estacion_data, names=['pistas verdes', 'pistas azules', 'pistas rojas', 'pistas negras'], 
             title='Niveles de pistas',
             values= [estacion_data['green_runs_total'], estacion_data['blue_runs_total'],
                      estacion_data['red_runs_total'], estacion_data['black_runs_total']])

st.plotly_chart(fig, use_container_width=True)


# tarjetas indicativas servicios

col1, col2, col3, col4 = st.columns(4)

if estacion_data.snowpark == 1:
    col1.metric('Snowpark', 'Sí')
else:
    col1.metric('Snowpark', 'No')
    
if estacion_data.raquetas == 1:
    col2.metric('Raquetas', 'Sí')
else:
    col2.metric('Raquetas', 'No')
    
if estacion_data.trineos == 1:
    col3.metric('Trineos', 'Sí')
else:
    col3.metric('Trineos', 'No')
    
if estacion_data.esqui_de_fondo == 1:
    col4.metric('Esquí de fondo', 'Sí')
else:
    col4.metric('Esquí de fondo', 'No')
  
 
st.markdown('---')


st.subheader('Comparador de precios')

estaciones_forfait = st.multiselect('Seleccione estaciones para comparar:', df.name.unique())

# Filtrar el DataFrame según las estaciones seleccionadas
df_filtrado = df[df.name.isin(estaciones_forfait)]

# barchart
fig = px.bar(df_filtrado, x='name', y='forfait', title='Comparación de Precios de Forfaits',
             labels={'name': 'Estación', 'forfait': 'Precio del Forfait'})

st.plotly_chart(fig, use_container_width=True)


st.markdown('---')

st.subheader('Precio por Kilómetro')

df['precio_por_km'] = df['forfait'] / df['km_total']

fig_2 = px.line(df, x='name', y='precio_por_km',
                labels={'name': 'Estación', 'precio_por_km':'Precio por km'})

st.plotly_chart(fig_2, use_container_width=True)



