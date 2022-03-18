# importing libraries and packages
import json
import os

import path as path
import snscrape.modules.twitter as sntwitter
import pandas as pd

# Creating list to append tweet data
if __name__ == "__main__":
    print("Crawling starts")
    news_tweets_df = pd.DataFrame()
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:WELT_GLASAUGE').get_items()):  # declare a username
        print("iteration: ", i)
        print("tweet: ", tweet)
        date = str(tweet.date)
        print("Tweet data", tweet.date)
        if '2021' in date:  # number of tweets you want to scrape

            print("Add Tweet to dataset")
            # possible attributes: url	date content	renderedContent	id	user	outlinks	tcooutlinks	replyCount	retweetCount	likeCount	quoteCount	conversationId	lang	source	media	retweetedTweet	quotedTweet	mentionedUser



            news_tweets_df = news_tweets_df.append({
                'id': tweet.id,
                'content': tweet.content,
                'author': tweet.user.username,
                'media': tweet.media,
                'hashtags': tweet.hashtags,
                'publishing_date': str(tweet.date),
                'url': tweet.url,
                'outlinks': tweet.outlinks,
                'in_reply_to_user': tweet.inReplyToUser,
                'mentioned_users': tweet.mentionedUsers,
                'likes': tweet.likeCount,
                'reply_count': tweet.replyCount,
                'retweet_count': tweet.retweetCount,
                'quote_count': tweet.quoteCount,
                'place': tweet.place,
                'coordinates': tweet.coordinates,
            }, ignore_index=True)

        elif '2020' in date:
            print("Tweet contains 2020; break")
            break
        else:
            print("Tweet contains 2022; skip")
            continue


    # Creating a dataframe from the tweets list above
    #tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username']) - columns could be useful later
    #result = tweets_df1.to_json(orient="split") # old ver
    result = news_tweets_df.to_json(orient="records")
    parsed = json.loads(result)
    filename = "glasauge_2021.json"
    path = os.path.join("./TwitterCrawlDirectory/Tweets_2021/", filename)
    with open(path, 'w+') as outfile:
        json.dump(parsed, outfile)
    print('Crawling done')
