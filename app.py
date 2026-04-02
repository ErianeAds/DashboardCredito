import dash
from dash import dcc, html, dash_table, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np

# 1. Carregamento e Preparação dos Dados
try:
    dados_df = pd.read_excel("BASE01.CREDITO.xlsx")
except Exception as e:
    print(f"Erro ao carregar Excel: {e}. Gerando dados fictícios.")
    dados_df = pd.DataFrame({
        'regiao': ['Norte', 'Sul', 'Leste', 'Oeste'] * 20,
        'idade': np.random.randint(18, 70, 80),
        'perda': np.random.randint(50, 600, 80),
        'sexo': ['M', 'F'] * 40
    })

# Preparação de Opções para Filtros
regioes = sorted(dados_df['regiao'].unique().tolist())
dropdown_regioes = [{'label': '🌎 TODAS AS REGIÕES', 'value': '*'}] + \
                   [{'label': r, 'value': r} for r in regioes]

# Normalização de Sexo para o Dropdown (trabalhando com 'masculino'/'feminino')
sexos_brutos = sorted(dados_df['sexo'].unique().tolist())
dropdown_sexo = [{'label': '👫 AMBOS OS SEXOS', 'value': '*'}] + \
                [{'label': '♂️ Masculino' if s.lower() == 'masculino' else '♀️ Feminino' if s.lower() == 'feminino' else s, 'value': s} for s in sexos_brutos]

min_age = int(dados_df['idade'].min())
max_age = int(dados_df['idade'].max())

# 2. Inicialização do App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

# 3. Layout (Interface Premium com Quatro Visualizações)
app.layout = html.Div(className="dashboard-container", children=[
    
    # Cabeçalho
    html.Div(className="header-section", children=[
        html.H1("Dashboard de Crédito"),
        html.P("Análise preditiva e comparativa de risco financeiro")
    ]),

    # Seção de Filtros (Grid)
    dbc.Row([
        dbc.Col([
            html.Div(className="filter-card", children=[
                html.Label("Região:", className="filter-label"),
                dcc.Dropdown(id='regiao-dropdown', options=dropdown_regioes, value='*', clearable=False)
            ])
        ], width=12, md=4),
        
        dbc.Col([
            html.Div(className="filter-card", children=[
                html.Label("Sexo:", className="filter-label"),
                dcc.Dropdown(id='sexo-dropdown', options=dropdown_sexo, value='*', clearable=False)
            ])
        ], width=12, md=4),
        
        dbc.Col([
            html.Div(className="filter-card", children=[
                html.Label(f"Faixa Etária:", id="age-label", className="filter-label"),
                dcc.RangeSlider(
                    id='idade-slider',
                    min=min_age, max=max_age,
                    step=1,
                    value=[min_age, max_age],
                    marks={min_age: str(min_age), max_age: str(max_age)},
                    className="custom-slider"
                )
            ])
        ], width=12, md=4),
    ]),

    # 1. Gráfico Original: Barras Consolidado
    dbc.Row([
        dbc.Col([
            html.Div(className="graph-card animate-up", children=[
                html.H4("Idade vs Perda (Consolidado)", style={'color': '#818cf8', 'marginBottom': '1rem'}),
                dcc.Graph(id='original-bar-graph', config={'displayModeBar': False})
            ])
        ], width=12),
    ]),

    # 2. Gráfico Geral: Dispersão
    dbc.Row([
        dbc.Col([
            html.Div(className="graph-card animate-up", children=[
                html.H4("Distribuição de Risco (Dispersão)", style={'color': '#818cf8', 'marginBottom': '1rem'}),
                dcc.Graph(id='main-scatter-graph', config={'displayModeBar': False})
            ])
        ], width=12),
    ]),

    # 3. Gráficos Espelhados (M vs F)
    dbc.Row([
        dbc.Col([
            html.Div(className="graph-card animate-up", children=[
                html.H5("♂️ Perfil Masculino", style={'color': '#60a5fa', 'textAlign': 'center'}),
                dcc.Graph(id='graph-male', config={'displayModeBar': False})
            ])
        ], width=12, lg=6),
        
        dbc.Col([
            html.Div(className="graph-card animate-up", children=[
                html.H5("♀️ Perfil Feminino", style={'color': '#f472b6', 'textAlign': 'center'}),
                dcc.Graph(id='graph-female', config={'displayModeBar': False})
            ])
        ], width=12, lg=6),
    ]),

    # Tabela Final
    dbc.Row([
        dbc.Col([
            html.Div(className="table-card animate-up", children=[
                html.H4("Detalhamento dos Dados", style={'marginBottom': '1.5rem', 'color': '#c084fc'}),
                dash_table.DataTable(
                    id='tabela-credito',
                    columns=[{"name": i.title(), "id": i} for i in ['cliente', 'regiao', 'sexo', 'idade', 'perda', 'renda']],
                    data=dados_df.to_dict('records'),
                    page_size=8,
                    style_table={'overflowX': 'auto'},
                    style_header={'backgroundColor': '#0f172a', 'color': '#818cf8', 'fontWeight': 'bold'},
                    style_cell={'backgroundColor': 'transparent', 'color': '#e2e8f0', 'textAlign': 'left'},
                    style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': 'rgba(255, 255, 255, 0.02)'}],
                )
            ])
        ], width=12)
    ])
])

