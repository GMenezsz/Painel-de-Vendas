import plotly.express as px
import plotly.graph_objects as go


def criar_grafico_linhas(df_diario):
  """Gera um Line Chart para faturamento ao longo do tempo."""
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
  )
  fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#E5E7EB")
  fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#E5E7EB")
  return fig


def criar_grafico_barras(df_loja):
  """Gera um Bar Chart para comparações diretas de vendas por loja."""
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
  )
  fig.update_xaxes(showgrid=False)
  fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#E5E7EB")
  return fig


def criar_grafico_barras_horizontal(df_produto):
  """Gera um Gráfico de Colunas/Barras na Horizontal para Produtos."""
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
  )
  fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#E5E7EB")
  fig.update_yaxes(showgrid=False, categoryorder="total ascending")
  return fig
