import streamlit as st
import pandas as pd
import plotly.express as px


# Cargar datos
df = pd.read_csv('data_infonieve.csv')
df = df.drop('id', axis=1)

# logo en el sidebar
logo_infonieve = 'logo_infonieve.jpg'

st.sidebar.image(logo_infonieve, caption='Logo infonieve', width=125)

# selectbox para cambiar de pagina
analisis_seleccionado = st.sidebar.selectbox('Seleccione análisis:',
                                             ['Inicio', 'Información de Estación', 'Comparador de precios', 'Precio por Kilómetro', 'Servicios'])


# Dependiendo del análisis seleccionado, mostrar el contenido correspondiente

if analisis_seleccionado == 'Inicio':
    
    # Título de la aplicación
    st.title('SkiForAll')
    st.write('Aquí encontrarás información detallada de las estaciones de la península.')
    
    st.image('imagen_inicio_st.png')
    


elif analisis_seleccionado == 'Información de Estación':
    
    estacion = st.selectbox('Estación', sorted(df.name.unique()))
    estacion_data = df[df['name'] == estacion].iloc[0]
    
    st.subheader(f'Información de la estación {estacion}')
    col1, col2, col3 = st.columns(3)
    col1.metric("Kms de la estación", estacion_data['km_total'])
    col2.metric("Telesillas de la estación", estacion_data['lifts_total'])
    col3.metric("Precio forfait", estacion_data['forfait'])
    
    fig = px.pie(estacion_data, names=['pistas verdes', 'pistas azules', 'pistas rojas', 'pistas negras'], 
                 title=f'Desglose de pistas en la estación {estacion}',
                 values= [estacion_data['green_runs_total'], estacion_data['blue_runs_total'],
                          estacion_data['red_runs_total'], estacion_data['black_runs_total']])
    
    st.plotly_chart(fig, use_container_width=True)
    
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

elif analisis_seleccionado == 'Comparador de precios':
    
    st.subheader('Comparador de precios')
    estaciones_forfait = st.multiselect('Seleccione estaciones para comparar:', df.name.unique())
    df_filtrado = df[df.name.isin(estaciones_forfait)]
    fig = px.bar(df_filtrado, x='name', y='forfait', title='Comparación de Precios de Forfaits',
                 labels={'name': 'Estación', 'forfait': 'Precio del Forfait'})
    st.plotly_chart(fig, use_container_width=True)


elif analisis_seleccionado == 'Precio por Kilómetro':
    
    st.subheader('Precio por Kilómetro')
    df['precio_por_km'] = df['forfait'] / df['km_total']
    fig = px.line(df, x='name', y='precio_por_km',
                  labels={'name': 'Estación', 'precio_por_km':'Precio por km'})
    st.plotly_chart(fig, use_container_width=True)
    
    
elif analisis_seleccionado == 'Servicios':
    
    st.subheader('Servicios en las estaciones')
    
    snowpark = st.checkbox('snowpark')
    raquetas = st.checkbox('raquetas')
    trineos = st.checkbox('trineos')
    esqui_de_fondo = st.checkbox('esqui de fondo')

    resultado = None

    if snowpark:
        resultado = df.loc[df['snowpark'] == 1, 'name']

    if raquetas:
        resultado = df.loc[df['raquetas'] == 1, 'name']

    if trineos:
        resultado = df.loc[df['trineos'] == 1, 'name']
   
    if esqui_de_fondo:
        resultado = df.loc[df['esqui_de_fondo'] == 1, 'name']

    st.write('Resultado:', resultado)
    