import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
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
    # Merging datasets on 'Date'
    data_merged = pd.merge(df_sentiment, df_crime, on='Date', how='inner')

    # Plotting
    # Calculate Pearson correlation coefficient
    correlation = data_merged['Crime_Count'].corr(data_merged['Sentiment'])

    # Create a scatter plot with a regression line
    plt.figure(figsize=(10, 6))
    sns.regplot(x='Crime_Count', y='Sentiment', data=data_merged, scatter_kws={'alpha':0.5}, line_kws={'color':'red'}, label=f'Correlation: {correlation:.2f}')

    plt.title('Correlation between Crime Reports and Daily Average Sentiment')
    plt.xlabel('Crime Reports')
    plt.ylabel('Average Sentiment')
    plt.grid(True)
    plt.show()

    # Prepare the independent variable (X) and dependent variable (y)
    X = data_merged['Crime_Count']  # Now Crime_Count is the predictor
    X = sm.add_constant(X)  # Adds a constant term to the predictor
    y = data_merged['Sentiment']  # Sentiment is now the response variable

    # Fit the linear regression model
    model = sm.OLS(y, X).fit()

    # Plotting the observed data
    plt.figure(figsize=(10, 6))
    plt.scatter(data_merged['Crime_Count'], data_merged['Sentiment'], color='blue', label='Observed data')

    # Plotting the regression line
    plt.plot(data_merged['Crime_Count'], model.predict(), color='red', label='Fitted line')

    # Adding labels and title
    plt.xlabel('Crime Reports')
    plt.ylabel('Average Sentiment')
    plt.title('Linear Regression Between Crime Reports and Daily Average Sentiment')
    plt.legend()

    # Show the plot
    plt.show()