# 4. Lógica de Interatividade (Callbacks)
@app.callback(
    [Output('original-bar-graph', 'figure'),
     Output('main-scatter-graph', 'figure'),
     Output('graph-male', 'figure'),
     Output('graph-female', 'figure'),
     Output('tabela-credito', 'data'),
     Output('age-label', 'children')],
    [Input('regiao-dropdown', 'value'),
     Input('sexo-dropdown', 'value'),
     Input('idade-slider', 'value')]
)
def update_dashboard(regiao, sexo, faixa_idade):
    # Filtragem Base (Região e Idade)
    df = dados_df[(dados_df['idade'] >= faixa_idade[0]) & (dados_df['idade'] <= faixa_idade[1])]
    
    if regiao != "*":
        df = df[df['regiao'] == regiao]
    
    # Filtro global para o gráfico principal e tabela
    df_global = df if sexo == "*" else df[df['sexo'] == sexo]
    
    # 1. Gráfico Original: Barras (Agrupado por Idade)
    df_grouped = df_global.groupby('idade')['perda'].sum().reset_index()
    fig_bar = px.bar(
        df_grouped, x='idade', y='perda',
        color='perda', color_continuous_scale='Turbo',
        template='plotly_dark'
    )
    
    # 2. Gráfico Geral: Dispersão
    fig_scatter = px.scatter(
        df_global, x='idade', y='perda', size='perda', color='perda',
        color_continuous_scale='Viridis', template='plotly_dark'
    )
    
    # 3. Gráficos Espelhados (Comparamos Masculino vs Feminino na base Region+Age)
    def filter_by_sex(data, s_val):
        return data[data['sexo'].str.lower() == s_val.lower()]

    df_male_base = filter_by_sex(df, 'masculino')
    df_female_base = filter_by_sex(df, 'feminino')
    
    def create_small_fig(data, title, color_val):
        # Agrupamento para as barras espelhadas tbm para ficar consistente
        data_agg = data.groupby('idade')['perda'].sum().reset_index()
        fig = px.bar(data_agg, x='idade', y='perda', template='plotly_dark')
        fig.update_traces(marker_color=color_val)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=20),
            title=dict(text=title, font=dict(size=14))
        )
        return fig

    fig_male = create_small_fig(df_male_base, "Idade vs Perda (Masculino)", '#60a5fa')
    fig_female = create_small_fig(df_female_base, "Idade vs Perda (Feminino)", '#f472b6')
    
    # Formatação de fundo para todos os gráficos
    for f in [fig_bar, fig_scatter]:
        f.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    label_idade = f"Filtros Ativos | Idade: {faixa_idade[0]} - {faixa_idade[1]} anos"
    
    return fig_bar, fig_scatter, fig_male, fig_female, df_global.to_dict('records'), label_idade

# 5. Execução
if __name__ == '__main__':
    app.run(debug=True)
