# import library
import pandas as pd #data manipulate
import streamlit as st #web abb (Dashboard (DB))
import numpy as np # function (math,arrays)
import matplotlib.pyplot as plt # visualized
import seaborn as sns # visualized
import plotly.express as px # ***visualized
import re # set of strings that matches


#layout
st.set_page_config(
    page_title="Condo bkk",
    layout = 'wide',
)
# Add custom CSS to center-align the title
st.markdown(
    """
    <style>
    .title {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Center-aligned title
st.markdown("<h1 class='title'>Accommodation Search and Management Platform in Bangkok:</h1>", unsafe_allow_html=True)
st.markdown("<h1 class='title'>Simplifying What You Need</h1>", unsafe_allow_html=True)


url = 'https://github.com/Trinsararom/data_eng/raw/main/Proprety_data%20-%20Proprety_data.csv'
df = pd.read_csv(url,  thousands=',' , parse_dates=['Date'])

# Sidebar with search input
search_input = st.text_input("Search for Property e.g. siam, Noble Revolve Ratchada", "")

# Filtered DataFrame based on search input
if search_input:
    filtered_df = df[df['Property Name'].str.contains(search_input, case=False, na=False)]
else:
    filtered_df = df

# filtered by variable
col1 , col2  = st.columns(2)
with col1:
    filter_LT = st.checkbox('Filter by 	Rent Prices')
    if filter_LT:
        min_val, max_val = int(400), int(480000)
        RP_min, RP_max = st.slider('Select a range of Rent Prices', min_val, max_val, (min_val, max_val))
        filtered_df = filtered_df[(filtered_df['Rent Prices'] >= RP_min) & (filtered_df['Rent Prices'] <= RP_max)]
    else:
        filtered_df = filtered_df.copy()
with col2:
    filter_LOS = st.checkbox('Filter by Room size')
    if filter_LOS:
        min_val, max_val = int(18), int(400)
        RS_min, RS_max = st.slider('Select a range of Room size', min_val, max_val, (min_val, max_val))
        filtered_df = filtered_df[(filtered_df['Room size'] >= RS_min) & (filtered_df['Room size'] <= RS_max)]
    else:   
        filtered_df = filtered_df.copy()



col1, col2 = st.columns(2)
with col1:
    # Create a scatter plot of Rent Prices vs. Room size
    grouped0 = filtered_df.groupby(['Room size','Property Name'])['Rent Prices'].mean().reset_index()
    fig1 = px.scatter(grouped0, x='Room size', y='Rent Prices', title='Rent Prices vs. Room Size', color = 'Property Name')
    st.plotly_chart(fig1)

with col2:
    list_tab = ['the top 10 properties with the highest Rent Prices', 'the bottom 10 properties with the highest Rent Prices']
    t , l = st.tabs(list_tab)
    with t :
        grouped = filtered_df.groupby('Property Name')['Rent Prices'].mean().reset_index()
        top10_properties = grouped.nlargest(10, 'Rent Prices')
        fig2 = px.bar(top10_properties, x='Property Name', y='Rent Prices', title='Top 10 Properties with Highest Rent Prices', color = 'Property Name')
        st.plotly_chart(fig2)

    with l :
        grouped = filtered_df.groupby('Property Name')['Rent Prices'].mean().reset_index()
        bottom10_properties = grouped.nsmallest(10, 'Rent Prices') 
        fig3 = px.bar(bottom10_properties, x='Property Name', y='Rent Prices', title='Top 10 Properties with Lowest Rent Prices', color='Property Name')
        st.plotly_chart(fig3)