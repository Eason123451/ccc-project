from get_elastic import get_data
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json

# Specify your parameters
port = 'https://localhost:9210'
index_name = 'daily_average_sentiment'
scroll_size = 1000
scroll_time = '2m'

# Now you can call the function with specified parameters
requested_data = get_data(port, index_name, scroll_size, scroll_time)

# Load the json data into a pandas dataframe
data_list = json.loads(requested_data)
daily_sentiment = pd.DataFrame(data_list)

# Convert the 'Date' column to datetime format
daily_sentiment['Date'] = pd.to_datetime(daily_sentiment['Date'])

# Group by date and calculate the average sentiment
average_daily_sentiment = daily_sentiment.groupby('Date')['Sentiment'].mean().reset_index()

# # Plot the average sentiment over time
# plt.figure(figsize=(10, 6))
# plt.plot(average_daily_sentiment['Date'], average_daily_sentiment['Sentiment'], marker='o')
# plt.xlabel('Date')
# plt.ylabel('Average Sentiment')
# plt.title('Average Sentiment Over Time')
# plt.grid(True)

# # Format the date on the x-axis
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
# plt.gcf().autofmt_xdate()

# plt.show()

def plot_average_sentiment_over_time():
    # Plot the average sentiment over time
    plt.figure(figsize=(10, 6))
    plt.plot(average_daily_sentiment['Date'], average_daily_sentiment['Sentiment'], marker='o')
    plt.xlabel('Date')
    plt.ylabel('Average Sentiment')
    plt.title('Average Sentiment Over Time')
    plt.grid(True)
    # Format the date on the x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
    plt.gcf().autofmt_xdate()
    plt.show()