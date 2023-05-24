import yfinance as yf
import pandas as pd
import numpy as np

# Fetch sentiment scores and publication dates from MongoDB
sentiment_data = db['news'].find({}, {'pubDate', 'sentiment_score'})

# Convert to DataFrame and preprocess
sentiment_df = pd.DataFrame(list(sentiment_data))
sentiment_df['pubDate'] = pd.to_datetime(sentiment_df['pubDate'])
sentiment_df.set_index('pubDate', inplace=True)
sentiment_df = sentiment_df.resample('D').mean()

# Fetch stock price data
price_data = yf.download('AAPL', start=sentiment_df.index.min(), end=sentiment_df.index.max())

# Calculate daily returns
price_data['Return'] = price_data['Close'].pct_change()

# Merge sentiment and price data
merged_data = pd.merge(sentiment_df, price_data['Return'], left_index=True, right_index=True)

# Calculate correlation
correlation = merged_data['sentiment_score'].corr(merged_data['Return'])
print(f'Correlation between sentiment score and return: {correlation}')
