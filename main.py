import pandas as pd
import streamlit as st
import plotly.express as px

import processor as pr

st.set_page_config(page_title="Análisis de refuerzo", layout="wide")
area_proyecto = 10000

data = pd.read_excel("./defaults.xlsx")

uploaded_file = st.file_uploader("Cargar archivo de excel", type="xlsx")

if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)

results, na_weight, na_splices, na_heads = pr.results_constructor(data)

with st.sidebar.form(key="Form1"):

    st.header("Información general")

    if data is not None:
        area_proyecto = st.number_input(
            "Área del proyecto (m²)", value=10000, min_value=1
        )

    st.header("")
    st.header("Calificación del refuerzo")

    score_weight = st.number_input("Puntaje por Peso", value=5, min_value=1)
    score_price = st.number_input("Puntaje por Precio", value=5, min_value=1)
    score_figures = st.number_input("Puntaje por #Figuras", value=5, min_value=1)
    score_pieces = st.number_input("Puntaje por #Piezas", value=5, min_value=1)
    score_blueprints = st.number_input("Puntaje por #Planos", value=5, min_value=1)

    st.header("")
    st.header("Precios de barras (COP)")

    bars = {}
    for name in na_weight:
        bars[name] = st.number_input(name, value=5000, min_value=1)

    st.header("")
    st.header("Precios de empalmes (COP)")

    splices = {}
    for name in na_splices:
        splices[name] = st.number_input(name, value=12000, min_value=1)

    st.header("")
    st.header("Precios de cabezas (COP)")

    heads = {}
    for name in na_heads:
        heads[name] = st.number_input(name, value=15000, min_value=1)

    submitted1 = st.form_submit_button(label="Guardar precios")
