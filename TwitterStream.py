from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import MySQLdb

db = MySQLdb.connect("hostname","username","password","database name") #Modify the parameters based on your database 

c = db.cursor()

ckey = '' #Enter your api key
csecret = '' #Enter your api secret key
atoken = '' #Enter your access token
asecret = '' #Enter your access secret

class listener(StreamListener):
    def on_data(self,data):
        try:

            username = data.split(',"name":"')[1].split('","screen_name')[0]
            print username
                        
            tweet = data.split(',"text":"')[1].split('","source')[0]
            print tweet

            tweetTime = str(data.split('{"created_at":"')[1].split('","id')[0])
            print tweetTime

            c.execute('INSERT INTO tweets (time,username,tweet) VALUES (%s,%s,%s)',(tweetTime,username,tweet)) #Create columns named time,username,tweet respectively
            db.commit()
            return True
			
        except BaseException, e:
            print "failed ondata, ",str(e)
            time.sleep(5)

    def on_error(self,status):
        print status

auth = OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
twitterStream = Stream(auth,listener())
twitterStream.filter(track=[""]) #Enter the search term within quotes, based on which you want to filter the tweets
    
