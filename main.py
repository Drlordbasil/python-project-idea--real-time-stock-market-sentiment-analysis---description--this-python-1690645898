import requests
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.sentiment import SentimentIntensityAnalyzer


class StockMarketAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.stock_api_url = "https://api.example.com/stocks"
        self.social_media_api_url = "https://api.example.com/social-media"
        self.news_article_api_url = "https://api.example.com/news-articles"

    def collect_real_time_data(self):
        stock_data = self.get_stock_data()
        social_media_data = self.get_social_media_data()
        news_article_data = self.get_news_article_data()

        return stock_data, social_media_data, news_article_data

    def get_stock_data(self):
        response = requests.get(self.stock_api_url, params={
                                "apiKey": self.api_key})
        stock_data = response.json()
        return stock_data

    def get_social_media_data(self):
        response = requests.get(self.social_media_api_url, params={
                                "apiKey": self.api_key})
        social_media_data = response.json()
        return social_media_data

    def get_news_article_data(self):
        response = requests.get(self.news_article_api_url, params={
                                "apiKey": self.api_key})
        news_article_data = response.json()
        return news_article_data

    def preprocess_text_data(self, text_data):
        preprocessed_data = []
        for text in text_data:
            processed_text = self.preprocess_text(text)
            preprocessed_data.append(processed_text)
        return preprocessed_data

    def preprocess_text(self, text):
        processed_text = text.lower()
        processed_text = nltk.word_tokenize(processed_text)
        processed_text = [word for word in processed_text if word.isalpha()]
        return processed_text

    def analyze_sentiment(self, text_data):
        sentiment_scores = []
        sid = SentimentIntensityAnalyzer()
        for text in text_data:
            sentiment_score = sid.polarity_scores(text)["compound"]
            sentiment_scores.append(sentiment_score)
        return sentiment_scores

    def generate_sentiment_distribution_chart(self, sentiment_scores):
        plt.hist(sentiment_scores, bins='auto')
        plt.xlabel('Sentiment Score')
        plt.ylabel('Frequency')
        plt.title('Sentiment Distribution')
        plt.show()

    def generate_word_cloud(self, text_data):
        wordcloud = WordCloud().generate(' '.join(text_data))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    def analyze_sentiment_of_stocks(self, sentiment_scores):
        stock_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        return stock_sentiment

    def display_results(self, stock_sentiment):
        print(f"Stock Sentiment: {stock_sentiment:.2f}")

    @classmethod
    def run_analysis(cls):
        api_key = input("Enter your API key: ")
        stock_market_analyzer = cls(api_key)
        stock_data, social_media_data, news_article_data = stock_market_analyzer.collect_real_time_data()
        preprocessed_data = stock_market_analyzer.preprocess_text_data(
            social_media_data + news_article_data)
        sentiment_scores = stock_market_analyzer.analyze_sentiment(
            preprocessed_data)
        stock_sentiment = stock_market_analyzer.analyze_sentiment_of_stocks(
            sentiment_scores)
        stock_market_analyzer.generate_sentiment_distribution_chart(
            sentiment_scores)
        stock_market_analyzer.generate_word_cloud(preprocessed_data)
        stock_market_analyzer.display_results(stock_sentiment)


if __name__ == '__main__':
    StockMarketAnalyzer.run_analysis()
