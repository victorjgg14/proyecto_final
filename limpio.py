import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
df = pd.read_csv('data_infonieve.csv')
df = df.drop('id', axis=1)

# Funciones de análisis
def porcentaje_pistas_por_estacion(nombre_estacion):
    # Filtrar el DataFrame por el nombre de la estación
    estacion_df = df[df['name'] == nombre_estacion]
    
    # Calcular el total de pistas
    total_pistas = estacion_df['green_runs_total'].iloc[0] + estacion_df['blue_runs_total'].iloc[0] + estacion_df['red_runs_total'].iloc[0] + estacion_df['black_runs_total'].iloc[0]
    
    # Calcular el porcentaje de cada tipo de pista
    verde = estacion_df['green_runs_total'].iloc[0] / total_pistas * 100
    azul = estacion_df['blue_runs_total'].iloc[0] / total_pistas * 100
    roja = estacion_df['red_runs_total'].iloc[0] / total_pistas * 100
    negra = estacion_df['black_runs_total'].iloc[0] / total_pistas * 100
    
    fig, ax = plt.subplots()
    ax.pie([verde, azul, roja, negra], labels=['Verde', 'Azul', 'Roja', 'Negra'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    fig.patch.set_facecolor('none')
    
    return verde, azul, roja, negra

def main_analisis():
    
    st.header('df infonieve')
    st.text('datos reacabados desde la api de infonieve')
    st.write(df)
    
    
    st.title("Desglose de pistas por estación")
    nombre_estacion = st.selectbox("Seleccione una estación:", df['name'].unique())
    verde, azul, roja, negra = porcentaje_pistas_por_estacion(nombre_estacion)
    fig, ax = plt.subplots()
    ax.pie([verde, azul, roja, negra], labels=['Verde', 'Azul', 'Roja', 'Negra'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal') 
    st.pyplot(fig)
    
    st.header('Servicios estación')
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

def buscar_estacion():
    buscar = st.text_input("Buscar estación")
    filtrado = df[df['name'].str.contains(buscar, case=False)]
    return filtrado

# Funciones de inicio
def main_inicio():
    st.title('Bienvenido a SkiForAll')
    st.text('Aquí encontrarás información detallada de las estaciones de esquí de la península.')
   

# Main
def main():
    st.sidebar.title("Menú")
    menu_option = st.sidebar.selectbox("Seleccionar opción", ["Inicio", "Análisis"])

    if menu_option == "Inicio":
        main_inicio()
    elif menu_option == "Análisis":
        main_analisis()

if __name__ == "__main__":
    main()
