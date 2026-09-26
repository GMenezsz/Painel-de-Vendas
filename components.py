"""
Camada de gráficos — Plotly puro.
Nenhuma dependência de Streamlit. Cada função recebe DataFrames e
retorna uma plotly.graph_objects.Figure.

Ferramentas disponíveis nos gráficos:
  - Pan (mover)     → modo padrão
  - Zoom (área/in/out)
  - Fullscreen
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ---------- Layout comum ----------
_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", size=12, color="#334155"),
    margin=dict(l=20, r=20, t=50, b=20),
    hoverlabel=dict(
        bgcolor="#0F172A", font_color="#F8FAFC", bordercolor="#0F172A",
    ),
    dragmode="pan",   # pan como prioridade
)

_PALETA = ["#2563EB", "#06B6D4", "#8B5CF6", "#F59E0B",
           "#EF4444", "#10B981", "#EC4899"]


# ============================================================
# 1. LINHA — Tendência temporal
# ============================================================
def grafico_linha_faturamento(df_diario: pd.DataFrame) -> go.Figure:
    fig = px.line(
        df_diario, x="Data", y="Valor Final",
        title="Tendência de Faturamento Diário",
        markers=True,
        color_discrete_sequence=["#2563EB"],
    )
    fig.update_traces(
        line=dict(width=3, shape="spline"),
        marker=dict(size=8, line=dict(width=2, color="#FFFFFF")),
        fill="tozeroy",
        fillcolor="rgba(37, 99, 235, 0.10)",
        hovertemplate="<b>%{x|%d/%m/%Y}</b><br>R$ %{y:,.2f}<extra></extra>",
    )
    fig.update_layout(**_LAYOUT, hovermode="x unified")
    fig.update_xaxes(showgrid=False, linecolor="#E2E8F0", fixedrange=False)
    fig.update_yaxes(showgrid=True, gridcolor="#F1F5F9", zeroline=False,
                     fixedrange=False)
    return fig


# ============================================================
# 2. BARRAS VERTICAIS — Comparação por loja (cores vivas)
# ============================================================
def grafico_barras_lojas(df_loja: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_loja, x="ID Loja", y="Valor Final",
        title="Comparativo de Faturamento por Loja",
        text_auto=".2s",
        color="ID Loja",
        color_discrete_sequence=["#1D4ED8", "#2563EB", "#3B82F6",
                                 "#06B6D4", "#0891B2", "#8B5CF6",
                                 "#7C3AED"],
    )
    fig.update_traces(
        textposition="outside",
        marker=dict(line=dict(width=0), cornerradius=6),
        hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>",
        cliponaxis=False,
    )
    fig.update_layout(**_LAYOUT, showlegend=False)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#F1F5F9", zeroline=False,
                     fixedrange=False)
    return fig


# ============================================================
# 3. ROSCA — Participação percentual por loja
# ============================================================
def grafico_rosca_lojas(df_loja: pd.DataFrame) -> go.Figure:
    fig = px.pie(
        df_loja, names="ID Loja", values="Valor Final",
        title="Participação Percentual de Faturamento por Loja",
        hole=0.62,
        color_discrete_sequence=_PALETA,
    )
    fig.update_traces(
        textposition="outside", textinfo="percent",
        textfont=dict(size=13, color="#0F172A"),
        marker=dict(line=dict(color="#FFFFFF", width=3)),
        hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
    )
    fig.update_layout(
        **_LAYOUT,
        legend=dict(orientation="h", y=-0.05, x=0.5, xanchor="center"),
    )
    return fig


# ============================================================
# 4. BARRAS HORIZONTAIS — Ranking de produtos (cores vivas)
# ============================================================
def grafico_barras_produtos(df_produto: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_produto, x="Quantidade", y="Produto", orientation="h",
        title="Ranking de Produtos por Quantidade Vendida",
        text_auto=True,
        color="Produto",
        color_discrete_sequence=["#4338CA", "#4F46E5", "#6366F1",
                                 "#8B5CF6", "#A855F7", "#EC4899",
                                 "#F43F5E", "#F59E0B", "#10B981",
                                 "#06B6D4"],
    )
    fig.update_traces(
        textposition="outside",
        marker=dict(cornerradius=6),
        hovertemplate="<b>%{y}</b><br>%{x:,} un<extra></extra>",
        cliponaxis=False,
    )
    fig.update_layout(**_LAYOUT, showlegend=False)
    fig.update_xaxes(showgrid=True, gridcolor="#F1F5F9", fixedrange=False)
    fig.update_yaxes(showgrid=False, categoryorder="total ascending",
                     fixedrange=False)
    return fig


# ============================================================
# REGISTRO CENTRAL
# ============================================================
GRAFICOS = {
    "📈 Tendência Diária":       grafico_linha_faturamento,
    "🏬 Ranking de Lojas":       grafico_barras_lojas,
    "🔵 Participação por Loja":  grafico_rosca_lojas,
    "🏆 Ranking de Produtos":    grafico_barras_produtos,
}


def construir(nome: str, dados: dict) -> go.Figure:
    if nome == "📈 Tendência Diária":
        return grafico_linha_faturamento(dados["faturamento_diario"])
    if nome == "🏬 Ranking de Lojas":
        return grafico_barras_lojas(dados["faturamento_loja"])
    if nome == "🔵 Participação por Loja":
        return grafico_rosca_lojas(dados["faturamento_loja"])
    if nome == "🏆 Ranking de Produtos":
        return grafico_barras_produtos(dados["produto_mais_vendido"])
    raise ValueError(f"Gráfico desconhecido: {nome}")
