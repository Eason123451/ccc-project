import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_url_data(port):
    fission_url = f"http://localhost:{port}/search-twitter-daily-tweets"
    response = requests.get(fission_url,verify=False)
    return response.json()

def plot_total_tweets_over_time_url():
    requested_data = get_url_data(9088)

    # Load the json data into a pandas dataframe
    daily_tweets = pd.DataFrame(requested_data)

    # Convert 'Date' from UNIX timestamp (milliseconds) to datetime
    daily_tweets['Date'] = pd.to_datetime(daily_tweets['Date'], unit='ms')

    # Plotting function
    plt.figure(figsize=(10, 6))
    plt.plot(daily_tweets['Date'], daily_tweets['Number of Tweets'], marker='o')
    plt.xlabel('Date')
    plt.ylabel('Total Tweets')
    plt.title('Daily Total Tweets Over Time')
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
    plt.gcf().autofmt_xdate()  # Rotate date labels for better readability
    plt.show()

