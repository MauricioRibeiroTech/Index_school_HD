import streamlit as st
import pandas as pd
import numpy as np
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


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


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

#authenticator.login()
#if st.session_state["authentication_status"]:
#    authenticator.logout()
#st.write(f'Bem Vindo *{st.session_state["name"]}*')

SIM = ['Sim1', 'Sim2', 'Sim3']
ERRO = ['Err1', 'Err2','Err3']

with st.sidebar:
    st.title('Relatório de notas')
    uploaded_file = st.file_uploader('Coloque o seu arquivo aqui')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=",")

    with st.sidebar:
        salas_distintas = df['Turma'].unique().tolist()
        salas_selecionadas = st.selectbox("Séries", salas_distintas)

        componente_selecionada = st.radio("Componente", ["Matematica","Portugues"])

        if componente_selecionada:
            df = df[df["Turma"] == salas_selecionadas]

        if componente_selecionada:
            df = df[df["Componente"] == componente_selecionada]

    st.header("Relatório de notas de " + str(componente_selecionada))

        # st.table(df)
    st.markdown("Relatório de acertos")
    st.bar_chart(df, x='Aluno', y=SIM, stack=False)

    st.markdown("Relatório de Erros")
    st.bar_chart(df, x='Aluno', y=ERRO, stack=False)

    a, b, c = st.columns(3)
    media_1 = df['Sim1'].sum()/len(df['Sim1'])
    media_2 = df['Err1'].sum()/len(df['Err1'])

    media_3 = df['Sim2'].sum()/len(df['Sim2'])
    media_4 = df['Err2'].sum()/len(df['Err2'])

    media_5 = df['Sim3'].sum() / len(df['Sim3'])
    media_6 = df['Err3'].sum() / len(df['Err3'])

    median_1 = df['Sim1'].median()
    median_2 = df['Sim2'].median()
    median_3 = df['Sim3'].median()




        #media_7 = df['Sim 7'].mean().round(1)
        #media_8 = df['Sim 8'].mean().round(1)
        #media_9 = df['Sim 9'].mean().round(1)
        #media_10 = df['Sim 10'].mean().round(1)
        #media_11 = df['Sim 11'].mean().round(1)
        #media_12 = df['Sim 12'].mean().round(1)

    dif1 = -6.0 + media_1
    dif2 = 0.0 - media_2

    dif3 = -6.0 + media_3
    dif4 = 0.0 - media_4

    dif5 = -6.0 + media_5
    dif6 = 0.0 - media_6

        #dif7 = media_7 - 6.0
        #dif8 = media_8 - 6.0
        #dif9 = media_9 - 6.0

        #dif10 = media_10 - 6.0
        #dif11 = media_11 - 6.0
        #dif12 = media_12 - 6.0

    a.metric("Média do simulado 1", media_1.round(2), dif1.round(2), border=True)
    b.metric("Mediana Acertos", median_1.round(2),median_1.round(2)-6.0, border=True)
    c.metric("Média de Erros", media_2.round(2), dif2.round(2), border=True)

    a.metric("Média do simulado 2", media_3.round(2), dif3.round(2), border=True)
    b.metric("Mediana Acertos", median_2.round(2),median_2.round(2)-6.0, border=True)
    c.metric("Média de Erros 2", media_4.round(2), dif4.round(2), border=True)

    a.metric("Média do simulado 3", media_5.round(2), dif5.round(2), border=True)
    b.metric("Mediana Acertos", median_3.round(2),median_3.round(2)-6.0, border=True)
    c.metric("Média de Erros 3", media_6.round(2), dif6.round(2), border=True)


        #a.metric("Simulado 7", media_7, dif7.round(1), border=True)
        #b.metric("Simulado 8", media_8, dif8.round(1), border=True)
        #c.metric("Simulado 9", media_9, dif9.round(1), border=True)
        #a.metric("Simulado 10", media_10, dif10.round(1), border=True)
        #b.metric("Simulado 11", media_11, dif11.round(1), border=True)
        #c.metric("Simulado 12", media_12, dif12.round(1), border=True)

    st.markdown("## Alunos acima de 6 pontos")
    st.markdown("### Primeiro Simulado")
    df_filtrado_1 = df[df['Sim1'] >= 6]
    st.table(df_filtrado_1[["Aluno", "Sim1"]].sort_values("Sim1",ascending=False))


    p1 = per_aluno(len(df_filtrado_1),len(df))

    #st.markdown("### Número total de aluno acima de 6 é " + str())
    a1, b1 =st.columns(2)
    a1.metric("Número de alunos acima de 6", len(df_filtrado_1), border=True)
    b1.metric("Porcentagem de alunos acima de 6", round(p1,2), border=True)

    st.markdown("### Segundo Simulado")
    df_filtrado_2 = df[df['Sim2'] >= 6]
    st.table(df_filtrado_2[["Aluno", "Sim2"]].sort_values("Sim2",ascending=False))

   #st.markdown("Número total de aluno acima de 6 é " + str(len(df_filtrado_2)))
    p2 = per_aluno(len(df_filtrado_2), len(df))
    a2, b2= st.columns(2)
    a2.metric("Número de alunos acima de 6", len(df_filtrado_2), border=True)
    b2.metric("Porcentagem de alunos acima de 6", round(p2,2), border=True)



    st.markdown("### Terceiro Simulado")
    df_filtrado_3 = df[df['Sim3'] >= 6]
    st.table(df_filtrado_3[["Aluno", "Sim3"]].sort_values("Sim3",ascending=False))

    #st.markdown("Número total de aluno acima de 6 é " + str(len(df_filtrado_3)))
    p2 = per_aluno(len(df_filtrado_3), len(df))
    a2, b2= st.columns(2)
    a2.metric("Número de alunos acima de 6", len(df_filtrado_3), border=True)
    b2.metric("Porcentagem de alunos acima de 6", round(p2,2), border=True)


    #with st.sidebar.expander("Desenvolvimento:"):
     #   st.write("Mauricio A. Ribeiro")
     #   st.write("EMAIL: mau.ap.ribeiro@gmail.com")
     #   st.write("GITHUB: ")

#elif st.session_state["authentication_status"] is False:
#    st.error('Usuário/Senha é inválido')
#elif st.session_state["authentication_status"] is None:
#    st.warning('Por Favor, utilize seu usuário e senha!')

