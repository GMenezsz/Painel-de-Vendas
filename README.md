
# 📊 Dashboard de Vendas e Pipeline ETL

Um painel de Business Intelligence (BI) interativo e moderno desenvolvido em  **Python** , utilizando **Pandas** para o pipeline de dados (ETL) e **Streamlit** junto com **Plotly** para a interface web de visualização.

O projeto foi construído para transformar planilhas brutas de vendas em métricas de negócio claras, automatizando análises de faturamento, ticket médio, volume físico e performance por loja/produto.

## 🚀 Funcionalidades

* **Pipeline ETL Modular (`main.py`):** Realiza a leitura dos dados brutos, tratamento e tipagem correta de datas, além do cálculo centralizado de múltiplos KPIs.
* **Interface Web Interativa (`app.py`):**
  * **Cards Executivos:** Visão rápida de Faturamento Total, Volume de Itens, Lojas Ativas, Ticket Médio e Destaques de Vendas.
  * **Aba de Lojas:** Gráficos de barras, rosca e visão hierárquica (Sunburst) de produtos por filial.
  * **Aba de Produtos:** Rankings de mais vendidos por quantidade e faturamento financeiro.
  * **Aba Temporal:** Curva de evolução do faturamento diário.
  * **Tabela Detalhada:** Filtros dinâmicos por Loja, Produto e Intervalo de Datas, com opção de exportação dos dados filtrados em CSV.

## 📂 Estrutura do Projeto

```
├── app.py                # Interface gráfica e visualizações (Streamlit + Plotly)
├── main.py               # Script de ETL e regras de negócio (Pandas)
├── Vendas.xlsx           # Base de dados de entrada
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação do projeto
```

## ⚙️ Instalação e Execução Local

1. **Clone o repositório ou baixe os arquivos** para a sua máquina.
2. **Instale as dependências** listadas no arquivo `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```
3. **Execute o aplicativo Streamlit:**
   ```
   streamlit run app.py
   ```

## ☁️ Hospedagem na Nuvem (Streamlit Community Cloud)

Este aplicativo pode ser publicado gratuitamente na nuvem do Streamlit.

> ⚠️ **Atenção sobre o modo ocioso (Idle):**
> Quando hospedado na  **Streamlit Community Cloud (plano gratuito)** , o aplicativo entra em **modo ocioso** automaticamente se ficar sem receber acessos por um determinado período. Quando isso acontece, o contêiner entra em hibernação para economizar recursos.
>
> * **O que acontece na prática:** O primeiro usuário que acessar o link após um período de inatividade perceberá que o carregamento inicial demorará alguns segundos a mais, pois a aplicação estará "acordando" (reinicializando o servidor e carregando o cache novamente). Basta clicar no botão azul do site e os acessos subsequentes voltarão à velocidade normal instantaneamente.

## 🛠️ Tecnologias Utilizadas

* **Python** (Linguagem principal)
* **Pandas** (Tratamento de dados e ETL)
* **Streamlit** (Criação do dashboard web)
* **Plotly** (Gráficos interativos)
* **Openpyxl** (Leitura de arquivos Excel)
