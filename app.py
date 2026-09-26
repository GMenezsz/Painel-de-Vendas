"""
Dashboard Analítico de Desempenho Comercial
--------------------------------------------
Streamlit + CSS + layout.
  main.py        → ETL (dados tratados)
  components.py  → Figuras Plotly (retorna Figure)
"""
import io
import pandas as pd
import streamlit as st

from main import executar_etl
from components import GRAFICOS, construir


# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="Dashboard Comercial Executivo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CSS — Tema moderno
# ============================================================
def injetar_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background:
                radial-gradient(1200px 600px at 100% -10%, rgba(37,99,235,.06), transparent),
                radial-gradient(900px 500px at -10% 10%, rgba(6,182,212,.05), transparent),
                #F8FAFC;
        }

        .main .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* ---------- HERO ---------- */
        .hero {
            position: relative;
            background: linear-gradient(120deg, #0F172A 0%, #1E3A8A 55%, #2563EB 100%);
            border-radius: 24px;
            padding: 2.4rem 2.6rem;
            color: #FFFFFF;
            overflow: hidden;
            box-shadow: 0 20px 45px -22px rgba(30,58,138,.65);
            margin-bottom: 1.8rem;
        }
        .hero::before {
            content: ""; position: absolute; inset: 0;
            background:
                radial-gradient(600px 300px at 90% 10%, rgba(6,182,212,.35), transparent),
                radial-gradient(500px 260px at 10% 100%, rgba(139,92,246,.25), transparent);
            pointer-events: none;
        }
        .hero h1 {
            position: relative; margin: 0;
            font-size: 1.95rem; font-weight: 800;
            letter-spacing: -.025em;
        }
        .hero p {
            position: relative; margin: .5rem 0 0;
            font-size: .98rem; opacity: .9; max-width: 780px;
            line-height: 1.55;
        }

        /* ---------- KPI CARDS ---------- */
        .kpi-card {
            position: relative;
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 18px;
            padding: 1.15rem 1.25rem;
            box-shadow: 0 4px 10px -4px rgba(15,23,42,.06);
            transition: transform .28s cubic-bezier(.2,.8,.2,1),
                        box-shadow .28s ease, border-color .28s ease;
            height: 100%; overflow: hidden;
        }
        .kpi-card::after {
            content: ""; position: absolute;
            top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, #2563EB, #06B6D4);
            opacity: 0; transition: opacity .28s ease;
        }
        .kpi-card:hover {
            transform: translateY(-4px) scale(1.025);
            box-shadow: 0 20px 32px -18px rgba(37,99,235,.45);
            border-color: #BFDBFE;
        }
        .kpi-card:hover::after { opacity: 1; }

        .kpi-top {
            display: flex; justify-content: space-between;
            align-items: center; margin-bottom: .65rem;
        }
        .kpi-label {
            font-size: .72rem; font-weight: 700; color: #64748B;
            text-transform: uppercase; letter-spacing: .07em;
        }
        .kpi-icon {
            font-size: 1rem; background: #EFF6FF; border-radius: 10px;
            width: 32px; height: 32px; display: grid; place-items: center;
        }
        .kpi-value {
            font-size: 1.55rem; font-weight: 800; color: #0F172A;
            letter-spacing: -.02em; line-height: 1.15;
        }
        .kpi-foot {
            font-size: .74rem; color: #94A3B8;
            margin-top: .35rem; font-weight: 500;
        }

        /* ---------- PILLS ---------- */
        div[data-testid="stPills"] button {
            border-radius: 999px !important;
            border: 1px solid #E2E8F0 !important;
            background: #FFFFFF !important;
            font-weight: 600 !important;
            color: #334155 !important;
            padding: .45rem 1rem !important;
            transition: all .22s ease;
        }
        div[data-testid="stPills"] button:hover {
            border-color: #93C5FD !important;
            color: #1D4ED8 !important;
            transform: translateY(-1px);
        }
        div[data-testid="stPills"] button[aria-checked="true"],
        div[data-testid="stPills"] button[kind="pillsActive"] {
            background: linear-gradient(120deg, #1D4ED8, #2563EB) !important;
            color: #FFFFFF !important;
            border-color: transparent !important;
            box-shadow: 0 8px 18px -10px rgba(37,99,235,.75);
        }

        /* ---------- SEÇÕES ---------- */
        .section-title {
            font-size: 1.15rem; font-weight: 700; color: #0F172A;
            margin: 1.4rem 0 .35rem; letter-spacing: -.01em;
        }
        .section-sub {
            font-size: .85rem; color: #64748B; margin-bottom: 1rem;
        }

        /* ---------- DATAFRAME ---------- */
        [data-testid="stDataFrame"] {
            border-radius: 14px; overflow: hidden;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 12px -8px rgba(15,23,42,.08);
        }

        /* ---------- DOWNLOAD ---------- */
        [data-testid="stDownloadButton"] button {
            background: #FFFFFF; color: #1D4ED8;
            border: 1.5px solid #BFDBFE; border-radius: 12px;
            padding: .55rem 1rem; font-weight: 600;
            transition: all .22s ease; width: 100%;
        }
        [data-testid="stDownloadButton"] button:hover {
            background: linear-gradient(120deg, #1D4ED8, #2563EB);
            color: #FFFFFF; border-color: transparent;
            transform: translateY(-2px);
            box-shadow: 0 10px 22px -12px rgba(37,99,235,.75);
        }

        /* ---------- RESPONSIVO ---------- */
        @media (max-width: 900px) {
            .hero { padding: 1.6rem 1.4rem; border-radius: 18px; }
            .hero h1 { font-size: 1.4rem; }
            .hero p { font-size: .85rem; }
            .kpi-value { font-size: 1.2rem; }
            .main .block-container { padding: 1rem 1rem 2rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


injetar_css()


# ============================================================
# CONFIG PLOTLY — apenas pan, zoom e fullscreen
# (scroll do mouse NÃO dá zoom)
# ============================================================
PLOTLY_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "scrollZoom": False,          # << scroll não dá zoom
    "doubleClick": "reset",
    "responsive": True,
    "modeBarButtonsToRemove": [
        "select2d", "lasso2d", "autoScale2d", "toggleSpikelines",
        "hoverClosestCartesian", "hoverCompareCartesian",
        "sendDataToCloud", "toImage",
    ],
}


# ============================================================
# HELPERS
# ============================================================
def fmt_moeda(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_int(v: float) -> str:
    return f"{int(v):,}".replace(",", ".")


def to_csv(df: pd.DataFrame) -> bytes:
    buf = io.StringIO()
    df.to_csv(buf, index=False, sep=";", decimal=",")
    return buf.getvalue().encode("utf-8-sig")


def titulo_secao(titulo: str, subtitulo: str = "") -> None:
    sub = f'<div class="section-sub">{subtitulo}</div>' if subtitulo else ""
    st.markdown(f'<div class="section-title">{titulo}</div>{sub}',
                unsafe_allow_html=True)


def renderizar_tabela(df: pd.DataFrame, altura: int = 380) -> None:
    st.dataframe(df, use_container_width=True, hide_index=True, height=altura)


def renderizar_download(df: pd.DataFrame, nome: str) -> None:
    st.download_button(
        label=f"⬇️ Baixar {nome}.csv",
        data=to_csv(df),
        file_name=f"{nome}.csv",
        mime="text/csv",
        use_container_width=True,
        key=f"dl_{nome}",
    )


def renderizar_grafico(nome: str, dados: dict, key: str) -> None:
    fig = construir(nome, dados)
    st.plotly_chart(
        fig,
        use_container_width=True,
        config=PLOTLY_CONFIG,
        key=key,
    )


# ============================================================
# HEADER (sem badge, com nova mensagem)
# ============================================================
st.markdown(
    """
    <div class="hero">
        <h1>Dashboard Analítico de Desempenho Comercial</h1>
        <p>Visão unificada de faturamento, produtos e lojas — arquitetura modular,
        dados tratados via ETL e foco total em decisão rápida.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DADOS (cache)
# ============================================================
@st.cache_data(show_spinner=False)
def carregar_dados() -> dict:
    return executar_etl(caminho_excel="Vendas.xlsx", exportar_csv=False)


try:
    dados = carregar_dados()
except FileNotFoundError:
    st.error("❌ Arquivo `Vendas.xlsx` não encontrado na raiz do projeto.")
    st.stop()


# ============================================================
# KPIs
# ============================================================
df = dados["tabela_original"]
total = dados["faturamento_total"]
itens = dados["volume_itens"]
ticket = df["Valor Final"].mean()
pedidos = len(df)

kpi_defs = [
    ("💰", "Faturamento Total", fmt_moeda(total),
     f"{len(dados['faturamento_loja'])} lojas ativas"),
    ("📦", "Volume de Itens", f"{fmt_int(itens)} un",
     f"média {itens / max(pedidos, 1):.1f} un/venda"),
    ("🎯", "Ticket Médio", fmt_moeda(ticket), "por transação"),
    ("🧾", "Transações", fmt_int(pedidos), "registros processados"),
]

cols = st.columns(4, gap="medium")
for col, (icon, label, value, foot) in zip(cols, kpi_defs):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-top">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-icon">{icon}</div>
                </div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-foot">{foot}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)


# ============================================================
# NAVEGAÇÃO
# ============================================================
opcoes = ["🌐 Visão Global"] + list(GRAFICOS.keys())
escolha = st.pills(
    "Selecione a visão",
    options=opcoes,
    default=opcoes[0],
    label_visibility="collapsed",
    selection_mode="single",
) or opcoes[0]

st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)


# ============================================================
# MAPA: gráfico → (título, df, nome do CSV)
# ============================================================
MAPA = {
    "📈 Tendência Diária": (
        "📈 Análise Temporal: Faturamento Diário",
        lambda: dados["faturamento_diario"],
        "faturamento_diario",
    ),
    "🏬 Ranking de Lojas": (
        "🏬 Comparativo de Performance por Loja",
        lambda: dados["faturamento_loja"],
        "faturamento_por_loja",
    ),
    "🔵 Participação por Loja": (
        "🔵 Participação Percentual do Faturamento por Loja",
        lambda: dados["faturamento_loja"],
        "participacao_faturamento_loja",
    ),
    "🏆 Ranking de Produtos": (
        "🏆 Ranking de Produtos por Quantidade Vendida",
        lambda: dados["produto_mais_vendido"],
        "faturamento_produto",
    ),
}


# ============================================================
# RENDERIZAÇÃO
# ============================================================
if escolha == "🌐 Visão Global":
    titulo_secao(
        "🌐 Visão Geral do Ecossistema de Vendas",
        "Todos os indicadores consolidados em um único painel.",
    )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        renderizar_grafico("📈 Tendência Diária", dados, key="ov_line")
    with c2:
        renderizar_grafico("🏬 Ranking de Lojas", dados, key="ov_bar")

    c3, c4 = st.columns(2, gap="large")
    with c3:
        renderizar_grafico("🔵 Participação por Loja", dados, key="ov_donut")
    with c4:
        renderizar_grafico("🏆 Ranking de Produtos", dados, key="ov_prod")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    titulo_secao("📋 Base Original Tratada",
                 "Todos os registros após tratamento no ETL.")
    renderizar_tabela(dados["tabela_original"], altura=420)
    renderizar_download(dados["tabela_original"], "dados_completos_tratados")

else:
    titulo, get_df, nome_csv = MAPA[escolha]
    titulo_secao(titulo, "Visualização detalhada com dados exportáveis.")

    renderizar_grafico(escolha, dados, key=f"g_{nome_csv}")

    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)

    titulo_secao(f"📋 Dados — {titulo.split(':', 1)[-1].strip()}",
                 "Tabela sincronizada com o gráfico acima.")
    df_tabela = get_df()
    renderizar_tabela(df_tabela)
    renderizar_download(df_tabela, nome_csv)
