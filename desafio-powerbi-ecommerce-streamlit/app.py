import streamlit as st
import pandas as pd
import plotly.express as px
import os
from data_processing import process_data

# 1. Configuração da Página
st.set_page_config(page_title="Dashboard E-commerce - Desafio DIO", layout="wide")

# 2. Função para carregar os dados (Busca flexível)
@st.cache_data
def load_and_setup_data():
    # Lista de possíveis nomes de arquivo que você pode estar usando
    possible_files = [
        "Financial Sample.xlsx - Sheet1.csv", 
        "Financial Sample.csv",
        "Financial Sample.xlsx"
    ]
    
    file_path = None
    for f in possible_files:
        if os.path.exists(f):
            file_path = f
            break
    
    if file_path is None:
        st.error("❌ Arquivo de dados não encontrado! Verifique se o arquivo está na mesma pasta que este script.")
        return None

    try:
        # Verifica se é CSV ou Excel e lê corretamente
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path, engine='openpyxl')
        
        # Limpeza básica de nomes de colunas (remove espaços extras)
        df.columns = df.columns.str.strip()
        
        # Aplicando o seu processamento do data_processing.py
        df = process_data(df)
        
        # Garantir que a coluna Date seja datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        return df
    except Exception as e:
        st.error(f"Erro ao processar dados: {e}")
        return None

# Execução do carregamento
df = load_and_setup_data()

if df is not None:
    # 3. Sidebar - Filtros
    st.sidebar.header("🔍 Filtros")
    
    countries = sorted(df['Country'].unique())
    country_filter = st.sidebar.multiselect("Selecione o País:", options=countries, default=countries)
    
    products = sorted(df['Product'].unique())
    product_filter = st.sidebar.multiselect("Selecione o Produto:", options=products, default=products)

    # Aplicando Filtros
    df_filtered = df[df['Country'].isin(country_filter) & df['Product'].isin(product_filter)]

    # 4. Cabeçalho Principal
    st.title("📊 Dashboard de Vendas E-commerce")
    st.markdown("---")

    # 5. KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Vendas Totais", f"$ {df_filtered['Sales'].sum():,.2f}")
    with col2:
        st.metric("Lucro Total", f"$ {df_filtered['Profit'].sum():,.2f}")
    with col3:
        st.metric("Unidades Vendidas", f"{df_filtered['Units Sold'].sum():,.0f}")
    with col4:
        # Coluna ' Sales' (com espaço) ou 'Sales' dependendo do CSV
        sales_col = ' Sales' if ' Sales' in df_filtered.columns else 'Sales'
        st.metric("Ticket Médio", f"$ {df_filtered[sales_col].mean():,.2f}")

    # 6. Gráficos
    c1, c2 = st.columns(2)
    
    with c1:
        df_temp = df_filtered.groupby('Date')[['Sales']].sum().reset_index()
        fig_date = px.line(df_temp, x='Date', y='Sales', title='Tendência de Vendas')
        st.plotly_chart(fig_date, use_container_width=True)

    with c2:
        fig_prod = px.pie(df_filtered, values='Sales', names='Product', title='Distribuição por Produto')
        st.plotly_chart(fig_prod, use_container_width=True)

    # 7. Tabela
    st.dataframe(df_filtered.head(10), use_container_width=True)
