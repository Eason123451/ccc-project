# Project Documentation for Twitter Sentiment Analysis

## Required Packages
- **pandas**
- **matplotlib**
- **seaborn**
- **numpy**
- **scipy**
- **ipython**
- **requests**
- **unittest**
  

## Data Preparation

### Tweets Data Files
- **tweets_100Gb_filtered.csv**: Due to the large size of the file, we are only interested in tweets with `tag` element contains `"Australia-based"`. Extracted fields `"created_at"`, `"sentiment"`, and `"text"` on SPARTAN using scripts:
  - `filter_data.py`
  - `filter.slurm`
- **tweets_cleaned.csv**: Cleaned to remove zero sentiments and emojis. (For reducing the file size)
For a purpose of time and space efficieny on the `elastic-search` database, in terms of storage and transmission, we pre-processed our dataset locally. 
- **daily_average_sentiment.json**: Calculated the average sentiment for each day.
- **daily_tweets.json**: Total number of tweets for each day.
- **busiest_day_data_sample**: Randomly sampled 6,000 tweets out of approximately 180,000 tweets on the busiest day(has the most tweets).
- **quietest_day_data**: With around 5,060 tweets on the quietest day(has the fewest tweets).
- **viccrime_twitter.json**: Containing the number of crime cases reported for the selected dates(allign with the dates we are interested)

## Analysis Scenarios

### Scenario 1: Daily Sentiment and Tweet Volume Analysis

![Scenario 1](/output_images/Scenario_1.png)

#### Overview
This analysis presents the relationship between daily tweet volumes and average sentiment scores over a period from June 21, 2021, to July 31, 2021.

#### Graph Features
- **Red Line**: Represents daily average sentiment.
- **Blue Line**: Represents total tweets per day.
- **Axes**: The graph uses dual y-axes to display average sentiment (left) and tweet volume (right), with time on the x-axis.

#### Insights
- **Inverse Relationship**: Peaks in tweet volume often coincide with drops in sentiment, suggesting that events triggering increased tweeting may evoke stronger emotional responses.
- **Event Impact**: Sharp changes in the graph may align with specific events, indicating public reaction intensity and engagement levels.

#### Conclusion
The dual tracking of sentiment and tweet volume offers insights into public mood and engagement, useful for understanding reactions to events and guiding strategic responses.

#### The Busiest and The Quietest Day
We found that the busiest day is corresponding with the lowest average sentiment, and the quietest day is corresponding with the highest average sentiment. So we pick these two days to be further investigated.

### Scenario 2: Sentiment Distribution on Busiest and Quietest Days

![Scenario 2](/output_images/Scenario_2.png)

#### Overview
This analysis compares the distribution of sentiment scores on the busiest and quietest days, visualized through histograms and normal distribution fits.

#### Graph Description
- **Histograms**: Show the frequency of sentiment scores on the busiest (maroon bars) and quietest (teal bars) days.
- **Normal Distribution Curves**:
  - Red line for the busiest day.
  - Blue line for the quietest day.

#### Key Features of the Graph
- **X-axis**: Sentiment scores ranging from -0.8 to 0.4.
- **Y-axis**: Density of the scores, indicating the probability distribution.
- **Comparison**: The curves and histograms allow for a visual comparison of sentiment trends between the two types of days.

#### Insights
- **Distribution Shape**: Both days exhibit roughly normal distributions, but the quietest shows a slightly more positive skew compared to the busiest day.
- **Sentiment Variability**: The busiest days tend to have a broader spread of sentiment scores, suggesting more varied reactions among tweets compared to quieter days.

#### Conclusion
This visual comparison highlights how public sentiment varies between days with high and low Twitter activity, potentially reflecting different public moods or events triggering these tweets.


### Scenario 3: Correlation between Crime Reports and Sentiment

![Scenario 3](/output_images/Scenario_3.png)

#### Overview
This analysis explores the correlation between daily crime reports and average sentiment scores from tweets.

#### Graph Description
The plot displays daily crime reports against average sentiment with a Pearson correlation coefficient of 0.33, indicating a moderate positive correlation.

#### Key Features of the Graph
- **Red Line**: Represents the regression line, illustrating the trend in the data.
- **Shaded Area**: Shows the 95% confidence interval around the regression line.

#### Insights
- **Correlation Interpretation**: The positive correlation suggests that higher crime reports might be associated with days of slightly more positive sentiment, possibly reflecting increased public awareness and engagement.

#### Conclusion
Understanding this correlation helps in assessing how public sentiment on social media corresponds with crime dynamics, potentially aiding in community-focused strategies and public safety measures.

### Scenario 4: Sampling Crime-Related Tweets

![Busiest Day](/output_images/Scenario_4_1.png)

![Quietest Day](/output_images/Scenario_4_2.png)

#### Overview
This scenario demonstrates the functionality of dynamically sampling and displaying five tweets related to crime from the busiest and quietest days. This is achieved through specific Python functions.

#### Functionality
- **`sample_crime_busiest_tweets()`**: When this function is called, it randomly selects five crime-related tweets from the busiest day, displaying each tweet's sentiment score and text.
- **`sample_crime_quietest_tweets()`**: This function works similarly but selects tweets from the quietest day.

#### Display Format
Each function outputs:
- **Sentiment**: The sentiment score of the tweet, indicating the emotional tone (positive, neutral, or negative).
- **Text**: The actual text of the tweet, providing context to the sentiment score.

#### Usage
These functions are particularly useful for analyzing variations in public sentiment towards crime on different types of days. They can help in understanding how public reactions vary with the intensity of social media activity.

#### Purpose
The sampled tweets provide insights into public opinion and sentiment trends related to crime, serving as a tool for qualitative analysis alongside quantitative measures.

#### Conclusion
By executing these functions, users can quickly gather examples of public sentiment on crime-related issues from specific days, which is invaluable for research, reporting, or further analysis in social science and digital humanities.


# Testing Documentation

## Unit Tests for Data Fetching

### Objective
Verify that `get_url_data` function correctly fetches data from the API.

### Test Cases
- **Success Test**: Provide a valid port and endpoint; expect the function to return data without errors.
- **Failure Test**: Provide an invalid port or endpoint; expect the function to handle errors gracefully, possibly by returning `None` or raising an informative exception.

## Integration Tests for Data Processing Functions