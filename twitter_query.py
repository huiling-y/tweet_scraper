import re
import tweepy
import json
from datetime import datetime
import argparse


def scrape_tweets(screen_name, num=1):

    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''
    
    auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth)
    
    tweets = tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode='extended').items(num)
    
    tweets_list = []
    
    # Process tweets
    for tweet in tweets:
        if 'retweeted_status' in dir(tweet):
            text = f"RT@{tweet.retweeted_status.user.screen_name} {tweet.retweeted_status.full_text}"
        elif tweet.in_reply_to_status_id is not None:
            text = tweet.full_text
        else:
            text = tweet.full_text
            
        tt = tweet.created_at 
        tt = tt.strftime("%I:%M %p, %b %d, %Y")
        
        tweet_piece = f"{tt}: {text}"
        tweets_list.append(tweet_piece)
        
    return tweets_list

def print_tweet(tweets_list):
    for tweet in tweets_list:
        print(tweet)
        print()

def main():
    parser = argparse.ArgumentParser(description="Scrape tweets by user id")
    parser.add_argument('name', help="Id or screen_name of the Twitter account", type=str)
    parser.add_argument("num", help="Number of tweets you wish to scrape", default=1, type=int, nargs="?")
    args = parser.parse_args()

    screen_name = args.name
    num = args.num

    tweets = scrape_tweets(screen_name, num)
    print_tweet(tweets)

if __name__ == '__main__':
    main()