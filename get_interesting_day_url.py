import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from get_url_data import get_url_data
import numpy as np
from scipy.stats import norm
from IPython.display import display, HTML


# Get data from each endpoint
busiest_day_data = get_url_data(9088, 'search-twitter-busiestday')
quiest_day_data = get_url_data(9088, 'search-twitter-quietestday')

# Load the json data into pandas dataframes
df_busiest_day = pd.DataFrame(busiest_day_data)
df_quietest_day = pd.DataFrame(quiest_day_data)

df_busiest_day = df_busiest_day.sample(n=5060, random_state=1)

def plot_sentiment_distribution():
    # Set up the matplotlib figure
    plt.figure(figsize=(10, 6))

    # Plot histograms
    sns.histplot(df_busiest_day['Sentiment'], color="teal", label='Busiest Day', kde=False, alpha=0.6, stat="density", bins=20)
    sns.histplot(df_quietest_day['Sentiment'], color="maroon", label='Quietest Day', kde=False, alpha=0.6, stat="density", bins=20)

    # Calculate the parameters for the normal distribution curve
    mean_buiest = df_busiest_day['Sentiment'].mean()
    std_buiest = df_busiest_day['Sentiment'].std()
    mean_quiest = df_quietest_day['Sentiment'].mean()
    std_quiest = df_quietest_day['Sentiment'].std()

    # Generate points on the x axis
    x_points = np.linspace(min(df_busiest_day['Sentiment'].min(), df_quietest_day['Sentiment'].min()), max(df_busiest_day['Sentiment'].max(), df_quietest_day['Sentiment'].max()), 100)

    # Plot normal distribution curve
    plt.plot(x_points, norm.pdf(x_points, mean_buiest, std_buiest), color='darkred', label='Normal Dist - Busiest Day')
    plt.plot(x_points, norm.pdf(x_points, mean_quiest, std_quiest), color='darkblue', label='Normal Dist - Quietest Day')

    # Add labels and title
    plt.xlabel('Sentiment Score')
    plt.ylabel('Density')
    plt.title('Distribution of Sentiments on Busiest and Quietest Days')
    plt.legend()

    # Show the plot
    plt.show()

# Filter for crime-related tweets
def filter_crime_related_tweets(df):
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

    return crime_related_tweets

# Apply the filter to both day datasets
df_quietest_day = filter_crime_related_tweets(df_quietest_day)
df_busiest_day = filter_crime_related_tweets(df_busiest_day)

pd.set_option('display.max_colwidth', None)

# Print 5 sample tweets of quietest day related to crime
def sample_crime_quietest_tweets():
    sample_tweets = df_quietest_day.sample(n=5, random_state =  None) 
    sample_tweets['Sentiment'] = sample_tweets['Sentiment'].round(3)
    
    # Drop the 'is_crime_related' column to avoid redundancy
    sample_tweets.drop('is_crime_related', axis=1, inplace=True)

    # Convert DataFrame to HTML
    html = sample_tweets.to_html(index=False, escape=False)

    # Display the HTML with custom CSS for auto-adjusting row heights
    display(HTML(f'''
    <style>
        table, th, td {{
            border: 1px solid black;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            vertical-align: top;
        }}
        td {{
            max-width: 500px;  /* Adjust the width of the cells */
            word-wrap: break-word;  /* Ensures that words wrap and text does not overflow */
        }}
    </style>
    {html}
    '''))

def sample_crime_busiest_tweets():
    sample_tweets = df_busiest_day.sample(n=5, random_state=None)  # Ensure random sampling
    sample_tweets['Sentiment'] = sample_tweets['Sentiment'].round(3)

    # Drop the 'is_crime_related' column to avoid redundancy
    sample_tweets.drop('is_crime_related', axis=1, inplace=True)

    # Convert DataFrame to HTML
    html = sample_tweets.to_html(index=False, escape=False)

    # Display the HTML with custom CSS for auto-adjusting row heights
    display(HTML(f'''
    <style>
        table, th, td {{
            border: 1px solid black;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            vertical-align: top;
        }}
        td {{
            max-width: 500px;  /* Adjust the width of the cells */
            word-wrap: break-word;  /* Ensures that words wrap and text does not overflow */
        }}
    </style>
    {html}
    '''))