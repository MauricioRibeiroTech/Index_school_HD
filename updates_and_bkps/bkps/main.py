import streamlit as st
import pandas as pd
import numpy as np


def per_aluno(A,B):
    p= (A/B)*100
    return p


st.set_page_config(
    page_title="SIMULADOS SAEB HD",
    page_icon=":book:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/MauricioRibeiroTech',
        'Report a bug': "https://github.com/MauricioRibeiroTech",
        'About': "# Aplicativo para os Indices dos Simulados do SAEB-HD "
    }
)

with st.sidebar:
    st.title('Projeto SAEB-HD 2025')
    st.markdown('Relatório de notas')
    uploaded_file = st.file_uploader('Coloque o seu arquivo aqui')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=",")

    with st.sidebar:
        salas_distintas = df['Simulados'].unique().tolist()
        salas_selecionadas = st.selectbox("Simulados", salas_distintas)

        componente_selecionada = st.radio("Componentes", ["Matematica","Portugues"])

        if componente_selecionada:
            df = df[df["Simulados"] == salas_selecionadas]

        if componente_selecionada:
            df = df[df["Componentes"] == componente_selecionada]

    st.header("Relatório de notas de " + str(componente_selecionada))
    # dataframe desconsiderando as tres primeiras colunas
    df1 = df.iloc[:, 3:31]
    df_alunos = df.iloc[:,0]
    Num_descritores = len(df1.columns)
    Num_alunos = len(df_alunos)
    df_analise_alunos = pd.DataFrame()
    df_descritores = pd.DataFrame()

    #soma das linhas do dataframe (analise por aluno)
    df2 = df1.sum(axis=1)
    df_analise_alunos['Nomes'] = df_alunos
    df_analise_alunos['Porcentagem'] = (df2/Num_descritores)*100

    #df_descritores['Descritores']

    df_descritores['Descritor'] = df1.columns.tolist()
    df_descritores['Porcentagem'] = df1.sum(axis=0).tolist()
    df_descritores['Porcentagem'] = (df_descritores['Porcentagem']/Num_alunos)*100
    #df_porcentagem_descritor = df1.sum(axis=0)
    #st.table(df_descritores)

    #Gráfico Notas em Porcentagem dos alunos
    st.markdown("## Nota em porcentagem dos alunos")
    st.bar_chart(df_analise_alunos,x= "Nomes", y="Porcentagem",stack=False)

    #Gráfico de porcentagem dos descritores
    st.markdown("## Porcentagem de acerto dos descritores")
    st.bar_chart(df_descritores, x="Descritor", y="Porcentagem", stack=False)

    a, b = st.columns(2)
    dif1 = df_descritores['Porcentagem'].mean().round(2) - 60
    dif2 = df_analise_alunos['Porcentagem'].mean().round(2) - 60

    a.metric("Porcentagem Média Descritores", df_descritores['Porcentagem'].mean().round(2), dif1.round(2) , border = True)
    b.metric("Porcentagem Média Alunos", df_analise_alunos['Porcentagem'].mean().round(2), dif2.round(2), border=True)

