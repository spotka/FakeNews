import json
import os
import re

import nltk
import pandas
import pandas as pd
import plotly.graph_objects as go
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from spacy.lang.de.examples import sentences
from collections import Counter

import spacy

"""
Dieses Skript bietet zahlreich3e Methoden aus der NLTK und spaCy Pipeline um eine Top 3 der höchst frequentierten Wörter anhand
einer Frequency Distribution zu erstellen. Die Methoden tragen die Zugehörigkeit zu einer der jeweiligen Libraries im Namen.
Das Preprocessing besteht dabei immer aus dem Herausfiltern von Stopwords und Links, einer Lemmatisierung sowie Tokenisierung der Tweets.

Weiterführende Quellen: https://github.com/solariz/german_stopwords, https://www.nltk.org, https://spacy.io/usage

"""

def load_tweets(filepath, file):

    filename = os.fsdecode(file)
    path = filepath + filename
    with open(path, "rb") as infile:
        data = json.load(infile)
        author = data[0]['author']
        total_tweets = ""
        for tweet in data:
            tweet_content = tweet['content']
            total_tweets += tweet_content


    return total_tweets, author

def nltk_lemmatization(tokenized_tweets):
    lemmatizer = nltk.WordNetLemmatizer()
    nltk_lemmatized_doc = [lemmatizer.lemmatize(w) for w in tokenized_tweets]
    return nltk_lemmatized_doc

def spacy_lemmatization_punctuation(tweets_str):
    nlp = spacy.load("de_core_news_lg")
    texts = tweets_str.split(".") # due to limitation of pipeline
    spacy_lemmatized_doc = []
    for i, w1 in enumerate(texts):
        print("iteration", i, len(texts))
        nlp_text = nlp(w1)
        for token in nlp_text:
            # print("token ", token, token.is_punct, token.is_space, token.is_alpha)
            if not token.is_punct or token.is_space or token.is_stop or token.like_url:
                if token.is_alpha:
                    spacy_lemmatized_doc.append(token.lemma_)
                else:
                    continue
            else:
                continue
    return spacy_lemmatized_doc


def nltk_tokenize(tweets_filtered_lowercased):
    tokenized_tweets = nltk.word_tokenize(tweets_filtered_lowercased, language="german") # remove punctuation
    return tokenized_tweets

def top_3_most_frequent_words(filtered_tweets):

    word_freq = Counter(filtered_tweets)
    common_words = word_freq.most_common(3)
    print("common words", common_words)
    fdist = FreqDist(filtered_tweets)
    most_common_words = fdist.most_common(3)

    print("top3", most_common_words)

    return most_common_words

def create_visulisation(dataframe, path_to_save):

    data = []
    for row in dataframe.iterrows():
        top_3_words = [row[1]['top_1_word'], row[1]['top_2_word'], row[1]['top_3_word']]
        top_3_counts = [row[1]['top_1_count'], row[1]['top_2_count'], row[1]['top_3_count']]
        data.append(go.Bar(name=row[1]['news_agency'], x=top_3_words, y=top_3_counts))
    # Change the bar mode

    fig = go.Figure(data=data)
    fig.update_layout(barmode='group')
    fig.show()
    fig.write_html(path_to_save)

if __name__ == "__main__":
    print("=== Most frequent word analysis ===")
    nltk.download('punkt')
    nltk.download('omw-1.4')
    german_stop_words = stopwords.words('german')  # nltk stopwords
    stopwords_path = "../german_stopwords-master/german_stopwords_full.txt"

    with open(stopwords_path) as f:
        stopword_lines = f.readlines()
        full_stopword_list = []
        print("stopwords", stopwords)
        for stopwords in stopword_lines:
            cleaned_stopword = stopwords.rstrip()
            # print("cleaned stopwords", cleaned_stopword)
            full_stopword_list.append(cleaned_stopword)




    # load tweets from file, returns string with tweets
    file_path = "../DataCrawling/TwitterCrawlDirectory/Tweets_2021/"


    directory = os.fsencode(file_path)
    nltk_df = pd.DataFrame()
    spacy_df = pd.DataFrame()
    for file in os.listdir(directory):
        total_tweets, author = load_tweets(file_path, file)

        #remove links and names - otherwise disortion
        tweets_total_no_links = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', total_tweets, flags=re.MULTILINE)
        tweets_total_no_names = re.sub(r'\b(BILD|TITANIC|SZPlus|BILDlive|"SPIEGEL"|"Spiegel"|Spiegel+)', '',
                                               tweets_total_no_links, flags=re.MULTILINE)



        # spacy-based precprocessing piepline

        spacy_lemmatized_tweets = spacy_lemmatization_punctuation(total_tweets)

        # custom stop words

        spacy_custom_filtered_tweets = spacy_lemmatized_tweets


        # nltk based pipeline tokenization
        nltk_tokenized_tweets =  nltk_tokenize(total_tweets)
        nltk_lemmatized = nltk_lemmatization(nltk_tokenized_tweets)

        # remove stopwords - nltk
        words = [word.lower() for word in nltk_lemmatized if word.isalpha()]  # nltk method
        nltk_filtered_tweets = [word for word in words if word not in german_stop_words]

        spacy_top3 = top_3_most_frequent_words(spacy_custom_filtered_tweets)
        spacy_df = spacy_df.append({
            "news_agency": author,
            "top_1_word": spacy_top3[0][0],
            "top_1_count": spacy_top3[0][1],
            "top_2_word": spacy_top3[1][0],
            "top_2_count": spacy_top3[1][1],
            "top_3_word": spacy_top3[2][0],
            "top_3_count": spacy_top3[2][1]

        }, ignore_index=True)

        nltk_top3 = top_3_most_frequent_words(nltk_filtered_tweets)
        nltk_df = nltk_df.append({
            "news_agency": author,
            "top_1_word": nltk_top3[0][0],
            "top_1_count": nltk_top3[0][1],
            "top_2_word": nltk_top3[1][0],
            "top_2_count": nltk_top3[1][1],
            "top_3_word": nltk_top3[2][0],
            "top_3_count": nltk_top3[2][1]

        }, ignore_index=True)

    spacy_custom_path = "../Results/Language_Analysis/top3_spacy_pipeline_no_regex.html"
    create_visulisation( spacy_df, spacy_custom_path)

    path_nltk = "../Results/Language_Analysis/top3_nltk_pipeline_no_regex.html"
    create_visulisation(nltk_df, path_nltk)
