# Home.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Load and preprocess data
df = pd.read_csv("df.csv", parse_dates=["Date"])
df['Month'] = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.strftime('%B')
df['Year'] = df['Date'].dt.year
month_order = pd.date_range("2023-01-01", periods=12, freq='M').strftime('%B').tolist()

st.title("Group-Level Spending Dashboard")

# Group-wise summary chart
summary = df.groupby('Persons')['Spend'].sum().sort_values(ascending=False).reset_index()
fig1 = px.bar(summary, x='Persons', y='Spend', title='Overall Spend by Person', labels={'Spend': 'Total Spend'})
fig1.update_layout(template='plotly_white')
st.plotly_chart(fig1, use_container_width=True)

# Monthly total spend
monthly_summary = df.groupby('Month_Name')['Spend'].sum().reindex(month_order).reset_index()
fig2 = px.line(monthly_summary, x='Month_Name', y='Spend', title='Overall Monthly Spend by Group', markers=True)
fig2.update_layout(template='plotly_white')
st.plotly_chart(fig2, use_container_width=True)
