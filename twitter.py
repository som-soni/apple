import requests
from requests.auth import HTTPBasicAuth
import json

TWIITER_API = 'https://api.twitter.com'
CONSUMER_KEY = 'Nblj0MJTmnVpWxfQcfcGogs9E'
CONSUMER_SECRET = 'XrlTAjMku85Wz4uw0IDxw0DSIUGkrdgfK1MwBClIXRRIuQLmU9'
MAX_TWEETS_PER_PAGE = 100

def __get_access_token():
    headers = {'Content-Type' : 'application/x-www-form-urlencoded;charset=UTF-8'}
    data = {'grant_type' :'client_credentials'}
    resp = requests.post('{0}/oauth2/token'.format(TWIITER_API),auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET),headers=headers,data=data)
    access_token = resp.json()['access_token']
    return access_token

def __get_tweets(access_token,query,count,search_url=None):
    twitter_search_url = '{0}/1.1/search/tweets.json'.format(TWIITER_API)
    if search_url:
        twitter_search_url += search_url
    else:
        params = {'q':query,'count':count}
    headers = {'Authorization': 'Bearer ' + access_token}
    tweets = requests.get(twitter_search_url,headers=headers,params=params)
    return tweets.json()

def __get_tweets_top_n(access_token,query,top_n):
    tweets = []
    if top_n > MAX_TWEETS_PER_PAGE:
        search_url = None
        while len(tweets) < top_n:
            next_tweets_response = __get_tweets(access_token,query,MAX_TWEETS_PER_PAGE,search_url)
            search_metadata = next_tweets_response.get('search_metadata')
            next_tweets = next_tweets_response['statuses']
            for tweet in next_tweets:
                if len(tweets) >= top_n:
                    break
                else:
                    tweets.append(tweet)
                if 'next_results' not in search_metadata:
                    break
        return tweets
    else:
        response = __get_tweets(access_token,query,top_n)
        tweets = response['statuses']

    return tweets

if __name__ == '__main__':
    input_query = input("Enter search query : ") 
    top_n = int(input("Enter Top N : "))
    access_token = None

    try:
        access_token = __get_access_token()
    except Exception:
        print('Error generating access token. Please verify consumer credentials')
    
    if access_token:
        try:
            tweets = __get_tweets_top_n(access_token,input_query,top_n)
            count = 0
            for tweet in tweets:
                print('tweet id : {0} , tweet text : {1}'.format(tweet['id'],tweet['text']))
        except Exception as e:
            print('Error fetching tweets from twitter')
