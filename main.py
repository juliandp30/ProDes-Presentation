import pandas as pd
import streamlit as st
import plotly.express as px

import processor as pr
import computing_prices as prices
import computing_scores as scores

st.set_page_config(page_title="Análisis de refuerzo", layout="wide")
area_proyecto = 10320

data = pd.read_excel("./defaults.xlsx")

uploaded_file = st.file_uploader("Cargar archivo de excel", type="xlsx")

if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)

results, na_weight, na_splices, na_heads = pr.results_constructor(data)

with st.sidebar.form(key="Form1"):

    st.header("Información general")

    submitted1 = st.form_submit_button(label="Generar reporte")

    if data is not None:
        building_area = st.number_input(
            "Área del proyecto (m²)", value=10320, min_value=1
        )

    st.header("Calificación del refuerzo")

    scores_data = dict(
        by_weigth=st.number_input("Puntaje por Peso", value=5, min_value=1),
        by_figures=st.number_input("Puntaje por #Figuras", value=5, min_value=1),
        by_pieces=st.number_input("Puntaje por #Operaciones", value=5, min_value=1),
        by_blueprints=st.number_input("Puntaje por #Planos", value=5, min_value=1),
    )

    st.header("Precios de barras (COP)")

    bars = {}
    for name in na_weight:
        bars[name] = st.number_input(name, value=4701, min_value=1)

    st.header("Precios de empalmes (COP)")

    splices = {}
    for name in na_splices:
        splices[name] = st.number_input(name, value=12566, min_value=1)

    st.header("Precios de cabezas (COP)")

    heads = {}
    for name in na_heads:
        heads[name] = st.number_input(name, value=17429, min_value=1)


if submitted1:
    results = pr.computing_unit_weigths(results, building_area)
    results = prices.assign_prices_global(results, bars, splices, heads)
    results = scores.assign_scores(results, scores_data)
    list_gh = pr.get_lists_to_graph(results)

    st.title("Puntajes de las opciones de refuerzo")

    fig = px.scatter(
        x=list_gh["keys"],
        y=list_gh["by_score"],
        height=700,
    )
    fig.update_layout(font_size=20, plot_bgcolor="rgba(180, 180, 180, 0.3)")
    fig.update_xaxes(title="Opciones de refuerzo", visible=True, showticklabels=False)
    fig.update_yaxes(title="Puntaje", visible=True, showticklabels=True, dtick=0.25)

    st.plotly_chart(fig, use_container_width=True)

    st.title("Precio del refuerzo (materiales)")

    fig = px.scatter(
        x=list_gh["keys"],
        y=list_gh["by_price"],
        height=700,
    )
    fig.update_layout(font_size=20, plot_bgcolor="rgba(180, 180, 180, 0.3)")
    fig.update_xaxes(title="Opciones de refuerzo", visible=True, showticklabels=False)
    fig.update_yaxes(title="Precio", visible=True, showticklabels=True, dtick=10000000)

    st.plotly_chart(fig, use_container_width=True)

    # st.title("Puntaje Vs. Precio")

    # fig = px.scatter(
    #     x=list_gh["by_price"],
    #     y=list_gh["by_score"],
    #     height=700,
    # )
    # fig.update_layout(font_size=20, plot_bgcolor="rgba(180, 180, 180, 0.3)")
    # fig.update_xaxes(title="Precio", visible=True, showticklabels=True, dtick=10000000)
    # fig.update_yaxes(title="Puntaje", visible=True, showticklabels=True, dtick=0.25)

    # st.plotly_chart(fig, use_container_width=True)

    st.title("Peso total del refuerzo")

    fig = px.scatter(
        x=list_gh["keys"],
        y=list_gh["by_weigth"],
        height=700,
    )
    fig.update_layout(font_size=20, plot_bgcolor="rgba(180, 180, 180, 0.3)")
    fig.update_xaxes(title="Opciones de refuerzo", visible=True, showticklabels=False)
    fig.update_yaxes(title="Peso total", visible=True, showticklabels=True, dtick=5)

    st.plotly_chart(fig, use_container_width=True)

    st.title("Tenores")

    fig = px.scatter(
        x=list_gh["keys"],
        y=list_gh["by_unitweigth"],
        height=700,
    )
    fig.update_layout(font_size=20, plot_bgcolor="rgba(180, 180, 180, 0.3)")
    fig.update_xaxes(title="Opciones de refuerzo", visible=True, showticklabels=False)
    fig.update_yaxes(
        title="Tenor",
        visible=True,
        showticklabels=False,
        range=[
            min(list_gh["by_unitweigth"]) * 0.8,
            max(list_gh["by_unitweigth"]) * 1.2,
        ],
    )

    st.plotly_chart(fig, use_container_width=True)

    # st.title("Colocación de piezas de refuerzo (# Operaciones)")

    # fig = px.scatter(
    #     x=list_gh["keys"],
    #     y=list_gh["by_pieces"],
    #     height=700,
    # )
    # fig.update_layout(font_size=20, plot_bgcolor="rgba(180, 180, 180, 0.3)")
    # fig.update_xaxes(title="Opciones de refuerzo", visible=True, showticklabels=False)
    # fig.update_yaxes(title="# Piezas", visible=True, showticklabels=True, dtick=500)

    # st.plotly_chart(fig, use_container_width=True)

    st.title("Gestión del inventario de la obra")

    fig = px.scatter(
        x=list_gh["keys"],
        y=list_gh["by_figures"],
        height=700,
    )
    fig.update_layout(font_size=20, plot_bgcolor="rgba(180, 180, 180, 0.3)")
    fig.update_xaxes(title="Opciones de refuerzo", visible=True, showticklabels=False)
    fig.update_yaxes(title="# Figuras", visible=True, showticklabels=True, dtick=10)

    st.plotly_chart(fig, use_container_width=True)

    st.title("Número de planos")

    fig = px.scatter(
        x=list_gh["keys"],
        y=list_gh["by_blueprints"],
        height=700,
    )
    fig.update_layout(font_size=20, plot_bgcolor="rgba(180, 180, 180, 0.3)")
    fig.update_xaxes(title="Opciones de refuerzo", visible=True, showticklabels=False)
    fig.update_yaxes(title="# Planos", visible=True, showticklabels=True, dtick=1)

    st.plotly_chart(fig, use_container_width=True)
