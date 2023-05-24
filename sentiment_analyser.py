from textblob import TextBlob

# Fetch news data from MongoDB
news_data = db['news'].find()

# Perform sentiment analysis and store sentiment scores in MongoDB
for news in news_data:
    analysis = TextBlob(news['description'])
    sentiment_score = analysis.sentiment.polarity
    db['news'].update_one({'_id': news['_id']}, {'$set': {'sentiment_score': sentiment_score}})
