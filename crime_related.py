import pandas as pd
import json

# Load data
with open('tweets_cleaned.json', 'r') as file:
    data = file.readlines()
    data = [json.loads(line) for line in data]

df = pd.DataFrame(data)

crime_keywords = [
    'crime', 'criminal', 'police', 'arrest', 'suspect', 'law', 'illegal', 'felony', 'misdemeanor', 
    'theft', 'stolen', 'robbery', 'fraud', 'assault', 'murder', 'kidnapping', 'trafficking', 
    'vandalism', 'arson', 'terrorism', 'terrorist', 'rape', 'sexual assault', 'drugs', 'cybercrime', 'hacking',
    'corruption', 'bribery', 'court', 'trial', 'judge', 'lawyer', 'sentence', 'parole'
]

# Filter for crime-related tweets based on the presence of any keyword in the 'Text'
df['is_crime_related'] = df['Text'].apply(lambda x: any(keyword in x.lower() for keyword in crime_keywords))

# Keep only crime-related tweets
crime_related_tweets = df[df['is_crime_related']]

print(crime_related_tweets.head())

# Convert 'Created_At' to datetime and extract the date
crime_related_tweets['Date'] = pd.to_datetime(crime_related_tweets['Created_At']).dt.date

# Group by date and calculate the average sentiment
daily_average_sentiment = crime_related_tweets.groupby('Date')['Sentiment'].mean().reset_index()

print(daily_average_sentiment)

# Convert 'Date' to string for JSON compatibility (if not already in a suitable format)
daily_average_sentiment['Date'] = daily_average_sentiment['Date'].astype(str)

# Export the DataFrame to a JSON file
daily_average_sentiment.to_json('crime_average_sentiment.json', orient='records', lines=True)

