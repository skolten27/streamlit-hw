import pandas as pd
import zipfile
import plotly.express as px
import matplotlib.pyplot as plt
import requests
from io import BytesIO
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from my_plots import *
import streamlit as st

@st.cache_data
def load_name_data():
    names_file = 'https://www.ssa.gov/oact/babynames/names.zip'
    response = requests.get(names_file)
    with zipfile.ZipFile(BytesIO(response.content)) as z:
        dfs = []
        files = [file for file in z.namelist() if file.endswith('.txt')]
        for file in files:
            with z.open(file) as f:
                df = pd.read_csv(f, header=None)
                df.columns = ['name','sex','count']
                df['year'] = int(file[3:7])
                dfs.append(df)
        data = pd.concat(dfs, ignore_index=True)
    data['pct'] = data['count'] / data.groupby(['year', 'sex'])['count'].transform('sum')
    return data

@st.cache_data
def ohw(df):
    nunique_year = df.groupby(['name', 'sex'])['year'].nunique()
    one_hit_wonders = nunique_year[nunique_year == 1].index
    one_hit_wonder_data = df.set_index(['name', 'sex']).loc[one_hit_wonders].reset_index()
    return one_hit_wonder_data

data = load_name_data()
ohw_data = ohw(data)

st.title("Kolten's First Streamlit app!")

with st.sidebar:
    input_name = st.text_input('Enter a name:', 'Mary')
    year_input = st.slider("Year", min_value=1880, max_value=2023, value=2000)
    n_names = st.radio('Number of names per sex', [3, 4, 5, 6])
    sex_input = st.selectbox("Sex for One Hit Wonders", ["M", "F"])


tab1, tab2, tab3, tab4 = st.tabs(['Names', 'Year', 'Trends', 'One Hit Wonders'])

with tab1: 
    name_data = data[data['name']==input_name].copy()
    fig = px.line(name_data, x='year', y='count', color='sex')
    st.plotly_chart(fig)

with tab2:
    fig2 = top_names_plot(data, year=year_input, n=n_names)
    st.plotly_chart(fig2)

    st.write('Unique Names Table')
    output_table = unique_names_summary(data, 2000)
    st.dataframe(output_table)

with tab3:
    fig3 = name_trend_plot(data, name=input_name)
    st.plotly_chart(fig3)

with tab4:
    st.subheader(f"One-Hit Wonders in {year_input}")
    ohw_result = one_hit_wonders(ohw_data, year=year_input, sex=sex_input)
    if not ohw_result.empty:
        st.dataframe(ohw_result)
    else:
        st.write(f"No one-hit wonders found for {sex_input} in {year_input}.")