import pandas as pd
import streamlit as st
import plotly.express as px


def graficar_data(data):
    st.title("Indicadores y tendencias")
    fig = px.bar(
        data,
        x="Análisis",
        y=["Peso Total", "Número Barras", "Número Figuras"],
        labels={"value": "", "variable": "Indicador"},
        barmode=view_mode,
    )
    fig.update_yaxes(title="", visible=True, showticklabels=False)
    fig.update_traces(hoverinfo="skip", hovertemplate=None)
    st.plotly_chart(fig, use_container_width=True)

    st.title("Peso total de refuerzo")
    fig_peso = px.bar(
        data,
        x="Longitud",
        y=["PesoRefLongitudinal", "PesoEstribos"],
        labels={
            "Longitud": "Múltiplo de Longitud (m)",
            "Calibres": "Calibres empleados",
            "value": "Peso (tonf)",
        },
        color="Calibres",
        barmode="group",
    )
    st.plotly_chart(fig_peso, use_container_width=True)

    st.title("Tenores de refuerzo")
    fig_tenor = px.bar(
        data,
        x="Longitud",
        y=["TenorRefLongitudinal", "TenorEstribos"],
        labels={
            "Longitud": "Múltiplo de Longitud (m)",
            "Calibres": "Calibres empleados",
            "value": "Tenor (kgf/m²)",
        },
        color="Calibres",
        barmode="group",
    )
    st.plotly_chart(fig_tenor, use_container_width=True)

    st.title("Análisis de almacenamiento")
    fig_figuras = px.bar(
        data,
        x="Longitud",
        y=["NúmeroFiguras"],
        labels={
            "Longitud": "Múltiplo de Longitud (m)",
            "Calibres": "Calibres empleados",
            "value": "Número figuras",
        },
        color="Calibres",
        barmode="group",
    )
    st.plotly_chart(fig_figuras, use_container_width=True)

    st.title("Análisis de colocación")
    fig_barras = px.bar(
        data,
        x="Longitud",
        y=["NúmeroBarras"],
        labels={
            "Longitud": "Múltiplo de Longitud (m)",
            "Calibres": "Calibres empleados",
            "value": "Número de barras",
        },
        color="Calibres",
        barmode="group",
    )
    st.plotly_chart(fig_barras, use_container_width=True)


def update_dataframe(data, area_proyecto):
    data["PesoTotal"] = data["PesoRefLongitudinal"] + data["PesoEstribos"]
    data["TenorRefLongitudinal"] = data["PesoRefLongitudinal"] * 1000 / area_proyecto
    data["TenorEstribos"] = data["PesoEstribos"] * 1000 / area_proyecto
    data["TenorTotal"] = data["PesoTotal"] * 1000 / area_proyecto

    data["Longitud"] = data["Longitud"].apply(str)
    data["Análisis"] = data["Calibres"] + " % " + data["Longitud"] + "m"

    data["Peso Total"] = data["PesoTotal"] / max(data["PesoTotal"])
    data["Número Barras"] = data["NúmeroBarras"] / max(data["NúmeroBarras"])
    data["Número Figuras"] = data["NúmeroFiguras"] / max(data["NúmeroFiguras"])

    return data


st.set_page_config(page_title="ProDes", layout="wide")
area_proyecto = 15531

data = pd.read_csv("./defaults.csv")
data = update_dataframe(data, area_proyecto)

uploaded_file = st.file_uploader("Cargar CSV", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

if data is not None:
    area_proyecto = st.sidebar.number_input(
        "Area del proyecto (m2)", value=15531, min_value=1
    )
    update_dataframe(data, area_proyecto)
    view_mode = st.sidebar.selectbox("Modo de vista", options=["group", "stack"])
    graficar_data(data)
