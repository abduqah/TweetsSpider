import tweepy
import json
from time import sleep

# Consumer keys and access tokens, used for OAuth
consumer_key = 'WxEstdKl7ddTImNEUrMLIN0vX'
consumer_secret = 's2Q7vtBi2NCD8Zbg6kduU9smsd1OiSGvmQvLfJ1RT2A6ilOhen'
access_token = '847679801850699778-9hc8jJa1rXGvLZ3IAN4gqjiN1eUEZkS'
access_token_secret = 'GSR7JQtEEECdhi4TYN4rOjUGf4emx6Z0hEvMxdDvA90vY'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)
maxtweets = 10000

# Getting Geo ID for USA
places = api.geo_search(query="USA", granularity="country")
searchQuery = "place:%s" % places[0].id

while(maxtweets >= 0):
    try:
        if (not api):
            print("Problem Connecting to API")
            exit(1)


        with open('raw_data','a') as raw_data:
            for tweet in tweepy.Cursor(api.search, q = searchQuery, result_type="recent").items():

                # Verify the tweet has place info before writing (It should, if it got past our place filter)
                if tweet.place is not None:

                    # Write the JSON format to the text file, and add one to the number of tweets we've collected
                    raw_data.write(json.dumps(tweet._json) + '\n\n')
                    maxtweets -= 1

                    # Display how many tweets we have collected
            print("Downloaded {0} tweets".format(10000 - maxtweets))

    except:
        print('waiting')
        sleep(450)
print('\n\nFINISHED!!!')