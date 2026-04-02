import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Configuração da Página
st.set_page_config(
    page_title="Dashboard Savino | Streamlit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização Customizada via Markdown
st.markdown("""
<style>
    /* Fundo principal */
    .main {
        background-color: #0f172a;
    }
    
    /* Estilização dos Cards de Métricas */
    [data-testid="stMetric"] {
        background-color: rgba(30, 41, 59, 1);
        padding: 20px !important;
        border-radius: 15px;
        border-left: 5px solid #818cf8;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-left: 5px solid #ec4899;
    }

    /* Garantir que o texto caiba (responsividade de fontes) */
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        color: #94a3b8 !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
    }

    h1, h2, h3 {
        color: #0f6ecd !important;
    }
</style>
""", unsafe_allow_html=True)

# 1. Carregamento de Dados com Cache
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("BASE01.CREDITO.xlsx")
    except Exception:
        # Dummy data se falhar
        df = pd.DataFrame({
            'regiao': ['Norte', 'Sul', 'Leste', 'Oeste'] * 25,
            'idade': np.random.randint(18, 70, 100),
            'perda': np.random.randint(50, 800, 100),
            'sexo': ['masculino', 'feminino'] * 50,
            'cliente': [f'Cliente {i}' for i in range(100)],
            'renda': np.random.randint(2000, 15000, 100)
        })
    return df

df = load_data()

# 2. Sidebar - Filtros
st.sidebar.header("🛠️ Painel de Filtros")

regioes = ["🌎 TODAS"] + sorted(df['regiao'].unique().tolist())
regiao_sel = st.sidebar.selectbox("Selecione a Região", regioes)

sexos = ["👫 TODOS"] + sorted(df['sexo'].unique().tolist())
sexo_sel = st.sidebar.selectbox("Selecione o Sexo", sexos)

idade_min, idade_max = int(df['idade'].min()), int(df['idade'].max())
faixa_idade = st.sidebar.slider("Selecione a Faixa Etária", idade_min, idade_max, (idade_min, idade_max))

# 3. Lógica de Filtragem
df_filt = df[(df['idade'] >= faixa_idade[0]) & (df['idade'] <= faixa_idade[1])]

if regiao_sel != "🌎 TODAS":
    df_filt = df_filt[df_filt['regiao'] == regiao_sel]

# Base para os gráficos espelhados (antes do filtro de sexo)
df_base_espelhada = df_filt.copy()

if sexo_sel != "👫 TODOS":
    df_filt = df_filt[df_filt['sexo'] == sexo_sel]

# 4. Conteúdo Principal
st.title("📊 Dashboard de Crédito (Streamlit)")
st.caption("Análise de performance financeira e perfil de risco em tempo real")

# Métricas Principais
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total Clientes", f"{len(df_filt)}")
with m2:
    st.metric("Perda Total", f"R$ {df_filt['perda'].sum():,.2f}")
with m3:
    st.metric("Idade Média", f"{df_filt['idade'].mean():.1f} anos")
with m4:
    st.metric("Renda Média", f"R$ {df_filt['renda'].mean():,.2f}")

st.markdown("---")

# 1º Gráfico: Barras Consolidado
st.subheader("1. Idade vs Perda (Consolidado)")
df_bar = df_filt.groupby('idade')['perda'].sum().reset_index()
fig_bar = px.bar(df_bar, x='idade', y='perda', color='perda', 
                 color_continuous_scale='Turbo', template='plotly_dark')
fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_bar, use_container_width=True)

# 2º Gráfico: Dispersão
st.subheader("2. Distribuição de Risco (Dispersão)")
fig_scatter = px.scatter(df_filt, x='idade', y='perda', size='perda', color='perda',
                        color_continuous_scale='Viridis', template='plotly_dark')
fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_scatter, use_container_width=True)

# 3º Gráficos Espelhados
st.subheader("3. Comparativo por Gênero")
c1, c2 = st.columns(2)

with c1:
    st.markdown("♂️ **Perfil Masculino**")
    m_data = df_base_espelhada[df_base_espelhada['sexo'].str.lower() == 'masculino'].groupby('idade')['perda'].sum().reset_index()
    fig_m = px.bar(m_data, x='idade', y='perda', template='plotly_dark')
    fig_m.update_traces(marker_color='#60a5fa')
    fig_m.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350)
    st.plotly_chart(fig_m, use_container_width=True)

with c2:
    st.markdown("♀️ **Perfil Feminino**")
    f_data = df_base_espelhada[df_base_espelhada['sexo'].str.lower() == 'feminino'].groupby('idade')['perda'].sum().reset_index()
    fig_f = px.bar(f_data, x='idade', y='perda', template='plotly_dark')
    fig_f.update_traces(marker_color='#f472b6')
    fig_f.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350)
    st.plotly_chart(fig_f, use_container_width=True)

# Tabela Detailada
with st.expander("📂 Visualizar Dados Detalhados"):
    st.dataframe(df_filt, use_container_width=True)
