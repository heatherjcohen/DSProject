import pymongo
import tweepy
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

#Connect to MongoDB
client = MongoClient('c621.candidate.15.mongolayer.com', 10621)
client.twitter.authenticate('hjc', 'Iamnumber1')
db = client.twitter

#Double check to make sure connected correctly
db.tweets.count()

db.tweets.find({'fem':1}).count() #neg
#should be the same number in each category
db.tweets.find({'fem':0}).count() #pos/neutral

#grab the hand-coded tweets from twitter along with their valence
neg_tweets = [(doc['text'], doc['fem']) for doc in db.tweets.find({'fem':1})] 
pos_tweets = [(doc['text'], doc['fem']) for doc in db.tweets.find({'fem':0})] 

#Turn into list of words and print them out for interest
pos_tweets_words = []
for words in pos_tweets :
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    pos_tweets_words.append(words_filtered)
print pos_tweets_words

neg_tweets_words = []
for words in pos_tweets :
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    neg_tweets_words.append(words_filtered)
print neg_tweets_words

#Combine into one big list of (["words", "words", "words"], valence)
tweets_words = []
for (words, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in words.split()if len(e) >= 3]
    tweets_words.append((words_filtered, sentiment))
print tweets_words


#NLTK Builder
import nltk
def get_words_in_tweets(tweets_words): 
    all_words = []
    for (words, sentiment) in tweets_words:
      all_words.extend(words)
    return all_words # makes a list of all words

def get_word_features(wordlist): 
    wordlist = nltk.FreqDist(wordlist) #Word count
    word_features = wordlist.keys()
    return word_features

word_features = get_word_features(get_words_in_tweets(tweets_words)) #Calls both functions


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features
    
# create training set
training_set = nltk.classify.apply_features(extract_features, tweets_words)

#train classifier
classifier = nltk.NaiveBayesClassifier.train(training_set)
#show features
classifier.show_most_informative_features()

#test tweet
test_tweet = "i mean people can base their definition of feminism off of what one \"feminist\" says or acts like"
print classifier.classify(extract_features(test_tweet.split()))
