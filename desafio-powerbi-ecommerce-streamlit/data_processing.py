import pandas as pd

def process_data(df):
    # Limpa novamente as colunas para garantir
    df.columns = df.columns.str.strip()

    # Mapeamento de IDs (Desafio DIO)
    product_map = {
        'Carretera': 0, 'Montana': 1, 'Paseo': 2, 
        'Velo': 3, 'VTT': 4, 'Amarilla': 5
    }
    
    df['Product'] = df['Product'].str.strip()
    df['ID_Produto'] = df['Product'].map(product_map)
    df['SK_ID'] = range(1, len(df) + 1)

    # 1. D_Produtos
    d_produtos = df.groupby('Product').agg(
        ID_Produto=('ID_Produto', 'first'),
        Media_Unidades_Vendidas=('Units Sold', 'mean'),
        Media_Valor_Vendas=('Sale Price', 'mean'),
        Mediana_Valor_Vendas=('Sale Price', 'median'),
        Max_Venda=('Sale Price', 'max'),
        Min_Venda=('Sale Price', 'min'),
        Media_Manufatura=('Manufacturing Price', 'mean')
    ).reset_index()

    # 2. D_Produtos_Detalhes
    d_produtos_detalhes = df[['ID_Produto', 'Discount Band', 'Sale Price', 'Units Sold', 'Manufacturing Price']].copy()

    # 3. D_Descontos (Busca flexível da coluna de descontos)
    col_desc = [c for c in df.columns if 'Discount' in c and 'Band' not in c][0]
    d_descontos = df[['ID_Produto', col_desc, 'Discount Band']].copy()

    # 4. D_Calendario
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    d_calendario = pd.DataFrame({"Date": pd.date_range(min_date, max_date)})
    d_calendario['Ano'] = d_calendario['Date'].dt.year
    d_calendario['Mes'] = d_calendario['Date'].dt.month
    d_calendario['Dia_Semana'] = d_calendario['Date'].dt.day_name()

    # 5. F_Vendas
    f_vendas = df[[
        'SK_ID', 'ID_Produto', 'Product', 'Units Sold', 
        'Sale Price', 'Discount Band', 'Segment', 
        'Country', 'Profit', 'Date'
    ]].copy()

    return d_produtos, d_produtos_detalhes, d_descontos, d_calendario, f_vendas
