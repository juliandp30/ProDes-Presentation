import pandas as pd
import streamlit as st
import plotly.express as px

area_proyecto = 15531.0

data = pd.DataFrame(
    [
        ["0.1", 115.3, 28.8, 193, 8953, 'Φ1/2" a Φ1"'],
        ["0.1", 115.9, 28.0, 178, 8665, 'Φ5/8" a Φ7/8"'],
        ["0.1", 116.5, 27.6, 133, 8691, 'Φ3/4"'],
        ["0.1", 116.9, 27.6, 149, 8610, 'Φ3/4" y Φ7/8"'],
        ["0.1", 150.5, 27.6, 119, 6713, 'Φ7/8"'],
        ["0.5", 118.4, 28.8, 87, 9233, 'Φ1/2" a Φ1"'],
        ["0.5", 119.1, 28.0, 75, 8938, 'Φ5/8" a Φ7/8"'],
        ["0.5", 119.8, 27.6, 50, 8945, 'Φ3/4"'],
        ["0.5", 120.1, 27.6, 60, 8860, 'Φ3/4" y Φ7/8"'],
        ["0.5", 154.0, 27.6, 38, 6994, 'Φ7/8"'],
        ["1", 123.3, 28.9, 67, 9167, 'Φ1/2" a Φ1"'],
        ["1", 124.0, 28.0, 50, 8820, 'Φ5/8" a Φ7/8"'],
        ["1", 124.7, 27.6, 33, 8807, 'Φ3/4"'],
        ["1", 125.1, 27.6, 39, 8720, 'Φ3/4" y Φ7/8"'],
        ["1", 157.4, 27.6, 22, 6949, 'Φ7/8"'],
    ],
    columns=["long", "peso_long", "peso_est", "n_fig", "n_barras", "calibres"],
)

data["peso_total"] = data["peso_long"] + data["peso_est"]
data["tenor_long"] = data["peso_long"] * 1000 / area_proyecto
data["tenor_est"] = data["peso_est"] * 1000 / area_proyecto
data["tenor_total"] = data["peso_total"] * 1000 / area_proyecto

data["analisis"] = data["calibres"] + ' con ' + data["long"] + 'm'
data["Numero figuras"] = data["n_fig"]
data["Barras por 100m2"] = data["n_barras"] * 100 / area_proyecto
data["10 * tenor"] = data["tenor_total"] * 10

st.set_page_config(
    page_title="ProDes",
    layout="wide",
    menu_items={
        # "About": "# This is a header. This is an *extremely* cool app!"
    },
)

view_mode = st.sidebar.selectbox('Modo de vista', options=['group', 'stack'])

fig = px.bar(
    data,
    x="analisis",
    y=["Numero figuras", "10 * tenor", "Barras por 100m2"],
    width=1400,
    barmode=view_mode,
)
st.plotly_chart(fig)

col1, col2 = st.columns(2)

with col1:
    fig_peso = px.bar(
        data,
        x="long",
        y=["peso_long", "peso_est"],
        labels={
            "long": "Multiplo de longitud (m)",
            "calibres": "Calibres empleados",
            "value": "Peso (tonf)",
        },
        color="calibres",
        barmode="group",
        height=400,
        title="Pesos",
    )
    st.plotly_chart(fig_peso)

    fig_tenor = px.bar(
        data,
        x="long",
        y=["tenor_long", "tenor_est"],
        labels={
            "long": "Multiplo de longitud (m)",
            "calibres": "Calibres empleados",
            "value": "Tenor (kgf/m²)",
        },
        color="calibres",
        barmode="group",
        height=400,
        title="Tenores",
    )
    st.plotly_chart(fig_tenor)

with col2:
    fig_figuras = px.bar(
        data,
        x="long",
        y=["n_fig"],
        labels={
            "long": "Multiplo de longitud (m)",
            "calibres": "Calibres empleados",
            "value": "Número figuras",
        },
        color="calibres",
        barmode="group",
        height=400,
        title="Número de figuras",
    )
    st.plotly_chart(fig_figuras)

    fig_barras = px.bar(
        data,
        x="long",
        y=["n_barras"],
        labels={
            "long": "Multiplo de longitud (m)",
            "calibres": "Calibres empleados",
            "value": "Número de barras",
        },
        color="calibres",
        barmode="group",
        height=400,
        title="Cantidad de varillas",
    )
    st.plotly_chart(fig_barras)
