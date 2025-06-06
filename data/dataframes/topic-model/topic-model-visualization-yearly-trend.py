# visualize_topic_trends_bar.py

import pandas as pd
import plotly.express as px
import os

# Step 1: Load the dataset
df = pd.read_csv("topic-model.csv")

# Step 2: Remove unassigned topics and meaningless topics
df = df[df['Topic'] != -1]
df = df[~df['topic_1'].str.lower().isin(['my', 'of', 'to', 'and', 'you', 'we'])]

# Step 3: Create a readable topic label
df['topic_label'] = df['topic_1'] + " (ID " + df['Topic'].astype(str) + ")"

# Step 4: Map topic labels to clearer human-readable themes
theme_mapping = {
    "bank (ID 0)": "West Bank Conflict",
    "captives (ID 1)": "Hostages / Captives",
    "hospital (ID 3)": "Health Infrastructure",
    "iran (ID 4)": "Regional Politics (Iran & Lebenon)",
    "gaza (ID 5)": "Gaza Coverage"
}

df['theme'] = df['topic_label'].map(theme_mapping)

# Step 5: Keep only rows with valid themes
df_top = df[df['theme'].notnull()]

# Step 6: Group by year and theme
topic_trends = df_top.groupby(['year', 'theme']).size().reset_index(name='count')

# Step 7: Create a grouped bar chart
fig = px.bar(
    topic_trends,
    x="year",
    y="count",
    color="theme",
    barmode="group",
    title="Top 5 Topic Frequencies by Year in Al-Jazeera Gaza Corpus (2021–2024)",
    labels={
        "year": "Year",
        "count": "Number of Articles",
        "theme": "Topic Theme"
    }
)

# Optional: Clean layout
fig.update_layout(
    template="plotly_white",
    title_font_size=18,
    xaxis=dict(dtick=1),
    legend_title="Topic"
)

# Step 8: Save and display the chart

fig.show()
