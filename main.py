import streamlit as st
import pandas as pd
import re
import altair as alt
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


# UI
st.title("Cristiano Ronaldo - Top 5 Favorite Opponents")
st.markdown("These are the teams he has scored the most goals against.")


# Count goals per opponent
top_opponents = df["Opponent"].value_counts().head(5).reset_index()
top_opponents.columns = ["Opponent", "Goals"]

# Altair bar chart with horizontal labels and unique colors
bar_chart = alt.Chart(top_opponents).mark_bar().encode(
    x=alt.X("Opponent", sort="-y", axis=alt.Axis(labelAngle=0)),
    y="Goals",
    color=alt.Color("Opponent", legend=None)  # Color by opponent, hide legend
).properties(width=600, height=400)

st.altair_chart(bar_chart, use_container_width=True)

# Process minute values (only once)
df["MinuteValue"] = df["Minute"].apply(extract_minute)
df = df.dropna(subset=["MinuteValue"])
df = df[(df["MinuteValue"] >= 0) & (df["MinuteValue"] <= 120)]

# Rank each goal within the same minute to separate on Y axis
df["StackY"] = df.groupby("MinuteValue").cumcount()

# Streamlit UI
st.title("Cristiano Ronaldo - Stacked Goal Timing Distribution")
st.markdown("Each dot represents a goal. Minutes with more than one goal now stack vertically.")

# Altair dot plot with stacked y-axis
dot_chart = alt.Chart(df).mark_circle(size=60, opacity=0.6).encode(
    x=alt.X("MinuteValue:Q", title="Minute of Goal", scale=alt.Scale(domain=[0, 120])),
    y=alt.Y("StackY:Q", axis=None),  # Hide Y axis since it's just for stacking
    color=alt.Color("Goal Type", legend=None),
    tooltip=["Opponent", "Club", "Date", "MinuteValue", "Goal Type"]
).properties(height=300)

st.altair_chart(dot_chart, use_container_width=True)

# Goals by minute intervals
st.title("Goals by Minute Intervals")
st.markdown("Distribution of goals across different periods of the game")

# Calculate goals by minute intervals
df["MinuteInterval"] = pd.cut(
    df["MinuteValue"], 
    bins=[0, 15, 30, 45, 60, 75, 90, 105, 120], 
    labels=["0-15", "15-30", "30-45", "45-60", "60-75", "75-90", "90-105", "105-120"]
)

# Count goals by minute interval and create a better visualization
interval_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("MinuteInterval:N", title="Game Period (minutes)"),
    y=alt.Y("count():Q", title="Number of Goals"),
    color=alt.value("#FF4B4B")  # Use a nice red color
).properties(
    title="Goals Scored in Different Game Periods",
    width=600,
    height=400
)

st.altair_chart(interval_chart, use_container_width=True)


