import tweepy
import pandas as pd
import textblob
import preprocessor.api as p
import statistics
from typing import List
from preprocessor.api import clean, tokenize, parse


consumer_key= ''
consumer_secret= ''
access_token= ''
access_token_secret= ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


def get_tweets(keyword:str) -> List[str]:
    all_tweets = []
    for tweet in tweepy.Cursor(api.search, q=keyword, tweet_mode = "extended", lang="en").items(10):
        #print(tweet)
        all_tweets.append(tweet.full_text)
    return all_tweets


def clean_tweets(all_tweets: List[str]) -> List[str]:
    tweets_clean = []
    for iteration in all_tweets:
        #print(iteration)
        tweets_clean.append(p.clean(iteration))
    return tweets_clean


def get_sentiments(tweets_clean: List[str])-> List[float]:
    sentiment_scores = []
    for iteration_sentiment in tweets_clean:
        blob = textblob.TextBlob(iteration_sentiment)
        #print(blob)
        sentiment_scores.append(blob.sentiment.polarity)
    return sentiment_scores


def generate_average_sentiment_score(keyword: str)-> int:
    tweets = get_tweets(keyword)
    tweets_clean = clean_tweets(tweets)
    sentiment_scores = get_sentiments(tweets_clean)
    average_score = statistics.mean(sentiment_scores)
    return average_score

#MAIN
print('What does the world prefer?')
first_input = input()
print('....or....')
second_input = input()
print('\n')
first_score = generate_average_sentiment_score(first_input)
second_score = generate_average_sentiment_score(second_input)
if first_score > second_score:
    print('The humanity prefers {} over {}'.format(first_input, second_input))
else:
    print('The humanity prefers {} over {}'.format(second_input, first_input))
