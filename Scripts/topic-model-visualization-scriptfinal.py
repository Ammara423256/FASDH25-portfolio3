
import pandas as pd
import plotly.express as px
import os

# Load preprocessed datasets
df_top = pd.read_csv("final_topic_relative_freq.csv")
combined_monthly = pd.read_csv("conflict_vs_aid_trends.csv")

# Convert 'year_month' to datetime if it's not already
df_top['year_month'] = pd.to_datetime(df_top['year_month'])
combined_monthly['year_month'] = pd.to_datetime(combined_monthly['year_month'])

# Create a grouped bar chart for topic frequency by month
fig = px.bar(
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

fig.show()
# Get the directory where the script is located                                
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one level and into the outputs folder                                  
output_dir = os.path.abspath(os.path.join(current_dir, '..', 'Outputs'))

# Ensure directory exists                                                      
os.makedirs(output_dir, exist_ok=True)

# Define full path to output file                                                
output_file = os.path.join(output_dir, "monthly_top5_topics.html")

# Save Plotly figure
fig.write_html(output_file)

# Plot the monthly trend: Conflict vs Humanitarian Themes
fig=px.bar(
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
fig.update_layout(template="plotly_white", xaxis=dict(dtick="M1"))

fig.show()
# Define full path to output file                                                 
output_file = os.path.join(output_dir, "conflict_vs_humanitarian.html")

# Save Plotly figure
fig.write_html(output_file)
