import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from main import executar_etl

# ------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide",
)

CORES = px.colors.qualitative.Set2


# ------------------------------------------------------------------
# CARREGAMENTO (cache)
# ------------------------------------------------------------------
@st.cache_data(show_spinner="Carregando e tratando dados...")
def carregar_dados():
    return executar_etl(exportar_csv=False)


dados = carregar_dados()

faturamento_total = dados["faturamento_total"]
volume_itens = dados["volume_itens"]
faturamento_loja = dados["faturamento_loja"]
ticket_medio_loja = dados["ticket_medio_loja"]
faturamento_produto = dados["faturamento_produto"]
produto_mais_vendido = dados["produto_mais_vendido"]
faturamento_diario = dados["faturamento_diario"]
faturamento_loja_produto = dados["faturamento_loja_produto"]
quantidade_produto = dados["quantidade_produto"]
tabela_original = dados["tabela_original"]


# ------------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------------
def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def numero(v):
    return f"{v:,.0f}".replace(",", ".")


# ------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------
st.title("📊 Dashboard de Vendas")
st.caption("Visão geral de faturamento, ticket médio, produtos e volume de itens.")

# ------------------------------------------------------------------
# KPIs (sempre no topo)
# ------------------------------------------------------------------
n_lojas = faturamento_loja["ID Loja"].nunique()
n_produtos = produto_mais_vendido["Produto"].nunique()
ticket_medio_geral = (
    tabela_original["Valor Final"].sum() / len(tabela_original)
    if len(tabela_original) else 0
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Faturamento Total", moeda(faturamento_total))
col2.metric("📦 Volume Total de Itens", numero(volume_itens))
col3.metric("🏬 Lojas", n_lojas)
col4.metric("🎯 Ticket Médio Geral", moeda(ticket_medio_geral))

col5, col6, col7, col8 = st.columns(4)
col5.metric("🛒 Produtos distintos", n_produtos)
col6.metric(
    "🏆 Loja Top 1",
    faturamento_loja.iloc[0]["ID Loja"] if not faturamento_loja.empty else "-",
    moeda(faturamento_loja.iloc[0]["Valor Final"]) if not faturamento_loja.empty else "",
)
col7.metric(
    "🥇 Produto Mais Vendido",
    produto_mais_vendido.iloc[0]["Produto"] if not produto_mais_vendido.empty else "-",
    f"{numero(produto_mais_vendido.iloc[0]['Quantidade'])} un" if not produto_mais_vendido.empty else "",
)
col8.metric(
    "📅 Dias com venda",
    len(faturamento_diario),
)

st.divider()

# ------------------------------------------------------------------
# ABAS
# ------------------------------------------------------------------
aba_lojas, aba_produtos, aba_tempo, aba_detalhada = st.tabs(
    ["🏬 Lojas", "🛍️ Produtos", "📅 Faturamento Diário", "📋 Tabela Detalhada"]
)


# ==================================================================
# ABA LOJAS
# ==================================================================
with aba_lojas:
    st.subheader("Análise por Loja")

    top_n = st.slider("Quantidade de lojas exibidas (Top N)", 3, max(3, n_lojas), min(10, n_lojas), key="top_lojas")
    df_lojas = faturamento_loja.head(top_n)

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            df_lojas,
            x="ID Loja",
            y="Valor Final",
            color="ID Loja",
            text_auto=".2s",
            title=f"Faturamento por Loja (Top {top_n})",
            color_discrete_sequence=CORES,
        )
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Faturamento (R$)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.pie(
            df_lojas,
            names="ID Loja",
            values="Valor Final",
            hole=0.55,
            title="Participação no Faturamento (%)",
            color_discrete_sequence=CORES,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        df_ticket = ticket_medio_loja.head(top_n)
        fig = px.bar(
            df_ticket,
            x="ID Loja",
            y="Valor Final",
            color="ID Loja",
            text_auto=".2s",
            title=f"Ticket Médio por Loja (Top {top_n})",
            color_discrete_sequence=CORES,
        )
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Ticket Médio (R$)")
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        # Donut: faturamento por loja x produto (top 5 produtos por loja)
        top_produtos_geral = (
            faturamento_loja_produto.groupby("Produto", as_index=False)["Valor Final"]
            .sum()
            .sort_values("Valor Final", ascending=False)
            .head(5)["Produto"]
            .tolist()
        )
        df_fp = faturamento_loja_produto[
            faturamento_loja_produto["Produto"].isin(top_produtos_geral)
            & faturamento_loja_produto["ID Loja"].isin(df_lojas["ID Loja"])
        ]
        fig = px.sunburst(
            df_fp,
            path=["ID Loja", "Produto"],
            values="Valor Final",
            title="Composição Loja → Produto (Top 5 produtos)",
            color_discrete_sequence=CORES,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 Tabela — Faturamento por Loja")
    st.dataframe(
        faturamento_loja.style.format({"Valor Final": "R$ {:,.2f}"}),
        use_container_width=True,
    )

    st.markdown("### 📋 Tabela — Ticket Médio por Loja")
    st.dataframe(
        ticket_medio_loja.style.format({"Valor Final": "R$ {:,.2f}"}),
        use_container_width=True,
    )


# ==================================================================
# ABA PRODUTOS
# ==================================================================
with aba_produtos:
    st.subheader("Análise de Produtos")

    top_p = st.slider(
        "Quantidade de produtos exibidos (Top N)",
        3,
        max(3, n_produtos),
        min(10, n_produtos),
        key="top_produtos",
    )
    df_prod = quantidade_produto.head(top_p)

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            df_prod.sort_values("Quantidade"),
            x="Quantidade",
            y="Produto",
            orientation="h",
            color="Produto",
            text_auto=True,
            title=f"Top {top_p} — Produtos Mais Vendidos (unidades)",
            color_discrete_sequence=CORES,
        )
        fig.update_layout(showlegend=False, yaxis_title="", xaxis_title="Quantidade")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.pie(
            df_prod,
            names="Produto",
            values="Quantidade",
            hole=0.55,
            title="Participação nas Vendas (unidades)",
            color_discrete_sequence=CORES,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        df_prod_fat = produto_mais_vendido.head(top_p)
        fig = px.bar(
            df_prod_fat.sort_values("Valor Final"),
            x="Valor Final",
            y="Produto",
            orientation="h",
            color="Produto",
            text_auto=".2s",
            title=f"Top {top_p} — Faturamento por Produto",
            color_discrete_sequence=CORES,
        )
        fig.update_layout(showlegend=False, yaxis_title="", xaxis_title="Faturamento (R$)")
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        fig = px.pie(
            df_prod_fat,
            names="Produto",
            values="Valor Final",
            hole=0.55,
            title="Participação no Faturamento por Produto",
            color_discrete_sequence=CORES,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 Tabela — Produtos Mais Vendidos")
    st.dataframe(
        produto_mais_vendido.style.format(
            {"Quantidade": "{:,.0f}", "Valor Final": "R$ {:,.2f}"}
        ),
        use_container_width=True,
    )

    st.markdown("### 📋 Tabela — Faturamento por Loja × Produto")
    st.dataframe(
        faturamento_produto.style.format(
            {"Valor Final": "R$ {:,.2f}", "Quantidade": "{:,.0f}"}
        ),
        use_container_width=True,
    )


# ==================================================================
# ABA FATURAMENTO DIÁRIO
# ==================================================================
with aba_tempo:
    st.subheader("Faturamento Diário")

    fig = px.line(
        faturamento_diario,
        x="Data",
        y="Valor Final",
        markers=True,
        title="Evolução do Faturamento Diário",
        color_discrete_sequence=["#2E86AB"],
    )
    fig.update_layout(xaxis_title="Data", yaxis_title="Faturamento (R$)")
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(
            faturamento_diario,
            x="Data",
            y="Valor Final",
            title="Faturamento por Dia (barras)",
            color_discrete_sequence=["#F18F01"],
        )
        fig.update_layout(xaxis_title="Data", yaxis_title="Faturamento (R$)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        top_dias = faturamento_diario.sort_values("Valor Final", ascending=False).head(5)
        fig = px.pie(
            top_dias,
            names="Data",
            values="Valor Final",
            hole=0.55,
            title="Top 5 Dias com Maior Faturamento",
            color_discrete_sequence=CORES,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 Tabela — Faturamento Diário")
    st.dataframe(
        faturamento_diario.style.format({"Valor Final": "R$ {:,.2f}"}),
        use_container_width=True,
    )


# ==================================================================
# ABA TABELA DETALHADA
# ==================================================================
with aba_detalhada:
    st.subheader("Tabela Detalhada (dados originais tratados)")

    # Cópia SEMPRE — nunca mexe no df cacheado
    # "Data" já vem normalizada como datetime do executar_etl(); aqui só
    # extraímos a parte de data pura, pra usar no date_input/filtro
    base = tabela_original.copy()
    base["Data"] = base["Data"].dt.date

    lojas = ["Todas"] + sorted(base["ID Loja"].dropna().unique().tolist())
    produtos = ["Todos"] + sorted(base["Produto"].dropna().unique().tolist())

    c1, c2 = st.columns(2)
    loja_sel = c1.selectbox("Filtrar por Loja", lojas, key="det_loja")
    produto_sel = c2.selectbox("Filtrar por Produto", produtos, key="det_produto")

    usar_data = st.checkbox("Filtrar por data", value=False, key="det_usar_data")

    c3, c4 = st.columns(2)
    data_min = base["Data"].min()
    data_max = base["Data"].max()
    data_ini = c3.date_input(
        "Data inicial",
        value=data_min,
        min_value=data_min,
        max_value=data_max,
        key="det_data_ini",
        disabled=not usar_data,
    )
    data_fim = c4.date_input(
        "Data final",
        value=data_max,
        min_value=data_min,
        max_value=data_max,
        key="det_data_fim",
        disabled=not usar_data,
    )

    # ---------- APLICA OS FILTROS NUMA CÓPIA NOVA ----------
    df_filtrado = base.copy()

    if loja_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["ID Loja"] == loja_sel]

    if produto_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Produto"] == produto_sel]

    if usar_data:
        df_filtrado = df_filtrado[
            (df_filtrado["Data"] >= data_ini) & (df_filtrado["Data"] <= data_fim)
        ]

    # ---------- FORMATA PRA EXIBIÇÃO ----------
    df_exibir = df_filtrado.copy()
    df_exibir["Data"] = df_exibir["Data"].astype(str)

    # ---------- RESUMO ----------
    m1, m2, m3 = st.columns(3)
    m1.metric("Registros", f"{len(df_exibir):,}".replace(",", "."))
    m2.metric("Faturamento", moeda(df_exibir["Valor Final"].sum()) if not df_exibir.empty else "R$ 0,00")
    m3.metric("Itens", numero(df_exibir["Quantidade"].sum()) if not df_exibir.empty else "0")

    # ---------- TABELA ----------
    st.dataframe(
        df_exibir.style.format({"Valor Final": "R$ {:,.2f}"}),
        use_container_width=True,
        height=500,
    )

    # ---------- CSV ----------
    csv_bytes = df_exibir.to_csv(
        index=False, sep=";", decimal=",", encoding="utf-8-sig"
    ).encode("utf-8-sig")

    st.download_button(
        "⬇️ Baixar CSV (filtrado)",
        data=csv_bytes,
        file_name="vendas_filtrado.csv",
        mime="text/csv",
        key="det_download",
    )