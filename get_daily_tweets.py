from get_elastic import get_data
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json

# Specify your parameters
port = 'https://localhost:9210'
index_name = 'daily_tweets'
scroll_size = 1000
scroll_time = '2m'

# Now you can call the function with specified parameters
requested_data = get_data(port, index_name, scroll_size, scroll_time)

# Load the json data into a pandas dataframe
data_list = json.loads(requested_data)
daily_tweets = pd.DataFrame(data_list)

# Convert 'Date' from UNIX timestamp (milliseconds) to datetime
daily_tweets['Date'] = pd.to_datetime(daily_tweets['Date'], unit='ms')

# Plotting function
def plot_total_tweets_over_time():
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
