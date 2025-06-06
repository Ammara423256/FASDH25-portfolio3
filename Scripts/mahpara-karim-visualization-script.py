# visualize_topic_model.py

import pandas as pd
import plotly.express as px

# Load preprocessed datasets
df_top = pd.read_csv("outputs/final_topic_relative_freq.csv")
combined_monthly = pd.read_csv("outputs/conflict_vs_aid_trends.csv")

# Convert 'year_month' to datetime if it's not already
df_top['year_month'] = pd.to_datetime(df_top['year_month'])
combined_monthly['year_month'] = pd.to_datetime(combined_monthly['year_month'])

# Create a grouped bar chart for topic frequency by month
fig1 = px.bar(
    df_top,
    x="year_month",
    y="count",
    color="topic_label",
    barmode="group",
    title="Monthly Frequency of Top 5 Topics",
    labels={
        "year_month": "Month",
        "count": "Article Count",
        "topic_label": "Topic"
    },
    height=500
)
fig1.update_layout(template="plotly_white", xaxis=dict(dtick="M1"))
fig1.write_html("outputs/monthly_top5_topics.html")
fig1.show()

# Plot the monthly trend: Conflict vs Humanitarian Themes
fig2 = px.bar(
    combined_monthly,
    x='year_month',
    y='count',
    color='theme',
    barmode='group',
    title='Monthly Article Counts: Conflict vs. Humanitarian Themes',
    labels={
        'year_month': 'Month',
        'count': 'Number of Articles',
        'theme': 'Theme'
    },
    height=500
)
fig2.update_layout(template="plotly_white", xaxis=dict(dtick="M1"))
fig2.write_html("outputs/conflict_vs_humanitarian.html")
fig2.show()


