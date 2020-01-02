import re
import tweepy
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# CATATAN GANTI REGEX
def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+) ", " ", tweet).split())

def analyze(sample):
    sample = clean_tweet(sample)
    compound = analyzer.polarity_scores(sample)["compound"]
    pos = analyzer.polarity_scores(sample)["pos"]
    neu = analyzer.polarity_scores(sample)["neu"]
    neg = analyzer.polarity_scores(sample)["neg"]
    print("COMPOUND", compound)
    print("POS", pos)
    print("NEU", neu)
    print("NEG", neg)
    result = {
        "compound": compound,
        "pos": pos,
        "neu": neu,
        "neg": neg
    }
    return result


# Authentication Data
consumer_key = 'bSewMjpb0enxVAEGJujbJO0SA'
consumer_secret = 'wVsEzlIshcgIUsc9SDNQWXKaNdL8reo2Jv70wZjUCQ662wlVIX'
access_token = '238334622-8me025RTN9or9GX6znzp5PGoDQBO9uyxnZiGxaUu'
access_token_secret = 'buKLU0LF0rX3cJgsjgCCGTbq1diEpvCZpaNFvGMyGtyfr'

try:
    # Authorize
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
except:
    print("Error: Authentication Failed")

# Prep var
hashtag = "#delivery"
filename = hashtag + ".csv"

# Prep CSV
csvFile = open(filename, 'a')
csvWriter = csv.writer(csvFile)

# Init Vader
analyzer = SentimentIntensityAnalyzer()

# Execute API tweepy with filters
data_objs = []
for page in tweepy.Cursor(api.search, q=hashtag).pages():
    for data_objs in page:
        user_info = api.get_user(data_objs._json["user"]["id"])
        print(data_objs._json["user"]["id"])
        print(data_objs._json["text"])
        result_analyze = analyze(data_objs._json["text"])
        print(result_analyze)
        csvWriter.writerow([result_analyze["compound"], result_analyze["pos"], result_analyze["neu"], result_analyze["neg"], data_objs._json["text"].encode('utf-8')])