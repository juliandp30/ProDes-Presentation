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

if data is not None:
    area_proyecto = st.sidebar.number_input(
        "Área del proyecto (m²)", value=10000, min_value=1
    )




# data_heads = data.columns.values
# data_values = data.values

# results = {}

# for data_i in data_values:

#     analysis_results = pr.new_analysis_constructor()
#     analysis_results = pr.asign_values(data_i, data_heads, analysis_results)
#     results[data_i[0]] = analysis_results

# print(data_heads)