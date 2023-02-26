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


with st.sidebar.form(key ='Form1'):

    if data is not None:
        area_proyecto = st.number_input(
            "Área del proyecto (m²)", value=10000, min_value=1
        )

    for i in range (5):
        precio_i = st.number_input(
                "Peso barra " + str(i), value=5000, min_value=1
            )
            
    user_word = st.text_input("Enter a keyword", "habs")    
    select_language = st.radio('Tweet language', ('All', 'English', 'French'))
    include_retweets = st.checkbox('Include retweets in data')
    num_of_tweets = st.number_input('Maximum number of tweets', 100)
    submitted1 = st.form_submit_button(label = 'Guardar precios')



# data_heads = data.columns.values
# data_values = data.values

# results = {}

# for data_i in data_values:

#     analysis_results = pr.new_analysis_constructor()
#     analysis_results = pr.asign_values(data_i, data_heads, analysis_results)
#     results[data_i[0]] = analysis_results

# print(data_heads)