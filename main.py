import streamlit as st
import pandas as pd
import re

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


def extract_minute(minute_str):
    if pd.isna(minute_str):
        return None
    minute_str = minute_str.replace("'", "")
    parts = re.split(r"\+|’", minute_str)
    try:
        return sum(int(p) for p in parts if p.isdigit())
    except:
        return None

df["MinuteValue"] = df["Minute"].apply(extract_minute)

# Drop rows with missing Year or MinuteValue
df_clean = df.dropna(subset=["Year", "MinuteValue"])

# Group by Year and calculate average minute
minutes_per_goal = df_clean.groupby("Year")["MinuteValue"].mean().round(2).reset_index()
minutes_per_goal["Year"] = minutes_per_goal["Year"].astype(str)
minutes_per_goal = minutes_per_goal.set_index("Year")

# Calculate total average minute
total_avg_minute = round(df_clean["MinuteValue"].mean(), 2)

# Streamlit UI
st.title("Cristiano Ronaldo - Average Minute per Goal (Per Year)")

# Display total average
st.markdown(f"**Overall Average Minute per Goal:** {total_avg_minute}")

# Line chart
st.line_chart(minutes_per_goal)