import pandas as pd
import plotly.express as px

# Load the CSV file
df = pd.read_csv("topic-model.csv")

# Display column names and preview selected topic columns to columns and unique values
print(df.columns)
print(df[['Topic', 'topic_1', 'topic_2', 'topic_3', 'topic_4']].head())
print("Months available:", df['month'].unique())
print("Years available:", df['year'].unique())

# Filter the dataset to include only articles from October to December 2023
df_filtered = df[(df['year'] == 2023) & (df['month'].isin([10, 11, 12]))].copy()

# Combine the top 4 topic words into a single string label for each article                             [AI (Conversation 2) + Class knowledge] 
df_filtered["Topic_label"] = df_filtered["topic_1"].astype(str)
df_filtered["Topic_label"] = df_filtered["Topic_label"] + ", " + df_filtered["topic_2"].astype(str)
df_filtered["Topic_label"] = df_filtered["Topic_label"] + ", " + df_filtered["topic_3"].astype(str)
df_filtered["Topic_label"] = df_filtered["Topic_label"] + ", " + df_filtered["topic_4"].astype(str)

#Aggregate the data: sum article counts by month and topic label 
topic_month_counts = df_filtered.groupby(['month', 'Topic_label'], as_index=False)['Count'].sum()

# Map month numbers to names for better readability in plots
month_map = {10: 'Oct', 11: 'Nov', 12: 'Dec'}
topic_month_counts['Month'] = topic_month_counts['month'].map(month_map)                  # [AI Code (Conversation 3)] 

# Plot total article counts for each topic label across the selected months
fig = px.bar(
    topic_month_counts,
    x='Month',
    y='Count',
    color='Topic_label',
    labels={'Count': 'Article Count', 'Month': 'Month', 'Topic_label': 'Topic Combination'},
    title='Article Counts by Topic and Month (Oct-Dec 2023)'
)
fig.show()

# Define keyword lists for theme classification
people_keywords = [
    "children", "civilians", "family", "families", "human", "people",
    "protest", "protesters", "refugees", "rights", "victims", "patients",
    "prisoners", "prison", "journalists", "journalist", "staff", "voters"
]

power_keywords = [
    "government", "police", "army", "military", "hamas",
    "israel", "israeli", "idf", "security", "president",
    "party", "congress", "leader", "leaders", "trump", "netanyahu", "putin",
    "biden", "starmer", "resolution", "arms", "weapons", "settlements",
    "settlement", "detention", "court"
]

# Reshape the topic columns into a long format to simplify keyword filtering     [(Mofified the code using an example from AI (conversation 4)]
df_melted = df_filtered.melt(
    id_vars=['month', 'year', 'Count'],
    value_vars=['topic_1', 'topic_2', 'topic_3', 'topic_4'],
    var_name='topic_position',
    value_name='topic_word'
)

# Keep only rows where the topic word matches one of the defined keywords
df_filtered_keywords = df_melted[df_melted['topic_word'].isin(people_keywords + power_keywords)].copy()

# Assign a theme label ("People" or "Power") to each matched keyword                      (Used concepts from future coder) 
def assign_theme(word):
    if word in people_keywords:
        return 'People'
    elif word in power_keywords:
        return 'Power'
    else:
        return 'Other'  # just in case

df_filtered_keywords['Theme'] = df_filtered_keywords['topic_word'].apply(assign_theme)

# Group counts by month and theme
theme_counts = df_filtered_keywords.groupby(['month', 'Theme'], as_index=False)['Count'].sum()
theme_counts['Month'] = theme_counts['month'].map(month_map)

# Plot article counts for each theme (People vs Power) across the selected months
fig_theme = px.bar(
    theme_counts,
    x='Month',
    y='Count',
    color='Theme',
    barmode='group',
    labels={'Count': 'Article Count', 'Month': 'Month', 'Theme': 'Theme'},
    title='Article Counts by Theme (People vs Power) Oct–Dec 2023'
)
fig_theme.show()

# Save plots as interactive HTML files
fig.write_html("topic_counts_by_month.html")
fig_theme.write_html("theme_counts_by_month.html")
