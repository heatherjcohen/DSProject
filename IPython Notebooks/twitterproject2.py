from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pymongo
import tweepy
import json

#Variables that contains the user credentials to access Twitter API 
access_key = '2981595259-rNdQQ3gkigeDoKkcfNAOBOz99jQcJsh379fsSC1'
access_secret = 'sp0mR0a0UPbB04Lart0eVt8Eh57II7gCIpcFecwQH9qGo'
consumer_key = 'UcUk7YemRsZolPKpG5WX2RGZy'
consumer_secret = '4CU9UAcudTIVD405h4HAICPiLXAT2XzXKdOtdZzppKM09cfAuU'

#Runs auth to Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


#This is a basic listener that will print incoming data to stdout
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


#Customizes the stream and saves text and lang to databases 
class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        self.db = pymongo.MongoClient('c621.candidate.15.mongolayer.com', 10621).twitter
    
    
    def on_data(self, data):
        jd = json.loads(data)
        if jd.has_key('text'):
            self.db.tweets.insert(str(jd['text'])).encode('ascii','ignore')
            self.db.langs.insert(jd['lang'])
               

    def on_error(self, status_code):
        return True # Don't kill the stream

    def on_timeout(self):
        return True # Don't kill the stream

#Calls on StreamListerner and provides specifications of tracking
l = tweepy.streaming.Stream(auth, CustomStreamListener(api))
<<<<<<< HEAD
l.filter(track=['feminism', 'feminist'], languages =['en'])
=======
l.filter(track=['feminism', 'feminist'], languages =['en'])
>>>>>>> be606a9086c89a0ce30d08474a39171963884b80
