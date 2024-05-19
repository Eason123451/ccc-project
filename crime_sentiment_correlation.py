from get_viccrime_tweet import get_viccrime_twitter
from get_average_sentiment import get_average_sentiment
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm


# Call the functions to get the data
df_crime = get_viccrime_twitter()
df_sentiment = get_average_sentiment()

# Print columns to inspect the structure
print("Sentiment DataFrame Columns:", df_sentiment.columns)
print("Crime DataFrame Columns:", df_crime.columns)

# Parse 'Date' in sentiment DataFrame
df_sentiment['Date'] = pd.to_datetime(df_sentiment['Date'])

# Ensure there's no duplicate 'Date' column in crime DataFrame
if 'Date' in df_crime.columns:
    df_crime.drop('Date', axis=1, inplace=True)

# Convert 'Reported Date per day' to datetime and rename directly
df_crime['Date'] = pd.to_datetime(df_crime['Reported Date per day'])
df_crime.drop('Reported Date per day', axis=1, inplace=True)  # Drop the original date column to avoid confusion
df_crime.rename(columns={'Sum of Offence count': 'Crime_Count'}, inplace=True)

# Check if 'Date' columns exist and are unique after renaming
print("New Sentiment DataFrame Columns:", df_sentiment.columns)
print("New Crime DataFrame Columns:", df_crime.columns)

# Merging datasets on 'Date'
data_merged = pd.merge(df_sentiment, df_crime, on='Date', how='inner')

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Average Sentiment', color=color)
ax1.plot(data_merged['Date'], data_merged['Sentiment'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Crime Reports', color=color)
ax2.plot(data_merged['Date'], data_merged['Crime_Count'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # to ensure the layout doesn't overlap
plt.title('Daily Average Sentiment vs. Crime Reports')
plt.show()

# Calculate Pearson correlation coefficient
correlation = data_merged['Sentiment'].corr(data_merged['Crime_Count'])
print(f"Pearson correlation coefficient: {correlation}")

# Create a scatter plot with a regression line
plt.figure(figsize=(10, 6))
sns.regplot(x='Sentiment', y='Crime_Count', data=data_merged, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})

plt.title('Correlation between Daily Average Sentiment and Crime Reports')
plt.xlabel('Average Sentiment')
plt.ylabel('Crime Reports')
plt.grid(True)
plt.show()

# Prepare the independent variable (X) and dependent variable (y)
X = data_merged['Crime_Count']  # Now Crime_Count is the predictor
X = sm.add_constant(X)  # Adds a constant term to the predictor
y = data_merged['Sentiment']  # Sentiment is now the response variable

# Fit the linear regression model
model = sm.OLS(y, X).fit()

# Print out the statistics
print(model.summary())

# Plotting the observed data
plt.figure(figsize=(10, 6))
plt.scatter(data_merged['Crime_Count'], data_merged['Sentiment'], color='blue', label='Observed data')

# Plotting the regression line
plt.plot(data_merged['Crime_Count'], model.predict(), color='red', label='Fitted line')

# Adding labels and title
plt.xlabel('Crime Reports')
plt.ylabel('Average Sentiment')
plt.title('Linear Regression Analysis')
plt.legend()

# Show the plot
plt.show()