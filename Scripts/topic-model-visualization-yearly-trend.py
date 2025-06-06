
import pandas as pd
import plotly.express as px
import os

#  Load the dataset
df = pd.read_csv("topic-model.csv")

# Remove unassigned topics and meaningless topics
df = df[df['Topic'] != -1]
df = df[~df['topic_1'].str.lower().isin(['my', 'of', 'to', 'and', 'you', 'we'])]

# Create a readable topic label
df['topic_label'] = df['topic_1'] + " (ID " + df['Topic'].astype(str) + ")"

#  Map topic labels to clearer human-readable themes
theme_mapping = {
    "bank (ID 0)": "West Bank Conflict",
    "captives (ID 1)": "Hostages / Captives",
    "hospital (ID 3)": "Health Infrastructure",
    "iran (ID 4)": "Regional Politics (Iran & Lebenon)",
    "gaza (ID 5)": "Gaza Coverage"
}

df['theme'] = df['topic_label'].map(theme_mapping)

# Keep only rows with valid themes
df_top = df[df['theme'].notnull()]

# Group by year and theme
topic_trends = df_top.groupby(['year', 'theme']).size().reset_index(name='count')

# Create a grouped bar chart
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

#  Clean layout
fig.update_layout(
    template="plotly_white",
    title_font_size=18,
    xaxis=dict(dtick=1),
    legend_title="Topic"
)

# Save and display the chart

fig.show()
# Get the directory where the script is located                                 
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one level and into the outputs folder                                   
output_dir = os.path.abspath(os.path.join(current_dir, '..', 'outputs'))

# Ensure directory exists                                                        
os.makedirs(output_dir, exist_ok=True)

# Define full path to output file                                                  
output_file = os.path.join(output_dir, "Top 5 Topic Frequencies by Year.html")

# Save Plotly figure
fig.write_html(output_file)
