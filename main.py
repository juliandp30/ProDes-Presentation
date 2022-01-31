import pandas as pd
import streamlit as st
import plotly.express as px


def graficar_data(data, font_size=20):
    min_index = data["PesoTotal"].T.idxmin()
    min_index_name_peso = data.iloc[min_index]["Análisis"]

    min_index = data["NúmeroBarras"].T.idxmin()
    min_index_name_barras = data.iloc[min_index]["Análisis"]

    min_index = data["NúmeroFiguras"].T.idxmin()
    min_index_name_figuras = data.iloc[min_index]["Análisis"]

    st.title("Indicadores y tendencias")
    fig = px.bar(
        data,
        x="Análisis",
        y=[
            f"Peso Total ({min_index_name_peso})",
            f"Número Barras ({min_index_name_barras})",
            f"Número Figuras ({min_index_name_figuras})",
        ],
        labels={"value": "", "variable": "Indicador"},
        barmode=view_mode,
        height=700,
    )
    fig.update_xaxes(tickangle=270)
    fig.update_layout(font_size=font_size)
    fig.update_yaxes(title="", visible=True, showticklabels=False)
    fig.update_traces(hoverinfo="skip", hovertemplate=None)
    st.plotly_chart(fig, use_container_width=True)

    st.title("Peso total de refuerzo")

    min_index = data["PesoTotal"].T.idxmin()
    min_index_name = data.iloc[min_index]["Análisis"]

    st.subheader(
        f"El análisis {min_index_name} tiene el menor peso, con {min(data['PesoTotal']):.2f} tonf"
    )
    fig = px.bar(
        data,
        x="Longitud",
        y=["PesoTotalMin"],
        labels={
            "Longitud": "Múltiplo de Longitud (m)",
            "Calibres": "Calibres empleados",
            "value": f"Aumento en el peso (tonf)",
        },
        color="Calibres",
        barmode="group",
        height=500,
    )
    fig.update_layout(font_size=font_size)
    st.plotly_chart(fig, use_container_width=True)

    st.title("Tenores de refuerzo")

    min_index = data["TenorTotal"].T.idxmin()
    min_index_name = data.iloc[min_index]["Análisis"]

    st.subheader(
        f"El análisis {min_index_name} tiene el menor tenor, con {min(data['TenorTotal']):.2f} kgf/m²"
    )

    fig = px.bar(
        data,
        x="Longitud",
        y=["TenorTotalMin"],
        labels={
            "Longitud": "Múltiplo de Longitud (m)",
            "Calibres": "Calibres empleados",
            "value": "Aumento en el tenor (kgf/m²)",
        },
        color="Calibres",
        barmode="group",
        height=500,
    )
    fig.update_layout(font_size=font_size)
    st.plotly_chart(fig, use_container_width=True)

    st.title("Análisis de almacenamiento")

    min_index = data["NúmeroFiguras"].T.idxmin()
    min_index_name = data.iloc[min_index]["Análisis"]

    st.subheader(
        f"El análisis {min_index_name} tiene la menor cantidad de figuras, con {min(data['NúmeroFiguras'])}"
    )

    fig = px.bar(
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
        height=500,
    )
    fig.update_layout(font_size=font_size)
    st.plotly_chart(fig, use_container_width=True)

    st.title("Análisis de colocación")

    min_index = data["NúmeroBarras"].T.idxmin()
    min_index_name = data.iloc[min_index]["Análisis"]

    st.subheader(
        f"El análisis {min_index_name} tiene la menor cantidad de barras, con {min(data['NúmeroBarras'])}"
    )

    fig = px.bar(
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
        height=500,
    )
    fig.update_layout(font_size=font_size)
    fig.update_layout(
        yaxis_range=[0.99 * min(data["NúmeroBarras"]), 1.01 * max(data["NúmeroBarras"])]
    )
    st.plotly_chart(fig, use_container_width=True)


def update_dataframe(data, area_proyecto):
    data["PesoTotal"] = data["PesoRefLongitudinal"] + data["PesoEstribos"]
    data["TenorRefLongitudinal"] = data["PesoRefLongitudinal"] * 1000 / area_proyecto
    data["TenorEstribos"] = data["PesoEstribos"] * 1000 / area_proyecto
    data["TenorTotal"] = data["PesoTotal"] * 1000 / area_proyecto

    data["Longitud"] = data["Longitud"].apply(str)
    data["Análisis"] = data["Calibres"] + " % " + data["Longitud"] + "m"

    min_index = data["TenorTotal"].T.idxmin()
    min_index_name = data.iloc[min_index]["Análisis"]
    data["TenorTotalMin"] = data["TenorTotal"] - min(data["TenorTotal"])
    data[f"Tenor Total ({min_index_name})"] = data["TenorTotalMin"] / max(
        data["TenorTotalMin"]
    )

    min_index = data["PesoTotal"].T.idxmin()
    min_index_name = data.iloc[min_index]["Análisis"]
    data["PesoTotalMin"] = data["PesoTotal"] - min(data["PesoTotal"])
    data[f"Peso Total ({min_index_name})"] = data["PesoTotalMin"] / max(
        data["PesoTotalMin"]
    )

    min_index = data["NúmeroBarras"].T.idxmin()
    min_index_name = data.iloc[min_index]["Análisis"]
    data["NúmeroBarrasMin"] = data["NúmeroBarras"] - min(data["NúmeroBarras"])
    data[f"Número Barras ({min_index_name})"] = data["NúmeroBarrasMin"] / max(
        data["NúmeroBarrasMin"]
    )

    min_index = data["NúmeroFiguras"].T.idxmin()
    min_index_name = data.iloc[min_index]["Análisis"]
    data["NúmeroFigurasMin"] = data["NúmeroFiguras"] - min(data["NúmeroFiguras"])
    data[f"Número Figuras ({min_index_name})"] = data["NúmeroFigurasMin"] / max(
        data["NúmeroFigurasMin"]
    )

    return data


st.set_page_config(page_title="ProDes", layout="wide")
area_proyecto = 15531

data = pd.read_csv("./defaults.csv")

uploaded_file = st.file_uploader("Cargar CSV", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

if data is not None:
    area_proyecto = st.sidebar.number_input(
        "Area del proyecto (m²)", value=15531, min_value=1
    )
    update_dataframe(data, area_proyecto)
    view_mode = st.sidebar.selectbox("Modo de vista", options=["group", "stack"])
    graficar_data(data)
