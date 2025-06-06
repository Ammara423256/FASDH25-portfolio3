# explore_topic_model.py

import pandas as pd
import os

# Load the dataset
df = pd.read_csv("topic-model.csv")

# Show basic info about the dataset
print(" Dataset Info:")
print(df.info())
print()

# Show the first few rows
print(" First 5 Rows:")
print(df.head())
print()

# Show basic statistics for numeric columns
print(" Numeric Summary:")
print(df.describe())
print()

# Show column names
print(" Column Names:")
print(df.columns.tolist())
print()

# Count total rows and check for null values
print(" Missing Values:")
print(df.isnull().sum())
print()

# Count unique topics (including -1)
print(" Topic Distribution:")
print(df['Topic'].value_counts().sort_index())

# Drop unassigned topics, Topic = -1
df = df[df['Topic'] != -1]

# Create a readable topic label
df['topic_label'] = df['topic_1'] + " (ID " + df['Topic'].astype(str) + ")"

# Remove Stop Words to filter out meaningless topic keywords
stopwords = ['my', 'of', 'to', 'and', 'you', 'we']
df = df[~df['topic_1'].str.lower().isin(stopwords)]

# Show the Top 10 Topics
top_topics = df['topic_label'].value_counts().head(10)
print(" Top 10 topic labels:")
print(top_topics)

# Display all unique first topic keyword (topic-1)
print("Unique primary topic keywords:")
print(df['topic_1'].unique())

# Show most common co-occuring keywords when topic-1 is "bank"
print("\n Other keywords with topic_1 = 'bank':")
print(df[df['topic_1'] == 'bank'][['topic_2', 'topic_3', 'topic_4']].value_counts().head(5))

# Show sample article titles from topic_1 = 'bank'
print("\n Sample titles for topic_1 = 'bank':")
print(df[df['topic_1'] == 'bank']['title'].sample(5, random_state=1)) # Last part of code taken from AI (Conversation 2) 

# Create a proper 'year_month' datetime column
df["year_month"] = pd.to_datetime(dict(year=df["year"], month=df["month"], day=1))

# Define the selected timeframe
start = pd.to_datetime("2023-06")
end = pd.to_datetime("2024-04")

# Filter to select the data range
df = df[(df["year_month"] >= start) & (df["year_month"] <= end)]

# Calculate relative frequency % per month (Idea taken from Peter's feedback and AI Conversation 3)
# Calculate total article count per month (DENOMINATOR)
monthly_totals = df.groupby('year_month').size().rename("total_articles").reset_index()

# Count number of articles per topic per month (NUMERATOR)
monthly_topic_counts = df.groupby(['year_month', 'topic_label']).size().reset_index(name='count')

# Merge and compute relative frequency
topic_monthly = pd.merge(monthly_topic_counts, monthly_totals, on='year_month')
topic_monthly["relative_freq"] = (topic_monthly["count"] / topic_monthly["total_articles"]) * 100

# Identify top 5 topics overall
top_5 = df["topic_label"].value_counts().head(5).index

# Filter only those top 5 topics for visualization
final_topics = topic_monthly[topic_monthly["topic_label"].isin(top_5)].copy()

# Save to CSV
final_topics.to_csv("outputs/final_topic_relative_freq.csv", index=False)

# Preview
print("\nRelative Frequency of Top 5 Topics Per Month:")
print(final_topics.head())

# Filter conflict-related topics
conflict_keywords = ['gaza', 'hostages', 'israel', 'military', 'hamas', 'war', 'strike',
                     'bank', 'settlements', 'netanyahu', 'aqsa', 'iran', 'rockets',
                     'lebanon', 'jerusalem', 'erdogan', 'masafer']
conflict_df = df[df['topic_1'].str.lower().isin(conflict_keywords)]
print("\n Conflict-related article count by year:")
print(conflict_df.groupby('year').size())

# Filter humanitarian-related topics
humanitarian_keywords = ['hospital', 'refugees', 'aid', 'un', 'food', 'injury', 'shelter',
                         'resolution', 'journalists', 'contributors', 'updates']
aid_df = df[df['topic_1'].str.lower().isin(humanitarian_keywords)]
print("\n Humanitarian-related article count by year:")
print(aid_df.groupby('year').size())

# Monthly Analysis: Conflict vs Humanitarian
conflict_df = conflict_df.copy()
aid_df = aid_df.copy()
conflict_df['theme_type'] = 'conflict_count'
aid_df['theme_type'] = 'humanitarian_count'

# Group by month and theme_type
conflict_monthly = conflict_df.groupby('year_month').size().reset_index(name='count')
conflict_monthly['theme'] = 'conflict_count'

humanitarian_monthly = aid_df.groupby('year_month').size().reset_index(name='count')
humanitarian_monthly['theme'] = 'humanitarian_count'

# Combine both datasets
combined_monthly = pd.concat([conflict_monthly, humanitarian_monthly])
combined_monthly.to_csv("outputs/conflict_vs_aid_trends.csv", index=False)

# Manual theme mapping for interpretation and later visualization (AI conversation 1)
theme_map = {
    0: 'West Bank (Geopolitical)',
    1: 'Hostages / Captives',
    3: 'Health Infrastructure',
    4: 'Regional Politics (Iran)',
    5: 'Gaza Coverage'
}
df['theme'] = df['Topic'].map(theme_map)

print("\nTheme mapping sample:")

