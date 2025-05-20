import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("ronaldo.csv")

# Convert Date to datetime and extract year
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
df["Year"] = df["Date"].dt.year

# Drop rows where Year is missing
df = df.dropna(subset=["Year"])

# Group by Year and count goals
goals_per_year = df.groupby("Year").size().reset_index(name="Goals")

# Convert Year to string to avoid formatting like 2,008
goals_per_year["Year"] = goals_per_year["Year"].astype(str)
goals_per_year = goals_per_year.set_index("Year")

# Streamlit UI
st.title("Cristiano Ronaldo - Goals Per Year")

# Line chart of total goals per year
st.line_chart(goals_per_year)