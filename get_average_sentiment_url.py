import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_data(port):
    fission_url = f"http://localhost:{port}/search-twitter-daily-average-sentiment"
    response = requests.get(fission_url,verify=False)
    return response.json()


def plot_average_sentiment_url():
    requested_data = get_data(9088)

    # Load the json data into a pandas dataframe
    daily_sentiment = pd.DataFrame(requested_data)

    # Convert the 'Date' column to datetime format
    daily_sentiment['Date'] = pd.to_datetime(daily_sentiment['Date'])

    # Plot the average sentiment over time
    plt.figure(figsize=(10, 6))
    plt.plot(daily_sentiment['Date'], daily_sentiment['Sentiment'], marker='o')
    plt.xlabel('Date')
    plt.ylabel('Average Sentiment')
    plt.title('Average Sentiment Over Time')
    plt.grid(True)

    # Format the date on the x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
    plt.gcf().autofmt_xdate()  # Rotate date labels for better readability
    plt.show()

