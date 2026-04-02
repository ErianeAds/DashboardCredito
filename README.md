# 📊 Dashboard Savino - Análise de Crédito

Dashboard interativo desenvolvido em **Python** para análise de crédito, risco e performance demográfica. Este projeto oferece duas versões: uma em **Streamlit** (ideal para deploy rápido e visualizações dinâmicas) e outra em **Dash** (para controle total do layout).

---

### 🚀 Acesse Online (Streamlit Cloud)
O dashboard está disponível em:  
👉 [https://eriane-dashboardcredito.streamlit.app/](https://eriane-dashboardcredito.streamlit.app/)

---

### ✨ Funcionalidades
- **Filtros Dinâmicos**: Filtragem por Região, Sexo e Faixa Etária.
- **Painel de Métricas**: Visualização em tempo real de Total de Clientes, Perda Total, Idade Média e Renda Média.
- **Visualizações**:
  - **Gráfico de Barras Consolidado**: Análise de Idade vs Perda.
  - **Gráfico de Dispersão**: Distribuição de risco por perfil.
  - **Gráficos Espelhados**: Comparativo de performance por Gênero (Masculino vs Feminino).
- **Interface Premium**: Design com tema escuro (Dark Mode) e efeitos de *glassmorphism*.

---

### 🛠️ Instalação e Uso Local

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/SEU-USUARI/dashboardcredito.git
   cd dashboardcredito
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Para rodar a versão Streamlit:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Para rodar a versão Dash:**
   ```bash
   python app.py
   ```

---

### 📁 Estrutura do Projeto
- `streamlit_app.py`: Versão do dashboard em Streamlit (Recomendado para produção).
- `app.py`: Versão do dashboard em Dash.
- `requirements.txt`: Lista de dependências do Python.
- `BASE01.CREDITO.xlsx`: Fonte de dados em Excel.
- `assets/`: Pasta contendo estilos e imagens (CSS customizado).

---

### 💡 Autora: Eriane Savino
Este projeto foi desenvolvido focado em demonstrar o poder da análise de dados unida a um design moderno e intuitivo.
