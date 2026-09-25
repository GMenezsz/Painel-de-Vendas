import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)


def executar_etl(caminho_excel="Vendas.xlsx", exportar_csv=True):
    """
    Executa o ETL e retorna um dicionário com todos os DataFrames tratados.
    Se exportar_csv=True, também salva os CSVs como antes.
    """
    tabela = pd.read_excel(caminho_excel)

    # ---------- NORMALIZAÇÃO DE TIPOS ----------
    # Garante que "Data" seja datetime de verdade (evita agrupar errado
    # no groupby caso venha com horário embutido ou tipo misto do Excel)
    tabela["Data"] = pd.to_datetime(tabela["Data"], errors="coerce").dt.normalize()

    # ---------- FATURAMENTO TOTAL / POR LOJA ----------
    faturamento_total = tabela["Valor Final"].sum()

    faturamento_loja = (
        tabela[["ID Loja", "Valor Final"]]
        .groupby("ID Loja", as_index=False)
        .sum()
        .sort_values(by="Valor Final", ascending=False)
    )

    # ---------- TICKET MÉDIO ----------
    ticket_medio_loja = (
        tabela[["ID Loja", "Valor Final"]]
        .groupby("ID Loja", as_index=False)
        .mean()
        .sort_values(by="Valor Final", ascending=False)
    )

    # ---------- PRODUTO MAIS VENDIDO (por loja) ----------
    faturamento_produto = (
        tabela[["ID Loja", "Produto", "Valor Final", "Quantidade"]]
        .groupby(["ID Loja", "Produto"], as_index=False)
        .agg({"Valor Final": "sum", "Quantidade": "sum"})
        .sort_values(by="Quantidade", ascending=False)
    )

    # ---------- PRODUTO MAIS VENDIDO (geral) ----------
    produto_mais_vendido = (
        tabela[["Produto", "Quantidade", "Valor Final"]]
        .groupby("Produto", as_index=False)
        .agg({"Quantidade": "sum", "Valor Final": "sum"})
        .sort_values(by="Quantidade", ascending=False)
    )

    # ---------- VOLUME TOTAL DE ITENS ----------
    volume_itens = tabela["Quantidade"].sum()

    # ---------- FATURAMENTO DIÁRIO ----------
    faturamento_diario = (
        tabela[["Data", "Valor Final"]]
        .groupby("Data", as_index=False)
        .sum()
        .sort_values(by="Data")
    )

    # ---------- FATURAMENTO POR LOJA + PRODUTO (heatmap/stacked) ----------
    faturamento_loja_produto = (
        tabela[["ID Loja", "Produto", "Valor Final"]]
        .groupby(["ID Loja", "Produto"], as_index=False)
        .sum()
    )

    # ---------- Quantidade por produto e loja ----------
    quantidade_produto = (
        tabela[["Produto", "Quantidade"]]
        .groupby("Produto", as_index=False)
        .sum()
        .sort_values(by="Quantidade", ascending=False)
    )

    resultado = {
        "tabela_original": tabela,
        "faturamento_total": faturamento_total,
        "faturamento_loja": faturamento_loja,
        "ticket_medio_loja": ticket_medio_loja,
        "faturamento_produto": faturamento_produto,
        "produto_mais_vendido": produto_mais_vendido,
        "volume_itens": volume_itens,
        "faturamento_diario": faturamento_diario,
        "faturamento_loja_produto": faturamento_loja_produto,
        "quantidade_produto": quantidade_produto,
    }

    if exportar_csv:
        faturamento_loja.to_csv("Faturamento_por_loja.csv", index=False)
        ticket_medio_loja.to_csv("Ticket_medio_loja.csv", index=False)
        faturamento_produto.to_csv("Faturamento_produto.csv", index=False)

    return resultado


def main():
    executar_etl()


if __name__ == "__main__":
    main()