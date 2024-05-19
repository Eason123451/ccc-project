import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from get_url_data import get_url_data


crime_data = get_url_data(9088, 'search-viccrime-for-twitter')
sentiment_data = get_url_data(9088, 'search-twitter-daily-average-sentiment')


# Call the functions to get the data
df_crime = pd.DataFrame(crime_data)
df_sentiment = pd.DataFrame(sentiment_data)

# Parse 'Date' in sentiment DataFrame
df_sentiment['Date'] = pd.to_datetime(df_sentiment['Date'])

# Convert 'Reported Date per day' to datetime and rename directly
df_crime['Date'] = pd.to_datetime(df_crime['Reported Date per day'])
df_crime.drop('Reported Date per day', axis=1, inplace=True)  # Drop the original date column to avoid confusion
df_crime.rename(columns={'Sum of Offence count': 'Crime_Count'}, inplace=True)

def plot_crime_sentiment_url():
    data_merged = pd.merge(df_sentiment, df_crime, on='Date', how='inner')
    correlation = data_merged['Crime_Count'].corr(data_merged['Sentiment'])
    
    plt.figure(figsize=(10, 6))
    ax = sns.regplot(x='Crime_Count', y='Sentiment', data=data_merged, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    
    # Add a legend with the correlation
    plt.legend(title=f'Correlation: {correlation:.2f}')
    plt.title('Correlation between Crime Reports and Daily Average Sentiment')
    plt.xlabel('Crime Reports')
    plt.ylabel('Average Sentiment')
    plt.grid(True)
    plt.show()
