# importing necessary libraries
import pandas as pd
import plotly.express as px
import os

# Loading the 1 gram  csv file
file_path = "1-gram.csv"

# Reading the csv file
df = pd.read_csv("1-gram.csv")

# Printing to understand the structure of csv file
print(df.head())

# Printing the first few rows to confirm that the data is loaded correctly
print(df.head(10))

# Checking the columns name
print(df.columns)

# Checking for missing columns
print(df.isnull().sum())

# Sorting the dataset by 'count' in descending order to see most frequent words
df = df.sort_values(by="count", ascending=False)  
print(df.head(10))  # prints the top 10 most frequent 1-grams

# Creating a date column using year, month, and day
df["date"] = pd.to_datetime(dict(year=df["year"], month=df["month"], day=df["day"]))  
print(df[["date", "1-gram", "count"]].head())  # View new date column with words and count

#Removing stop words

# Listing common stop words (online source + Manual additions)
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
    "also" "since", "two", "since", "two", "al", "also", "including"
]

#  Removing rows where the '1-gram' is a stop word
df_filtered = df[~df["1-gram"].str.lower().isin(stop_words)]


# Checking the top frequent words after filtering
top_words = df_filtered.groupby("1-gram")["count"].sum().sort_values(ascending=False).head(20)

# Print the top 20 words
print(top_words)

# Group the filtered dataset (stop words removed) by '1-gram' and sum the counts
df_filtered_grouped = df_filtered.groupby("1-gram")["count"].sum().reset_index()

# Sort the grouped dataframe in descending order to get the most frequent 1-grams
df_filtered_grouped = df_filtered_grouped.sort_values("count", ascending=False)

# Get the current script directory                                                #From chatgpt, refrence:Chat-4
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the outputs directory (one level up)                          #From chatgpt, refrence:Chat-4
output_dir = os.path.abspath(os.path.join(current_dir, '..', 'outputs'))

# Ensure the outputs directory exists                                             #From chatgpt, refrence:Chat-4
os.makedirs(output_dir, exist_ok=True)

# Define the full path to the CSV file                                            #From chatgpt, refrence:Chat-4
csv_output_path = os.path.join(output_dir, "1-gram_filtered.csv")

# Save the DataFrame as a CSV
df_filtered.to_csv(csv_output_path, index=False)

# Plot a bar graph to display the Top 20 most frequent 1-grams after removing stop words
fig = px.bar(df_filtered_grouped.head(20), x="1-gram", y="count",
             title="Top 20 Most Frequent 1-grams (Stop Words Removed)")
fig.show()


# Define full path to output file
output_file = os.path.join(output_dir, "Top 20 Most Frequent 1-grams.html")       

# Save Plotly figure
fig.write_html(output_file) 
