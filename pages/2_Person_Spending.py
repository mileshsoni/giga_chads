# Person_Spending.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Load and preprocess data
df = pd.read_csv("df.csv", parse_dates=["Date"])
df['Month'] = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.strftime('%B')
df['Year'] = df['Date'].dt.year
month_order = pd.date_range("2023-01-01", periods=12, freq='M').strftime('%B').tolist()

def plot_monthly_spend(df, year=None, person=None):
    df_filtered = df.copy()
    title = "Monthly Spend"

    if person:
        df_filtered = df_filtered[df_filtered['Persons'] == person]
        title += f" for {person}"
    if year:
        df_filtered = df_filtered[df_filtered['Year'] == year]
        title += f" in {year}"
    else:
        title += " (All Years)"

    monthly_summary = df_filtered.groupby('Month_Name')['Spend'].sum().reindex(month_order).reset_index()

    fig = px.line(
        monthly_summary,
        x='Month_Name',
        y='Spend',
        title=title,
        markers=True,
        labels={'Month_Name': 'Month', 'Spend': 'Total Spend'}
    )
    fig.update_layout(template='plotly_white')
    return fig

st.title("Person-Level Spending Analysis")

# Sidebar filters
person_list = df['Persons'].dropna().unique().tolist()
year_list = sorted(df['Year'].dropna().unique().tolist())

selected_person = st.sidebar.selectbox("Select Person", person_list)
selected_year = st.sidebar.selectbox("Select Year (Optional)", [None] + year_list)

st.header("Monthly Trend for Selected Person")
fig = plot_monthly_spend(df, year=selected_year, person=selected_person)
st.plotly_chart(fig, use_container_width=True)
