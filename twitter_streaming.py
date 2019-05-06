import requests
import json
import base64

from twitter_tokens import tokens

class StreamTweets():
    def __init__(self, tokens):
        self.username = None
        self.tweets = []
        self.token_url = tokens.oauthURL
        self.endpoint = tokens.sandboxURL
        self.next_page = None
        
    def get_access_token(self, tokens):
        key_secret = '{}:{}'.format(tokens.CONSUMER_KEY, tokens.CONSUMER_SECRET).encode('ascii')
        b64_encoded_key = base64.b64encode(key_secret)
        b64_encoded_key = b64_encoded_key.decode('ascii')
        
        auth_headers = {'Authorization': 'Basic {}'.format(b64_encoded_key),
                        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
        
        auth_data = {'grant_type': 'client_credentials'}
        
        token_url = self.token_url
        
        auth_resp = requests.post(url=token_url, headers=auth_headers, data=auth_data)
        
        acess_token = auth_resp.json()['access_token']
        
        return acess_token
    
    def get_tweets_from_user(self, username, access_token, starting_page):
        terminate = False
        
        endpoint = self.endpoint
        self.username = username
        self.next_page = starting_page
        batch_number = 1
        max_calls = 15
        
        export_file = open("tweets_" + self.username + ".txt", "a+", encoding='utf-8')        
        
        headers = {"Authorization":"Bearer {}".format(access_token),
                   "Content-Type":"application/json"}
        
        while (not terminate):
            if (batch_number > max_calls):
                terminate = True
                break
            data =  {"query": "from:{}".format(username),
                     "fromDate":"201601010000",
                     "toDate":"201905010000",
                     "maxResults":100,}
            
            if (self.next_page != None):
                data["next"] = self.next_page
            
            print("Grabbing batch -> " + str(batch_number))
            
            search_resp = requests.get(url=endpoint,headers=headers,params=data).json()

            if ('error' in search_resp):
                print(search_resp)
                terminate = True
            else:
                tweet_data = search_resp['results']
                
                if ('next' in search_resp):
                    self.next_page = search_resp['next']
                else:
                    terminate = True
                    
                for tweet in tweet_data:
                    tweet_text = ''
                    if ('extended_tweet' in tweet):
                        tweet_text = tweet['extended_tweet']['full_text']
                    else:
                        tweet_text = tweet['text']
                    self.tweets.append(tweet_text)
                        
                    export_file.write(tweet_text + '\n')
                
                batch_number += 1
                print("Added " + str(len(tweet_data)) + " tweets")
                print("Total of " + str(len(self.tweets)) + " tweets")    
                print("Next value token: '\n'" + self.next_page)
                print("____________________________")
                
        export_file.close()
        
tokens = tokens()
stream_tweets = StreamTweets(tokens=tokens)
def run():
    access_token = stream_tweets.get_access_token(tokens=tokens)
    stream_tweets.get_tweets_from_user(username='realDonaldTrump', access_token=access_token, starting_page=None)