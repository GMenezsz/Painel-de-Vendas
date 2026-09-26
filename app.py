import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from main import executar_etl

# Configuração inicial da página com layout wide e ícone via URL externa
st.set_page_config(
    page_title="Dashboard Comercial Executivo",
    page_icon="📊",
    layout="wide",
)

# Estilização CSS moderna, responsiva e com efeito zoom suave nos cards ao passar o mouse
st.markdown(
    """
    <style>
    .main {
        background-color: #F8FAFC;
    }
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-align: center;
        margin-bottom: 15px;
    }
    .kpi-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #CBD5E1;
    }
    .kpi-title {
        font-size: 14px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 700;
        color: #0F172A;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# --- FUNÇÕES DE GRÁFICOS INTEGRADAS (Com dragmode="pan" para movimentação livre) ---
def criar_grafico_linhas(df_diario):
    fig = px.line(
        df_diario,
        x="Data",
        y="Valor Final",
        title="Tendência de Faturamento Diário ao Longo do Tempo",
        markers=True,
        color_discrete_sequence=["#2563EB"],
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        margin=dict(l=20, r=20, t=50, b=20),
        dragmode="pan",  # Permite mover o gráfico ao arrastar o mouse
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#E5E7EB")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#E5E7EB")
    return fig


def criar_grafico_barras(df_loja):
    fig = px.bar(
        df_loja,
        x="ID Loja",
        y="Valor Final",
        title="Comparativo de Faturamento por Loja",
        text_auto=".2s",
        color="ID Loja",
        color_discrete_sequence=px.colors.qualitative.Prism,
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        dragmode="pan",  # Permite mover o gráfico ao arrastar o mouse
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#E5E7EB")
    return fig


def criar_grafico_rosca(df_loja):
    """Gera um Gráfico de Rosca (Donut Chart) para participação de faturamento por loja."""
    fig = px.pie(
        df_loja,
        names="ID Loja",
        values="Valor Final",
        title="Participação Percentual de Faturamento por Loja",
        hole=0.4,  # Transforma o gráfico de pizza em rosca
        color_discrete_sequence=px.colors.qualitative.Prism,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        margin=dict(l=20, r=20, t=50, b=20),
        dragmode="pan",  # Permite mover o gráfico ao arrastar o mouse
    )
    return fig


def criar_grafico_barras_horizontal(df_produto):
    fig = px.bar(
        df_produto,
        x="Quantidade",
        y="Produto",
        orientation="h",
        title="Quantidade Vendida por Produto",
        text_auto=True,
        color="Produto",
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        dragmode="pan",  # Permite mover o gráfico ao arrastar o mouse
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#E5E7EB")
    fig.update_yaxes(showgrid=False, categoryorder="total ascending")
    return fig


# Função cacheada para carregar os dados do ETL com eficiência
@st.cache_data
def carregar_dados():
    return executar_etl(caminho_excel="Vendas.xlsx", exportar_csv=True)


dados = carregar_dados()

df_original = dados["tabela_original"]
faturamento_total = dados["faturamento_total"]
volume_itens = dados["volume_itens"]
df_loja = dados["faturamento_loja"]
df_diario = dados["faturamento_diario"]
df_produto = dados["produto_mais_vendido"]

# --- CABEÇALHO DO APLICATIVO ---
st.title(" Dashboard Analítico de Desempenho Comercial")
st.markdown("Painel interativo estruturado com arquitetura unificada e limpa.")

# --- CARDS DE KPI INDIVIDUAIS COM ZOOM SUAVE AO PASSAR O MOUSE ---
st.markdown("### 📌 Indicadores de Destaque (KPIs)")
col1, col2, col3, col4 = st.columns(4)

ticket_medio_geral = df_original["Valor Final"].mean()

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Faturamento Total</div>
            <div class="kpi-value">R$ {faturamento_total:,.2f}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Volume de Itens</div>
            <div class="kpi-value">{volume_itens:,} un</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Ticket Médio Geral</div>
            <div class="kpi-value">R$ {ticket_medio_geral:,.2f}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col4:
    total_pedidos = len(df_original)
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total de Transações</div>
            <div class="kpi-value">{total_pedidos:,}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# --- NAVEGAÇÃO POR CLIQUES (st.pills) ---
opcoes_disponiveis = [
    "🌐 Visão Global (Resumo Geral)",
    "📈 Linha do Tempo (Faturamento Diário)",
    "📉 Comparativo por Lojas",
    "🔴 Participação por Lojas",
    "📊 Ranking de Produtos",
]

opcao_menu = st.pills(
    "Selecione a visão:",
    options=opcoes_disponiveis,
    default=opcoes_disponiveis[0],
    label_visibility="collapsed",
)

st.markdown("---")

# --- RENDERIZAÇÃO DINÂMICA DA PÁGINA ESCOLHIDA ---
if opcao_menu == "🌐 Visão Global (Resumo Geral)":
    st.subheader("🌐 Visão Geral do Ecossistema de Vendas")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(criar_grafico_linhas(df_diario), width="stretch")
    with c2:
        st.plotly_chart(criar_grafico_barras(df_loja), width="stretch")

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(criar_grafico_rosca(df_loja), width="stretch")
    with c4:
        st.plotly_chart(
            criar_grafico_barras_horizontal(df_produto), width="stretch"
        )

    st.subheader("📋 Tabela Consolidada (Base Original Tratada)")
    st.dataframe(df_original, width="stretch", height=350)

    csv_geral = df_original.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Baixar Dados Completos Tratados (CSV)",
        data=csv_geral,
        file_name="dados_completos_tratados.csv",
        mime="text/csv",
    )

elif opcao_menu == "📈 Linha do Tempo (Faturamento Diário)":
    st.subheader("📈 Análise Temporal: Faturamento Diário")
    st.plotly_chart(criar_grafico_linhas(df_diario), width="stretch")

    st.markdown("### 📋 Tabela de Faturamento por Dia")
    st.dataframe(df_diario, width="stretch")

    csv_diario = df_diario.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Baixar Dados de Faturamento Diário (CSV)",
        data=csv_diario,
        file_name="faturamento_diario.csv",
        mime="text/csv",
    )

elif opcao_menu == "📉 Comparativo por Lojas":
    st.subheader("📉 Comparativo de Performance por Loja")
    st.plotly_chart(criar_grafico_barras(df_loja), width="stretch")

    st.markdown("### 📋 Tabela de Faturamento por Loja")
    st.dataframe(df_loja, width="stretch")

    csv_loja = df_loja.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Baixar Dados de Lojas (CSV)",
        data=csv_loja,
        file_name="Faturamento_por_loja.csv",
        mime="text/csv",
    )

elif opcao_menu == "🔴 Participação por Lojas":
    st.subheader("🔴 Participação Percentual do Faturamento por Loja")
    st.plotly_chart(criar_grafico_rosca(df_loja), width="stretch")

    st.markdown("### 📋 Tabela de Faturamento por Loja")
    st.dataframe(df_loja, width="stretch")

    csv_loja_rosca = df_loja.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Baixar Dados de Participação por Loja (CSV)",
        data=csv_loja_rosca,
        file_name="participacao_faturamento_loja.csv",
        mime="text/csv",
    )

elif opcao_menu == "📊 Ranking de Produtos":
    st.subheader("📊 Ranking de Produtos por Quantidade Vendida")
    st.plotly_chart(
        criar_grafico_barras_horizontal(df_produto), width="stretch"
    )

    st.markdown("### 📋 Tabela Consolidada por Produtos")
    st.dataframe(df_produto, width="stretch")

    csv_produto = df_produto.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Baixar Dados de Produtos (CSV)",
        data=csv_produto,
        file_name="Faturamento_produto.csv",
        mime="text/csv",
    )
