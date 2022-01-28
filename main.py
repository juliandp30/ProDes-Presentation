import pandas as pd
import streamlit as st
import plotly.express as px

area_proyecto = 15531.0

data = pd.DataFrame(
    [
        [0.1, 115.3, 28.8, 193, 8953, 'Φ1/2" a Φ1"'],
        [0.1, 115.9, 28.0, 178, 8665, 'Φ5/8" a Φ7/8"'],
        [0.1, 116.5, 27.6, 133, 8691, 'Φ3/4"'],
        [0.1, 116.9, 27.6, 149, 8610, 'Φ3/4" y Φ7/8"'],
        [0.1, 150.5, 27.6, 119, 6713, 'Φ7/8"'],
        [0.5, 118.4, 28.8, 87, 9233, 'Φ1/2" a Φ1"'],
        [0.5, 119.1, 28.0, 75, 8938, 'Φ5/8" a Φ7/8"'],
        [0.5, 119.8, 27.6, 50, 8945, 'Φ3/4"'],
        [0.5, 120.1, 27.6, 60, 8860, 'Φ3/4" y Φ7/8"'],
        [0.5, 154.0, 27.6, 38, 6994, 'Φ7/8"'],
        [1, 123.3, 28.9, 67, 9167, 'Φ1/2" a Φ1"'],
        [1, 124.0, 28.0, 50, 8820, 'Φ5/8" a Φ7/8"'],
        [1, 124.7, 27.6, 33, 8807, 'Φ3/4"'],
        [1, 125.1, 27.6, 39, 8720, 'Φ3/4" y Φ7/8"'],
        [1, 157.4, 27.6, 22, 6949, 'Φ7/8"'],
    ],
    columns=[
        "Longitud",
        "PesoRefLongitudinal",
        "PesoEstribos",
        "NúmeroFiguras",
        "NúmeroBarras",
        "Calibres",
    ],
)

data["PesoTotal"] = data["PesoRefLongitudinal"] + data["PesoEstribos"]
data["TenorRefLongitudinal"] = data["PesoRefLongitudinal"] * 1000 / area_proyecto
data["TenorEstribos"] = data["PesoEstribos"] * 1000 / area_proyecto
data["TenorTotal"] = data["PesoTotal"] * 1000 / area_proyecto

data["Longitud"] = data["Longitud"].apply(str)
data["Análisis"] = data["Calibres"] + " % " + data["Longitud"] + "m"

st.set_page_config(
    page_title="ProDes",
    layout="wide",
)

view_mode = st.sidebar.selectbox("Modo de vista", options=["group", "stack"])

data["Peso Total"] = data["PesoTotal"] / max(data["PesoTotal"])
data["Número Barras"] = data["NúmeroBarras"] / max(data["NúmeroBarras"])
data["Número Figuras"] = data["NúmeroFiguras"] / max(data["NúmeroFiguras"])

st.title('Indicadores y tendencias')

fig = px.bar(
    data,
    x="Análisis",
    y=["Peso Total", "Número Barras", "Número Figuras"],
    labels={
        "value": "",
        "variable": "Indicador"
    },
    barmode=view_mode,
)
fig.update_yaxes(title='', visible=True, showticklabels=False)
fig.update_traces(hoverinfo='skip', hovertemplate=None)
st.plotly_chart(fig, use_container_width=True)


st.title('Peso total de refuerzo')
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

st.title('Tenores de refuerzo')

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

st.title('Análisis de almacenamiento')

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

st.title('Análisis de colocación')

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
