import nltk
import textblob
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

# Download necessary NLTK resources
nltk.download('vader_lexicon')
nltk.download('punkt')

class SentimentAnalyzer:
    def __init__(self):
        # Initialize NLTK's Sentiment Intensity Analyzer
        self.nltk_analyzer = SentimentIntensityAnalyzer()
    
    def analyze_sentiment_nltk(self, text):
        """
        Analyze sentiment using NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner)
        Returns a detailed sentiment score and classification
        """
        # Get sentiment scores
        sentiment_scores = self.nltk_analyzer.polarity_scores(text)
        
        # Classify sentiment
        if sentiment_scores['compound'] >= 0.05:
            sentiment = 'Positive'
        elif sentiment_scores['compound'] <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return {
            'text': text,
            'nltk_scores': sentiment_scores,
            'nltk_sentiment': sentiment
        }
    
    def analyze_sentiment_textblob(self, text):
        """
        Analyze sentiment using TextBlob
        Returns polarity and subjectivity scores
        """
        # Create TextBlob object
        blob = TextBlob(text)
        
        # Determine sentiment classification
        if blob.sentiment.polarity > 0:
            sentiment = 'Positive'
        elif blob.sentiment.polarity < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return {
            'text': text,
            'textblob_polarity': blob.sentiment.polarity,
            'textblob_subjectivity': blob.sentiment.subjectivity,
            'textblob_sentiment': sentiment
        }
    
    def batch_sentiment_analysis(self, texts):
        """
        Perform sentiment analysis on a batch of texts
        Returns a DataFrame with results from both methods
        """
        results = []
        
        for text in texts:
            nltk_result = self.analyze_sentiment_nltk(text)
            textblob_result = self.analyze_sentiment_textblob(text)
            
            # Combine results
            combined_result = {
                **nltk_result,
                **textblob_result
            }
            results.append(combined_result)
        
        return pd.DataFrame(results)
    
    def visualize_sentiment_distribution(self, df):
        """
        Create visualizations of sentiment distribution
        """
        # NLTK Sentiment Distribution
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        df['nltk_sentiment'].value_counts().plot(kind='bar')
        plt.title('NLTK Sentiment Distribution')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        
        # TextBlob Sentiment Distribution
        plt.subplot(1, 2, 2)
        df['textblob_sentiment'].value_counts().plot(kind='bar')
        plt.title('TextBlob Sentiment Distribution')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        
        plt.tight_layout()
        plt.show()

def main():
    # Sample texts for sentiment analysis
    sample_texts = [
        "You can do it",
        "This is the worst experience I've ever had. Terrible service!",
        "This is the best day of my life!",
        "I always overthink about what others think about me and it upsets me",
        "I'm really impressed with the quality and customer support.",
        "Disappointed with the recent changes. Not what I expected at all.",
        "I am confident,brave,smartand beautiful",
        "I really wished that there was no viva to be conducted today!"
    ]
    
    # Create sentiment analyzer
    analyzer = SentimentAnalyzer()
    
    # Perform batch sentiment analysis
    results_df = analyzer.batch_sentiment_analysis(sample_texts)
    
    # Print detailed results
    print("Sentiment Analysis Results:")
    print(results_df)
    
    # Visualize sentiment distribution
    analyzer.visualize_sentiment_distribution(results_df)

if __name__ == "__main__":
    main()