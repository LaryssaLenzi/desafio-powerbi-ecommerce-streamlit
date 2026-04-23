import streamlit as st
import pandas as pd
import plotly.express as px
import os
from data_processing import process_data

# Configuração da página
st.set_page_config(page_title="Dashboard E-commerce", layout="wide")

@st.cache_data
def load_data():
    # O nome do arquivo exatamente como está no seu GitHub
    file_name = "Financial Sample.xlsx - Sheet1.csv"
    
    if not os.path.exists(file_name):
        st.error(f"Arquivo {file_name} não encontrado!")
        return None

    try:
        # Lendo o CSV e limpando nomes de colunas
        df = pd.read_csv(file_name)
        df.columns = df.columns.str.strip()
        
        # Aplicando as transformações do seu data_processing.py
        df = process_data(df)
        
        # Garantindo que a data seja reconhecida
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

df = load_data()

if df is not None:
    st.title("📊 Dashboard de Vendas E-commerce")
    
    # Sidebar
    st.sidebar.header("Filtros")
    paises = st.sidebar.multiselect("País", options=df['Country'].unique(), default=df['Country'].unique())
    
    df_filtrado = df[df['Country'].isin(paises)]

    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Vendas Totais", f"$ {df_filtrado['Sales'].sum():,.2f}")
    c2.metric("Lucro Total", f"$ {df_filtrado['Profit'].sum():,.2f}")
    c3.metric("Unidades Vendidas", f"{df_filtrado['Units Sold'].sum():,.0f}")

    # Gráfico
    fig = px.line(df_filtrado.groupby('Date')['Sales'].sum().reset_index(), 
                  x='Date', y='Sales', title="Evolução de Vendas")
    st.plotly_chart(fig, use_container_width=True)
