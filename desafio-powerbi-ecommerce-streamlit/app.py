import streamlit as st
import pandas as pd
import os

# 1. Configuração da Página
st.set_page_config(page_title="Dashboard E-commerce", layout="wide")

# Estilização básica para melhorar o visual
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Carregamento de Dados
@st.cache_data
def load_data():
    target_file = "Financial Sample.xlsx"
    file_path = None
    # Busca o arquivo em qualquer pasta do repositório
    for root, dirs, files in os.walk("."):
        if target_file in files:
            file_path = os.path.join(root, target_file)
            break
    
    if file_path is None:
        return None

    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return None

df = load_data()

# 3. Filtros na Sidebar
st.sidebar.header("Filtros")
country_filter = st.sidebar.multiselect("Selecione o País:", options=df['Country'].unique(), default=df['Country'].unique())
df_filtered = df[df['Country'].isin(country_filter)]

# 4. KPIs (Ajustado para as colunas: Sales, Units Sold, Profit)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Vendas Totais", f"$ {df_filtered['Sales'].sum():,.2f}")
with col2:
    st.metric("Unidades Vendidas", f"{df_filtered['Units Sold'].sum():,.0f}")
with col3:
    st.metric("Lucro Total", f"$ {df_filtered['Profit'].sum():,.2f}")

# 5. Gráfico de Vendas por Produto
st.subheader("Vendas por Produto")
fig_prod = px.bar(df_filtered, x='Product', y='Sales', color='Segment', barmode='group')
st.plotly_chart(fig_prod, use_container_width=True)
