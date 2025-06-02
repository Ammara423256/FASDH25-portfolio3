#importing the necessary libraries
import pandas as pd
import plotly.express as px
import os

# Load datasets
tfidf_df = pd.read_csv("tfidf-over-0.3.csv")
topic_df = pd.read_csv("topic-model.csv")

#combining the separate colums to datetime column in topic model
topic_df['date'] = pd.to_datetime(topic_df[['year', 'month', 'day']])                #took help from chatgpt. reference:CHAT1

#setting the date range
start_date = pd.to_datetime('2023-5-07')   
end_date = pd.to_datetime('2024-10-31')

#Filter rows within the date range
filtered_topic_df = topic_df[(topic_df['date'] >= start_date) & (topic_df['date'] <= end_date)]

#combining columns into a single datetime column in tf-idf
tfidf_df['date-filename1'] = pd.to_datetime(tfidf_df[['year-1', 'month-1', 'day-1']].rename(   #renaming the columns
    columns={'year-1': 'year', 'month-1': 'month', 'day-1': 'day'}
))

tfidf_df['date-filename2'] = pd.to_datetime(tfidf_df[['year-2', 'month-2', 'day-2']].rename(
    columns={'year-2': 'year', 'month-2': 'month', 'day-2': 'day'}
))
print(tfidf_df["date-filename1"])
print(tfidf_df["date-filename2"])

# Filtering rows where both articles fall within the date range
filtered_tfidf_df = tfidf_df[(tfidf_df['date-filename1'] >= start_date) & (tfidf_df['date-filename1'] <= end_date) &
                             (tfidf_df['date-filename2'] >= start_date) & (tfidf_df['date-filename2'] <= end_date)]

#merging the dataframes for filename 1
merged_df1 = filtered_tfidf_df.merge(                                                   #took help from chatgpt, reference:CHAT-3
    filtered_topic_df,
    left_on=['filename-1', 'date-filename1'],
    right_on=['file', 'date'],
    how='left'
).rename(columns={'Topic': 'topic1'})

#checking the result
print(merged_df1[['filename-1', 'date-filename1', 'topic1']].head(10))

#merging the dataframe for filename 2
merged_df2 = merged_df1.merge(
    filtered_topic_df,
    left_on=['filename-2', 'date-filename2'],
    right_on=['file', 'date'],
    how='left'
).rename(columns={'Topic': 'topic2'})

#checking the result
print(merged_df2[['filename-2', 'date-filename2', 'topic2']].head(10))

# Optional cleanup: remove duplicate columns from the merge
merged_df2 = merged_df2.loc[:, ~merged_df2.columns.duplicated()]

#
same_topic_df = merged_df2[merged_df2['topic1'] == merged_df2['topic2']]

#Extracting monthly period for grouping
same_topic_df['month'] = same_topic_df['date-filename1'].dt.to_period('M')

#Converting the 'month' Period to string for categorical x-axis
same_topic_df['month'] = same_topic_df['month'].astype(str)

#Sorting data by month (optional but keeps order clean)
same_topic_df_sorted = same_topic_df.sort_values('month')

#Creating interactive box plot with Plotly Express
fig = px.box(
    same_topic_df_sorted,
    x='month',
    y='similarity',
    color='month',                 # colors per month (optional)
    title='Distribution of Article Similarities (Same Topic) per Month',
    labels={'month': 'Month', 'similarity': 'TF-IDF Similarity'},
    points='all'                  # show all individual similarity points
)

#Improve layout
fig.update_layout(
    xaxis_tickangle=-45,          # rotate x-axis labels for readability
    yaxis=dict(range=[0, 1]),     # setting similarity scores from o to 1
    showlegend=False,           
    template='plotly_white'
)

#Show plot
fig.show()

# Get the directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one level and into the outputs folder
output_dir = os.path.abspath(os.path.join(current_dir, '..', 'outputs'))

# Ensure directory exists
os.makedirs(output_dir, exist_ok=True)

# Define full path to output file
output_file = os.path.join(output_dir, "Distribution of Articles Similarities with Same Topic Per Month.html")

# Save Plotly figure
fig.write_html(output_file)

#Grouping by month and calculate average similarity
monthly_avg_similarity = same_topic_df.groupby('month')['similarity'].mean().reset_index() #tookmhelp from chatgpt, reference: CHAT-1

#Creating an interactive line plot using Plotly
fig = px.line(
    monthly_avg_similarity,
    x='month',
    y='similarity',
    title='Monthly Average TF-IDF Similarity of Same-Topic Article Pairs',
    markers=True,
    labels={'month': 'Month', 'similarity': 'Average Similarity'}
)

#Customize layout (optional)
fig.update_layout(
    xaxis_title='Month',
    yaxis_title='Average Similarity',
    xaxis=dict(tickformat="%b %Y"),
    template='plotly_white'
)

#Show 
fig.show()

# Define full path to output file
output_file2 = os.path.join(output_dir, "Monthly Average TF-idf similarity of  Same Topic Pairs.html")

# Save Plotly figure
fig.write_html(output_file2)










































      




