import streamlit as st
import pandas as pd
import numpy as np
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

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

authenticator.login()


if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Bem Vindo *{st.session_state["name"]}*')

    SIM = ['Sim1', 'Smi2', 'Err1', 'Err2']

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
        st.bar_chart(df, x='Aluno', y=SIM, stack=False)


        a, b, c = st.columns(3)

        media_1 = df['Sim1'].mean().round(2)
        media_2 = df['Acer1'].mean().round(2)
        media_3 = df['Err1'].mean().round(2)
        media_4 = df['Sim2'].mean().round(1)
        media_5 = df['Acer2'].mean().round(1)
        media_6 = df['Err2'].mean().round(1)
        #media_7 = df['Sim 7'].mean().round(1)
        #media_8 = df['Sim 8'].mean().round(1)
        #media_9 = df['Sim 9'].mean().round(1)
        #media_10 = df['Sim 10'].mean().round(1)
        #media_11 = df['Sim 11'].mean().round(1)
        #media_12 = df['Sim 12'].mean().round(1)

        dif1 = 6.0 - media_1
        dif2 = 6.0 - media_2
        dif3 = 0.0 - media_3

        dif4 = media_4 - 6.0
        dif5 = media_5 - 6.0
        dif6 = media_6 - 6.0

        #dif7 = media_7 - 6.0
        #dif8 = media_8 - 6.0
        #dif9 = media_9 - 6.0

        #dif10 = media_10 - 6.0
        #dif11 = media_11 - 6.0
        #dif12 = media_12 - 6.0

        a.metric("Simulado 1", media_1, dif1.round(2), border=True)
        b.metric("Média de Acertos", media_2, dif2.round(2), border=True)
        c.metric("Média de Erros", media_3, dif3.round(2), border=True)
        a.metric("Simulado 2", media_4, dif4.round(1), border=True)
        b.metric("Média de Acertos", media_5, dif5.round(1), border=True)
        c.metric("Média de Erros", media_6, dif6.round(1), border=True)
        #a.metric("Simulado 7", media_7, dif7.round(1), border=True)
        #b.metric("Simulado 8", media_8, dif8.round(1), border=True)
        #c.metric("Simulado 9", media_9, dif9.round(1), border=True)
        #a.metric("Simulado 10", media_10, dif10.round(1), border=True)
        #b.metric("Simulado 11", media_11, dif11.round(1), border=True)
        #c.metric("Simulado 12", media_12, dif12.round(1), border=True)


    with st.sidebar.expander("Desenvolvimento:"):
        st.write("Mauricio A. Ribeiro")
        st.write("EMAIL: mau.ap.ribeiro@gmail.com")
        st.write("GITHUB: ")

elif st.session_state["authentication_status"] is False:
    st.error('Usuário/Senha é inválido')
elif st.session_state["authentication_status"] is None:
    st.warning('Por Favor, utilize seu usuário e senha!')




