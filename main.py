import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# Load data
df = pd.read_csv("ronaldo.csv")

# Convert Date to datetime and extract year
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
df["Year"] = df["Date"].dt.year

# Filter out rows where Club or Year is missing
club_df = df.dropna(subset=["Club", "Year"])

# Group by Year and Club, count goals
goals_per_year = club_df.groupby(["Year", "Club"]).size().reset_index(name="Goals")

# Streamlit app title
st.title("Cristiano Ronaldo - Club Goals Per Year")

# Let user pick clubs to include
clubs = goals_per_year["Club"].unique()
selected_clubs = st.multiselect("Select Clubs", clubs, default=list(clubs))

# Filter data based on selection
filtered_data = goals_per_year[goals_per_year["Club"].isin(selected_clubs)]

# Plot using matplotlib
fig, ax = plt.subplots(figsize=(10, 5))
for club in selected_clubs:
    club_data = filtered_data[filtered_data["Club"] == club]
    ax.plot(club_data["Year"], club_data["Goals"], marker='o', label=club)

ax.set_xlabel("Year")
ax.set_ylabel("Goals")
ax.set_title("Goals per Year by Club")
ax.legend()
st.pyplot(fig)