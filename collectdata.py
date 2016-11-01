# -*- coding: utf-8 -*-

import tweepy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


pd.set_option('display.mpl_style', 'default')

consumer_key = "###"
consumer_secret = "##"
access_token = "##"
access_token_secret = "##"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)








results = []

#Get the first 5000 items based on the search query
for tweet in tweepy.Cursor(api.search, q='usps', lang='en', since='2015-11-22', until='2015-12-03').items(6000):
    results.append(tweet)

print 'number of tweet: ' + str(len(results))


# Create a function to convert a given list of tweets into a Pandas DataFrame.
# The DataFrame will consist of only the values, which I think might be useful for analysis...

def toMentions(tweets):
    Mentions = []    
    for tweet in tweets:
        mention = str()
        for i, person in enumerate(tweet.entities['user_mentions']):
            if i != 0:
                mention = mention + '|' + person['screen_name']
            else:
                mention = person['screen_name']
        Mentions.append(mention)
               
    return Mentions

Mention = toMentions(results)


def toDataFrame(tweets):

    DataSet = pd.DataFrame()

    DataSet['tweetText'] = [tweet.text for tweet in tweets]
    DataSet['tweetRetweetCt'] = [tweet.retweet_count for tweet in tweets]
    DataSet['tweetFavoriteCt'] = [tweet.favorite_count for tweet in tweets]
    DataSet['tweetSource'] = [tweet.source for tweet in tweets]
    DataSet['tweetCreated'] = [tweet.created_at for tweet in tweets]
    DataSet['tweetLanguage'] = [tweet.lang for tweet in tweets]


    DataSet['userScreen'] = [tweet.user.screen_name for tweet in tweets]
    DataSet['userName'] = [tweet.user.name for tweet in tweets]
    DataSet['userFollowerCt'] = [tweet.user.followers_count for tweet in tweets]
    DataSet['userFriendsCt'] = [tweet.user.friends_count for tweet in tweets]
    DataSet['userLocation'] = [tweet.user.location for tweet in tweets]
    DataSet['userTimezone'] = [tweet.user.time_zone for tweet in tweets]
    
    
    DataSet['userMentions'] = Mention
    
    return DataSet
    
#Pass the tweets list to the above function to create a DataFrame
DataSet = toDataFrame(results)

# remove all the records whoes language is not English
DataSet = DataSet[DataSet.userTimezone.notnull()]
DataSet = DataSet[DataSet.userLocation != '']

    

DataSet.to_csv('allReviews.csv', encoding='utf-8')




