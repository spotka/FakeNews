import os
import pandas as pd
import json

import requests
import tweepy


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    # Twitter API credentials
    api_key = "o100mGNkOOEMek7gijCE2GHRJ"
    api_key_secret = "JFvRMwYGtoFCOTv82sZUAKFRzztmbs3QGTbEikAqfbak7U3QrL"
    bearer_token = "AAAAAAAAAAAAAAAAAAAAABG7VwEAAAAApJmBpGeXG5FoUDmuZE9Pcq%2B%2F4cI%3DT1Bfb0eOm7Q8a9lTaJbYtnNNUiSk2wenmAxsqshGfOC4UJPy18"
    access_token = "1457330111502561283-3gbvaXGuqipTClOaSjWWrmJYwKwgD6"
    access_token_secret = "TdyQpE0d3s80NpGRRtTNTB9l23tEAexNTk5oAiw9T9MIm"

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def crawl_tweets_from_profile():
    """
    Crawls 3200 from specific twitter profile. Limit is 3200 tweets and retweets due to API limits.
    """
    # useful ressources
    # https://github.com/twitterdev/Twitter-API-v2-sample-code - API doc with request examples
    # https://tweeterid.com - to get User IDs
    #  https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/User-Lookup/get_users_with_bearer_token.py
    # get tweet data - see for reference https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/User-Tweet-Timeline/user_tweets.py

    tweet_fields = "tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld"
    count = 32 # limit is 3200 tweets per user - therefore limit of 32 iterations
    user_id =  9204502


    """
    Possible Ids: 
    2834511 - Spiegel Normal
    17965092 - Spiegel Online
    114508061 - SZ; Süddeutsche Zeitung
    105554801 - Postillon
    5715752 - Zeit Online
    12509262 - Titanic Satire Magazin
     48660758 - Glausauge Satire (von WELT)
     8720562 - welt 
     9330012 - BildNews (Rund um die Uhr BILD)
     9204502 - BILD normal
    """
    tweets_limit = "100"
    url_tweet = ""
    pagination_token = ""
    for i in range(0, count):
        print("count: " + str(i))
        if pagination_token == "":
            url_tweet = "https://api.twitter.com/2/users/{}/tweets?{}&max_results={}".format(user_id, tweet_fields, tweets_limit)
            response_tweet = requests.request("GET", url_tweet, auth=bearer_oauth)
            print( " response.status: " + str(response_tweet.status_code))
            if response_tweet.status_code != 200:
                raise Exception(
                    "Request returned an error: {} {}".format(
                        response_tweet.status_code, response_tweet.text
                    )
                )

            response_json = response_tweet.json()
            pagination_token = response_json['meta']['next_token']
            print("pagination_token ", pagination_token)

        else:
            url_tweet = "https://api.twitter.com/2/users/{}/tweets?{}&max_results={}&pagination_token={}".format(user_id, tweet_fields,
                                                                                             tweets_limit, pagination_token)
            response_tweet = requests.request("GET", url_tweet, auth=bearer_oauth)
            print(" response.status: " + str(response_tweet.status_code))
            if response_tweet.status_code != 200:
                raise Exception(
                    "Request returned an error: {} {}".format(
                        response_tweet.status_code, response_tweet.text
                    )
                )

            response_json = response_tweet.json()
            pagination_token = response_json['meta']['next_token']
            print("pagination_token ", pagination_token)

        twitter_result_path = "TwitterCrawlDirectory/Twitter_API/Bild_CrawlDirectory/"
        filename = "profile_bild_data_" + str(i) + ".json"
        save_json(response_json, twitter_result_path, filename)


def test_get_all_data():

    # example url https://api.twitter.com/2/tweets/counts/all
    # https://developer.twitter.com/en/docs/twitter-api/tweets/counts/api-reference/get-tweets-counts-all
    tweet_fields = "tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld"
    count = 32  # limit is 3200 tweets per user - therefore limit of 32 iterations
    user_id = 9204502

    """
    Possible Ids: 
    2834511 - Spiegel Normal
    17965092 - Spiegel Online
    114508061 - SZ; Süddeutsche Zeitung
    105554801 - Postillon
    5715752 - Zeit Online
    12509262 - Titanic Satire Magazin
     48660758 - Glausauge Satire (von WELT)
     8720562 - welt 
     9330012 - BildNews (Rund um die Uhr BILD)
     9204502 - BILD normal
            """
    tweets_limit = "100"
    url_tweet = "https://api.twitter.com/2/tweets/counts/all"

    response_tweet = requests.request("GET", url_tweet, auth=bearer_oauth)
    print("response tweet", response_tweet)
    response_json = response_tweet.json()


    twitter_result_path = "./TwitterCrawlDirectory/"
    filename = "complete_bild_normal_data" + ".json"
    save_json(response_json, twitter_result_path, filename)


def save_json(json_obj, file_path, filename):
    with open(file_path + filename, 'w') as outfile:
        json.dump(json_obj, outfile)

def get_user_data():
    # TODO: improve method for profile analyses
    usernames = "usernames=SZ,Der_Postillon"
    user_ids = "ids=114508061,105554801"
    # note that the fields (also for tweet fields) have to be comma-seperated, but without empty spaces
    user_fields = "user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"

    """
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

    response_json = response.json()
    twitter_result_path = "./TwitterCrawlDirectory/"
    save_json(response_json, twitter_result_path)
    """

if __name__ == "__main__":

    #crawl_tweets_from_profile()
    test_get_all_data()

