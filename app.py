import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard Oficial", layout="wide")
st.title("📊 Painel de Evolução de Receita (Dados do Excel)")

NOME_ARQUIVO = "planilha.xlsx - Planilha1.csv"

try:
    # 1. Carrega o arquivo original
    df_original = pd.read_csv(NOME_ARQUIVO)

    # Limpeza de espaços nos nomes das colunas e linhas
    df_original.columns = df_original.columns.str.strip()
    df_original["Conta"] = df_original["Conta"].astype(str).str.strip()

    # 2. Filtra a linha da Receita
    df_receita = df_original[df_original["Conta"].str.lower() == "receita"]

    if not df_receita.empty:
        # 3. Separa apenas as colunas que são os Trimestres
        colunas_excluir = ["Conta", "Variação Trimestral", "Variação Anual"]
        colunas_trimestres = [
            c for c in df_original.columns if c not in colunas_excluir
        ]

        # 4. Extrai os valores
        valores = df_receita[colunas_trimestres].values.flatten()

        # 5. Cria o DataFrame estruturado para o gráfico
        df_final = pd.DataFrame(
            {"Trimestre": colunas_trimestres, "Receita": valores}
        )

        # ⚙️ CORREÇÃO DO BUG: Trata os traços '-' e espaços vazios
        df_final["Receita"] = df_final["Receita"].astype(str).str.strip()
        df_final["Receita"] = df_final["Receita"].replace("-", "0")

        # Força a conversão para número puro (Float)
        df_final["Receita"] = pd.to_numeric(
            df_final["Receita"], errors="coerce"
        )

        # Remove linhas que porventura tenham ficado inválidas (NaN)
        df_final = df_final.dropna(subset=["Receita"])

        # Garante que o Trimestre seja exibido como texto no eixo X
        df_final["Trimestre"] = df_final["Trimestre"].astype(str)

        # 6. Ordena do trimestre mais antigo para o mais recente
        df_final = df_final.iloc[::-1].reset_index(drop=True)

        # 7. Renderiza os componentes na tela
        st.subheader("📈 Gráfico de Evolução de Receita")

        # Usando o gráfico de área ou linha nativo com dados 100% numéricos agora
        st.area_chart(data=df_final, x="Trimestre", y="Receita")

        st.subheader("📋 Tabela de Dados Tratados")
        st.dataframe(df_final)

    else:
        st.error("A linha 'Receita' não foi encontrada na planilha.")

except Exception as e:
    st.error(f"Erro ao processar a planilha: {e}")