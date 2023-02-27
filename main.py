import pandas as pd
import streamlit as st
import plotly.express as px

import processor as pr
import computing_prices as prices
import computing_scores as scores

st.set_page_config(page_title="Análisis de refuerzo", layout="wide")
area_proyecto = 10000

data = pd.read_excel("./defaults.xlsx")

uploaded_file = st.file_uploader("Cargar archivo de excel", type="xlsx")

if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)

results, na_weight, na_splices, na_heads = pr.results_constructor(data)

with st.sidebar.form(key="Form1"):

    st.header("Información general")

    submitted1 = st.form_submit_button(label="Guardar datos")

    if data is not None:
        building_area = st.number_input(
            "Área del proyecto (m²)", value=10000, min_value=1
        )

    st.header("Calificación del refuerzo")

    scores_data = dict(
        by_weigth=st.number_input("Puntaje por Peso", value=5, min_value=1),
        by_price=st.number_input("Puntaje por Precio", value=5, min_value=1),
        by_figures=st.number_input("Puntaje por #Figuras", value=5, min_value=1),
        by_pieces=st.number_input("Puntaje por #Piezas", value=5, min_value=1),
        by_blueprints=st.number_input("Puntaje por #Planos", value=5, min_value=1),
    )

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


if submitted1:
    results = pr.computing_unit_weigths(results, building_area)
    results = prices.assign_prices_global(results, bars, splices, heads)
    results = scores.assign_scores(results, scores_data)
    list_gh = pr.get_lists_to_graph(results)

    st.title("Puntajes de las opciones de refuerzo")

    fig = px.scatter(
        x = list_gh['keys'],
        y = list_gh['by_score'],
        labels={"value": "", "variable": "Indicador"},
        height=700,
    )
    fig.update_layout(font_size=20, plot_bgcolor='rgba(180, 180, 180, 0.3)')
    fig.update_xaxes(title="Opciones de refuerzo", visible=True, showticklabels=False)
    fig.update_yaxes(title="Puntaje", visible=True, showticklabels=False)

    st.plotly_chart(fig, use_container_width=True)