import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from get_url_data import get_url_data

def plot_combined_sentiment_and_tweets(port):
    # Get data from each endpoint
    sentiment_data = get_url_data(port, 'search-twitter-daily-average-sentiment')
    tweet_data = get_url_data(port, 'search-twitter-daily-tweets')

    # Load the json data into pandas dataframes
    df_sentiment = pd.DataFrame(sentiment_data)
    df_tweets = pd.DataFrame(tweet_data)

    # Convert 'Date' from UNIX timestamp (milliseconds) to datetime for tweets dataframe
    df_tweets['Date'] = pd.to_datetime(df_tweets['Date'], unit='ms')
    # Convert 'Date' to datetime for sentiment dataframe
    df_sentiment['Date'] = pd.to_datetime(df_sentiment['Date'])

    # Merge dataframes on 'Date'
    data_merged = pd.merge(df_sentiment, df_tweets, on='Date', how='inner')

    # Plotting
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot average sentiment over time
    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Average Sentiment', color=color)
    ax1.plot(data_merged['Date'], data_merged['Sentiment'], marker='o', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a second y-axis for total tweets
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Total Tweets', color=color)
    ax2.plot(data_merged['Date'], data_merged['Number of Tweets'], marker='o', linestyle='--', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Formatting the x-axis for dates
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    fig.autofmt_xdate()  # Rotate date labels for better readability

    plt.title('Daily Average Sentiment and Total Tweets Over Time')
    plt.grid(True)
    plt.show()
