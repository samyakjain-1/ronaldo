import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("ronaldo.csv")

# Convert Date to datetime and extract year
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
df["Year"] = df["Date"].dt.year

# Filter for valid Club and Year data
club_df = df.dropna(subset=["Club", "Year"])

# Group by Year and Club
goals_per_year = club_df.groupby(["Year", "Club"]).size().reset_index(name="Goals")

# Streamlit app UI
st.title("Cristiano Ronaldo - Club Goals Per Year")

# Multiselect club filter
clubs = goals_per_year["Club"].unique()
selected_clubs = st.multiselect("Select Clubs", sorted(clubs), default=list(clubs))

# Filter the grouped data
filtered = goals_per_year[goals_per_year["Club"].isin(selected_clubs)]

# Pivot the data so each club is a column, years are the index
pivot_df = filtered.pivot(index="Year", columns="Club", values="Goals").fillna(0).astype(int)

# Show chart
st.line_chart(pivot_df)
