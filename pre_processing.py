"""
Handles the pre-processing used across various other scripts
"""

import re
import string

import pandas as pd
from sklearn.model_selection import train_test_split


def cleanText(var):
    # replace punctuation with spaces
    var = re.sub('[{}]'.format(string.punctuation), " ", var)
    # remove double spaces
    var = re.sub(r'\s+', " ", var)
    # put in lower case
    var = var.lower().split()
    # remove words that are smaller than 3 characters
    var = [w for w in var if len(w) >= 3]
    # remove stop-words
    # var = [w for w in var if w not in stopwords.words('english')]
    # stemming
    # stemmer = nltk.PorterStemmer()
    # var = [stemmer.stem(w) for w in var]
    var = " ".join(var)
    return var


# Removes 'rt' from all input data
def my_clean(text):
    text = text.lower().split()
    text = [w for w in text]
    text = " ".join(text)
    text = re.sub(r"rt", "", text)
    return text


def strip_links(text):
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text


def strip_all_entities(text):
    entity_prefixes = ['@', '#']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator, ' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)


def preProcessing(strings):
    clean_tweet_texts = []
    for string in strings:
        clean_tweet_texts.append(my_clean(strip_all_entities(strip_links(string))))
        # clean_tweet_texts.append(my_clean(string))
    return clean_tweet_texts


def get_text_data(data_path, dataset):
    df = pd.read_csv(data_path, encoding='utf-8')

    if dataset == "polarity":
        X = df['tweet'].values
        y = df['class'].values
    elif dataset == "hate":
        # Removing the offensive comments, keeping only neutral and hatespeech,
        # and convert the class value from 2 to 1 for simplification purposes
        df = df[df['class'] != 1]
        X = df['tweet'].values
        y = df['class'].apply(lambda x: 1 if x == 2 else 0).values

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y, test_size=0.25)

    new_X_test = preProcessing(X_test)

    return X_train, X_test, y_train, y_test, new_X_test