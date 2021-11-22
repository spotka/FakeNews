import os
import pandas as pd
import json

import requests
import tweepy


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    api_key = "o100mGNkOOEMek7gijCE2GHRJ"
    api_key_secret = "JFvRMwYGtoFCOTv82sZUAKFRzztmbs3QGTbEikAqfbak7U3QrL"
    bearer_token = "AAAAAAAAAAAAAAAAAAAAABG7VwEAAAAApJmBpGeXG5FoUDmuZE9Pcq%2B%2F4cI%3DT1Bfb0eOm7Q8a9lTaJbYtnNNUiSk2wenmAxsqshGfOC4UJPy18"
    access_token = "1457330111502561283-3gbvaXGuqipTClOaSjWWrmJYwKwgD6"
    access_token_secret = "TdyQpE0d3s80NpGRRtTNTB9l23tEAexNTk5oAiw9T9MIm"

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


if __name__ == "__main__":

    # Twitter API credentials
    api_key = "o100mGNkOOEMek7gijCE2GHRJ"
    api_key_secret =  "JFvRMwYGtoFCOTv82sZUAKFRzztmbs3QGTbEikAqfbak7U3QrL"
    bearer_token = "AAAAAAAAAAAAAAAAAAAAABG7VwEAAAAApJmBpGeXG5FoUDmuZE9Pcq%2B%2F4cI%3DT1Bfb0eOm7Q8a9lTaJbYtnNNUiSk2wenmAxsqshGfOC4UJPy18"
    access_token = "1457330111502561283-3gbvaXGuqipTClOaSjWWrmJYwKwgD6"
    access_token_secret = "TdyQpE0d3s80NpGRRtTNTB9l23tEAexNTk5oAiw9T9MIm"

    # useful ressources
    # https://github.com/twitterdev/Twitter-API-v2-sample-code - API doc with request examples


    # get user data
    # https://tweeterid.com - to get User IDs
    #https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/User-Lookup/get_users_with_bearer_token.py
    usernames = "usernames=SZ,Der_Postillon"
    user_ids = "ids=114508061,105554801"
    # note that the fields (also for tweet fields) have to be comma-seperated, but without empty spaces
    user_fields = "user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"


    url_user_profiles = "https://api.twitter.com/2/users?{}&{}".format(user_ids, user_fields)
    # https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user

    response = requests.request("GET", url_user_profiles, auth=bearer_oauth, )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

    print(json.dumps(response.json(), indent=4, sort_keys=True))

    twitter_result_path = "./TwitterCrawlDirectory/"
    with open(twitter_result_path + 'profile_data_example.json', 'w') as outfile:
        json.dump(response.json(), outfile)


    # get tweet data - see for reference https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/User-Tweet-Timeline/user_tweets.py

    tweet_fields = "tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld"

    user_id = 114508061 # SZ id
    url_tweet = "https://api.twitter.com/2/users/{}/tweets?{}".format(user_id, tweet_fields)
    response_tweet = requests.request("GET", url_tweet, auth=bearer_oauth)
    print(response_tweet.status_code)
    if response_tweet.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response_tweet.status_code, response.text
            )
        )

    twitter_result_path = "./TwitterCrawlDirectory/"
    with open(twitter_result_path + 'profile_sz_tweets_example.json', 'w') as outfile:
        json.dump(response_tweet.json(), outfile)