import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Initialize MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['market_news_db']

# Fetch Yahoo Finance RSS feed
url = 'https://finance.yahoo.com/news/rssindex/'
response = requests.get(url)
soup = BeautifulSoup(response.content, features='xml')

# Extract and store news data in MongoDB
for item in soup.findAll('item'):
    news = {
        'title': item.title.text,
        'description': item.description.text,
        'link': item.link.text,
        'pubDate': item.pubDate.text
    }
    db['news'].insert_one(news)
