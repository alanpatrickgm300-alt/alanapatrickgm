import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard Oficial", layout="wide")
st.title("📊 Painel de Evolução de Receita (Dados Reais do Excel)")

# Nome exato do arquivo que você subiu
NOME_ARQUIVO = "planilha.xlsx - Planilha1.csv"

try:
    # 1. Lendo o arquivo CSV da planilha
    df_original = pd.read_csv(NOME_ARQUIVO)

    # 2. Filtrando apenas a linha onde a coluna 'Conta' é igual a 'Receita'
    df_receita = df_original[df_original["Conta"] == "Receita"]

    if not df_receita.empty:
        # 3. Identificando as colunas de trimestres (todas exceto os textos iniciais)
        colunas_trimestres = [
            c
            for c in df_original.columns
            if c not in ["Conta", "Variação Trimestral", "Variação Anual"]
        ]

        # 4. Extraindo os valores dessas colunas
        valores = df_receita[colunas_trimestres].values.flatten()

        # 5. Criando um novo DataFrame estruturado para o gráfico
        df_final = pd.DataFrame(
            {"Trimestre": colunas_trimestres, "Receita": valores}
        )

        # 6. Convertendo a coluna Receita para número (removendo qualquer texto ou campo vazio)
        df_final["Receita"] = pd.to_numeric(
            df_final["Receita"], errors="coerce"
        )
        df_final = df_final.dropna()

        # 7. Invertendo a ordem para que o gráfico vá do trimestre mais antigo para o mais recente
        df_final = df_final.iloc[::-1].reset_index(drop=True)

        # 8. Exibindo os resultados no Streamlit
        st.subheader("📈 Gráfico de Linha Oficial do Excel")
        st.line_chart(data=df_final, x="Trimestre", y="Receita")

        st.subheader("📋 Tabela de Dados Estruturados")
        st.dataframe(df_final)

    else:
        st.error(
            "Não foi possível encontrar a linha com a palavra 'Receita' na coluna 'Conta'."
        )

except Exception as e:
    st.error(f"Erro ao processar o arquivo: {e}")
    st.info(
        f"Certifique-se de que o arquivo '{NOME_ARQUIVO}' está na mesma pasta do seu app.py"
    )