import streamlit as st
import pandas as pd
import plotly.express as px
import os
from data_processing import process_data

# 1. Configuração da Página
st.set_page_config(page_title="Dashboard E-commerce - Desafio DIO", layout="wide")

# Estilização CSS personalizada
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Carregamento e Processamento de Dados
@st.cache_data
def load_and_setup_data():
    # O nome do arquivo conforme carregado no ambiente
    target_file = "Financial Sample.xlsx - Sheet1.csv"
    
    if not os.path.exists(target_file):
        st.error(f"Arquivo {target_file} não encontrado!")
        return None

    try:
        # Lendo o CSV (ajustado para o arquivo fornecido)
        df = pd.read_csv(target_file)
        
        # Aplicando o processamento do arquivo data_processing.py
        df = process_data(df)
        
        # Garantir que a coluna Date seja datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        return df
    except Exception as e:
        st.error(f"Erro ao processar dados: {e}")
        return None

df = load_and_setup_data()

if df is not None:
    # 3. Sidebar - Filtros
    st.sidebar.header("🔍 Filtros")
    
    # Filtro de País
    countries = sorted(df['Country'].unique())
    country_filter = st.sidebar.multiselect("Selecione o País:", options=countries, default=countries)
    
    # Filtro de Produto
    products = sorted(df['Product'].unique())
    product_filter = st.sidebar.multiselect("Selecione o Produto:", options=products, default=products)

    # Aplicando Filtros
    mask = df['Country'].isin(country_filter) & df['Product'].isin(product_filter)
    df_filtered = df[mask]

    # 4. Cabeçalho Principal
    st.title("📊 Dashboard de Vendas E-commerce")
    st.markdown("---")

    # 5. KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    total_sales = df_filtered['Sales'].sum()
    total_profit = df_filtered['Profit'].sum()
    total_units = df_filtered['Units Sold'].sum()
    avg_discount = df_filtered['Discounts'].mean()

    with col1:
        st.metric("Vendas Totais", f"$ {total_sales:,.2f}")
    with col2:
        st.metric("Lucro Total", f"$ {total_profit:,.2f}")
    with col3:
        st.metric("Unidades Vendidas", f"{total_units:,.0f}")
    with col4:
        st.metric("Desconto Médio", f"$ {avg_discount:,.2f}")

    st.markdown("### Análises Detalhadas")
    
    row2_col1, row2_col2 = st.columns(2)

    # 6. Gráfico de Evolução Temporal
    with row2_col1:
        df_temp = df_filtered.groupby('Date')['Sales'].sum().reset_index()
        fig_date = px.line(df_temp, x='Date', y='Sales', title='Evolução de Vendas no Tempo',
                          line_shape='spline', render_mode='svg')
        st.plotly_chart(fig_date, use_container_width=True)

    # 7. Gráfico de Vendas por Produto
    with row2_col2:
        df_prod = df_filtered.groupby('Product')['Sales'].sum().sort_values(ascending=True).reset_index()
        fig_prod = px.bar(df_prod, x='Sales', y='Product', orientation='h',
                         title='Vendas por Produto', color='Sales',
                         color_continuous_scale='Blues')
        st.plotly_chart(fig_prod, use_container_width=True)

    # 8. Visão de Tabela de Dados (Opcional)
    with st.expander("Ver dados brutos filtrados"):
        st.dataframe(df_filtered)

else:
    st.info("Aguardando carregamento dos dados...")
