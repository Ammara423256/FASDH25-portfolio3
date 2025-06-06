import pandas as pd
import plotly.express as px
import os

# Load datasets
df = pd.read_csv("tfidf-over-0.3.csv")

#printing to familiriaze with the structure 
print(df.head())

# Check for missing values
print(df.isnull().sum())         #took from chatgpt, reference:CHAT-2

#combining columns into a single datetime column
df['date-filename1'] = pd.to_datetime(df[['year-1', 'month-1', 'day-1']].rename(   #renaming the columns
    columns={'year-1': 'year', 'month-1': 'month', 'day-1': 'day'}
))

df['date-filename2'] = pd.to_datetime(df[['year-2', 'month-2', 'day-2']].rename(
    columns={'year-2': 'year', 'month-2': 'month', 'day-2': 'day'}
))
print(df["date-filename1"])
print(df["date-filename2"])

#Defining the date range
start_date = pd.to_datetime('2023-5-07')
end_date = pd.to_datetime('2024-10-31')

# Filtering rows where both articles fall within the date range
filtered_df = df[(df['date-filename1'] >= start_date) & (df['date-filename1'] <= end_date) &
                 (df['date-filename2'] >= start_date) & (df['date-filename2'] <= end_date)]
print(filtered_df)

#sorting the filter data by similarity in ascending order
sorted_df = filtered_df.sort_values(by='similarity', ascending=False)
print(sorted_df[['filename-1', 'filename-2', 'similarity']].head(10))

# Counting how often each article appears in the top similar pairs
file_counts = pd.concat([sorted_df['filename-1'], sorted_df['filename-2']]).value_counts()
print(file_counts.head(10))

# Convert the 'date-filename1' column to a monthly period format (e.g., '2025-05') and store it in a new column 'month1'
sorted_df['month_1'] = sorted_df['date-filename1'].dt.to_period('M')

# Convert the 'date-filname2' column to a monthly period format and store it in a new column 'month2'
sorted_df["month_2"] = sorted_df["date-filename2"].dt.to_period("M")
                                                                                             #(took help from chatgpt,reference: chat-1)
# Grouping the DataFrame by the two monthly period columns, 'month1' and 'month2', 
# then calculate the mean of the 'similarity' values for each group
avg_similarity_by_both = sorted_df.groupby(['month_1', 'month_2'])['similarity'].mean()

#Reset the index of the resulting grouped DataFrame to convert the grouped indices into regular columns
avg_similarity_by_both = avg_similarity_by_both.reset_index()


# Get the current script directory                                               #From chatgpt, refrence:Chat-4
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the outputs directory (one level up)                        #From chatgpt, refrence:Chat-4
output_dir = os.path.abspath(os.path.join(current_dir, '..', 'outputs'))

# Ensure the outputs directory exists                                            #From chatgpt, refrence:Chat-4
os.makedirs(output_dir, exist_ok=True)

# Define the full path to the CSV file                                            #From chatgpt, refrence:Chat-4
csv_output_path = os.path.join(output_dir, "Average similarity of pairs per month.csv")

# Save the DataFrame as a CSV
avg_similarity_by_both.to_csv(csv_output_path, index=False)


# Convert months to string if needed
avg_similarity_by_both['month_1'] = avg_similarity_by_both['month_1'].astype(str)
avg_similarity_by_both['month_2'] = avg_similarity_by_both['month_2'].astype(str)

fig = px.scatter(
    avg_similarity_by_both,
    x='month_1',
    y='month_2',
    size='similarity',          
    color='similarity'
    color_continuous_scale='Viridis',
    title='Average similarity of pairs per month',
    labels={'month_1': 'Month 1', 'month_2': 'Month2 ', 'similarity': 'Avg Similarity'}
)

fig.show()


# Define full path to output file
output_file = os.path.join(output_dir, "Average similarity of pairs per month.html")       #from chatgpt, reference:chat-4

# Save Plotly figure
fig.write_html(output_file)














































      




