import pandas as pd
import plotly.express as px
import os

# Load the csv file
df = pd.read_csv("1-gram.csv")

#  Create a date column  
df["date"] = pd.to_datetime(dict(year=df["year"], month=df["month"], day=df["day"]))  

# List of common stop words (online source + manual additions)
stop_words = [
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she",
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
    "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of",
    "at", "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then",
    "once", "here", "there", "when", "where", "why", "how", "all", "any",
    "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor",
    "not", "only", "own", "same", "so", "than", "too", "very", "can", "will",
    "just", "don", "should", "now", "15", "s", "said" , "one", "would", "told",
    "also", "since", "two", "al", "including"
]

# Remove stop words from the dataframe based on '1-gram' column
df_filtered = df[~df["1-gram"].str.lower().isin(stop_words)]

# Defining two lists of 1-gram keywords based on frequency and theme
# Making 2 groups of words based on top 20 frequencies + manual additions

# People-related terms: high frequency words + Manual additions
people_terms = [
    'palestinian', 'people', 'killed', 'children',
    'women', 'families', 'man', 'citizens', 'victims'
]

# Power-related terms: state/military terms + manual additions
power_terms = [
    'israel', 'us', 'hamas', 'military', 'forces', 'attacks', 'occupied',
    'government', 'official', 'authority', 'minister', 'state'
]

# Combine both lists of keywords
keywords = people_terms + power_terms

# Filter dataframe to only include rows where 1-gram is in keywords list
df_keywords = df_filtered[df_filtered["1-gram"].isin(keywords)].copy()

# Defining a new function to assign themes
def assign_theme(word):
    if word in people_terms:
        return "People"
    else:
        return "Power"

# Apply the function to the '1-gram' column
df_keywords["theme"] = df_keywords["1-gram"].apply(assign_theme)

# Group by theme overall and sum counts
df_grouped = df_keywords.groupby("theme")["count"].sum().reset_index()

# Print the grouped counts by theme
print(df_grouped)

# Plot overall mentions by theme using a bar chart
fig = px.bar(df_grouped, x="theme", y="count",
             title="Total Mentions by Theme (People vs Power)",
             color="theme", color_discrete_map={"People": "blue", "Power": "red"})
fig.show()

# Get the current script directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the outputs directory (one level up)
output_dir = os.path.abspath(os.path.join(current_dir, '..', 'outputs'))

# Ensure the outputs directory exists
os.makedirs(output_dir, exist_ok=True)

# Define full path to output file
output_file = os.path.join(output_dir, "Total Mentions by theme 1-grams.html")
fig.write_html(output_file)

# Define start and end dates to filter data by time frame
start_date = pd.to_datetime("2023-06-01")
end_date = pd.to_datetime("2024-04-01")

# Filter dataset within the specified date range
df_time_filtered = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

# Remove stop words again on the time-filtered data
df_filtered_time = df_time_filtered[~df_time_filtered["1-gram"].str.lower().isin(stop_words)]

# Filter for keywords only on time-filtered data
df_keywords_time = df_filtered_time[df_filtered_time["1-gram"].isin(keywords)].copy()

# Apply the function to create the 'theme' column
df_keywords_time["theme"] = df_keywords_time["1-gram"].apply(assign_theme)

# Create a 'year_month' column for grouping by month
df_keywords_time["year_month"] = (
    df_keywords_time["date"].dt.year.astype(str) + "-" +
    df_keywords_time["date"].dt.month.astype(str)
)

# Group by 'year_month' and 'theme' and sum counts for monthly counts
monthly_theme_counts = df_keywords_time.groupby(["year_month", "theme"], as_index=False)["count"].sum()

# Sort by month so that X-axis in the plot is ordered
monthly_theme_counts = monthly_theme_counts.sort_values("year_month")

# Plot monthly mentions by theme in a grouped bar chart
fig = px.bar(monthly_theme_counts,
             x="year_month", y="count", color="theme", barmode="group",
             title="Monthly Mentions by Theme (People vs Power) June 2023 - April 2024",
             labels={"year_month": "Month", "count": "Count", "theme": "Theme"},
             color_discrete_map={"People": "blue", "Power": "red"})
fig.show()

# Define full path to output file (fixed by adding .html extension)
output_file = os.path.join(output_dir, "Monthly Mentions by Theme (People vs Power).html")
fig.write_html(output_file)

# Group by 'year_month' and '1-gram' to get monthly counts for each term
monthly_word_counts = df_keywords_time.groupby(["year_month", "1-gram"], as_index=False)["count"].sum()

# Sort by month for correct order on X-axis
monthly_word_counts = monthly_word_counts.sort_values("year_month")

# Plot stacked bar chart
fig = px.bar(monthly_word_counts,
             x="year_month", y="count", color="1-gram", barmode="stack",
             title="Monthly Mentions of Individual Terms (Stacked by People and Power Terms)",
             labels={"year_month": "Month", "count": "Count", "1-gram": "Keyword"})
fig.show()

# Define full path to output file
output_file = os.path.join(output_dir, "Monthly Mentions of Individual Terms (Stacked by People and Power Terms).html")
fig.write_html(output_file)

# Add 'theme' label again
monthly_word_counts["theme"] = monthly_word_counts["1-gram"].apply(assign_theme)

# Plot faceted stacked bar chart (one row for each theme)
fig = px.bar(monthly_word_counts,
             x="year_month", y="count", color="1-gram", barmode="stack",
             facet_row="theme",
             title="Monthly Mentions of Terms by Theme (Stacked within Each Theme)",
             labels={"year_month": "Month", "count": "Count", "1-gram": "Keyword"})
fig.show()

# Define full path to output file
output_file = os.path.join(output_dir, "Monthly Mentions of Terms by Theme (Stacked within Each Theme).html")
fig.write_html(output_file)
