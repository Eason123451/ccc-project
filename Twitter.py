import numpy as np
import pandas as pd
import re

# Importing the dataset
data = pd.read_csv('tweets_cleaned.csv')

# Displaying the first 5 rows of the dataset
print(data.head())

# Average sentiment of the tweets
data['Sentiment'].mean()

print(data['Sentiment'].mean())

# Number of rows in the dataset
print(data.shape[0])

