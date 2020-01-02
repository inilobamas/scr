import string
import tweepy
import csv
import re
import datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Emoji patterns
emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)

#HappyEmoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])

# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])

#combine sad and happy emoticons
emoticons = emoticons_happy.union(emoticons_sad)

def clean_tweet(tweet):
    stop_words = set(stopwords.words('indonesian'))
    word_tokens = word_tokenize(tweet)
    # after tweepy preprocessing the colon symbol left remain after      #removing mentions
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    # replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+', ' ', tweet)
    # remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)
    # filter using NLTK library append it to a string
    filtered_tweet = [w for w in word_tokens if not w in stop_words]
    filtered_tweet = []
    # looping through conditions
    for w in word_tokens:
        # check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)
    return ' '.join(filtered_tweet)
    # print(word_tokens)
    # print(filtered_sentence)return tweet

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
        "neg": neg,
        "clean_tweet": sample
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
hashtag = "#ibukotabaru"
filename = hashtag + ".csv"

# Prep CSV
csvFile = open(filename, 'a')
csvWriter = csv.writer(csvFile)

# Init Vader
analyzer = SentimentIntensityAnalyzer()

# Execute API tweepy with filters
# List date 3 months
# 25 August 2019 - 1 December 2019
list_date = [
    {
        "start_date": "2019-08-25",
        "end_date": "2019-08-26"
    },
    {
        "start_date": "2019-08-27",
        "end_date": "2019-08-28"
    },
    {
        "start_date": "2019-08-29",
        "end_date": "2019-08-30"
    },
    {
        "start_date": "2019-08-31",
        "end_date": "2019-09-01"
    },
    {
        "start_date": "2019-09-02",
        "end_date": "2019-09-03"
    },
    {
        "start_date": "2019-09-03",
        "end_date": "2019-09-04"
    },
    {
        "start_date": "2019-09-05",
        "end_date": "2019-09-06"
    },
    {
        "start_date": "2019-09-07",
        "end_date": "2019-09-08"
    },
    {
        "start_date": "2019-09-09",
        "end_date": "2019-09-10"
    },
    {
        "start_date": "2019-09-11",
        "end_date": "2019-09-12"
    },
    {
        "start_date": "2019-09-13",
        "end_date": "2019-09-14"
    },
    {
        "start_date": "2019-09-15",
        "end_date": "2019-09-16"
    },
    {
        "start_date": "2019-09-17",
        "end_date": "2019-09-18"
    },
    {
        "start_date": "2019-09-19",
        "end_date": "2019-09-20"
    },
    {
        "start_date": "2019-09-21",
        "end_date": "2019-09-22"
    },
    {
        "start_date": "2019-09-23",
        "end_date": "2019-09-24"
    },
    {
        "start_date": "2019-09-25",
        "end_date": "2019-09-26"
    },
    {
        "start_date": "2019-09-27",
        "end_date": "2019-09-28"
    },
    {
        "start_date": "2019-09-29",
        "end_date": "2019-09-30"
    },
    {
        "start_date": "2019-10-01",
        "end_date": "2019-10-02"
    },
    {
        "start_date": "2019-10-03",
        "end_date": "2019-10-04"
    },
    {
        "start_date": "2019-10-05",
        "end_date": "2019-10-06"
    },
    {
        "start_date": "2019-10-07",
        "end_date": "2019-10-08"
    },
    {
        "start_date": "2019-10-09",
        "end_date": "2019-10-10"
    },
    {
        "start_date": "2019-10-11",
        "end_date": "2019-10-12"
    },
    {
        "start_date": "2019-10-13",
        "end_date": "2019-10-14"
    },
    {
        "start_date": "2019-10-15",
        "end_date": "2019-10-16"
    },
    {
        "start_date": "2019-10-17",
        "end_date": "2019-10-18"
    },
    {
        "start_date": "2019-10-19",
        "end_date": "2019-10-20"
    },
    {
        "start_date": "2019-10-21",
        "end_date": "2019-10-22"
    },
    {
        "start_date": "2019-10-23",
        "end_date": "2019-10-24"
    },
    {
        "start_date": "2019-10-25",
        "end_date": "2019-10-26"
    },
    {
        "start_date": "2019-10-27",
        "end_date": "2019-10-28"
    },
    {
        "start_date": "2019-10-29",
        "end_date": "2019-10-30"
    },
    {
        "start_date": "2019-10-31",
        "end_date": "2019-11-01"
    },
    {
        "start_date": "2019-11-02",
        "end_date": "2019-11-03"
    },
    {
        "start_date": "2019-11-04",
        "end_date": "2019-11-05"
    },
    {
        "start_date": "2019-11-06",
        "end_date": "2019-11-07"
    },
    {
        "start_date": "2019-11-08",
        "end_date": "2019-11-09"
    },
    {
        "start_date": "2019-11-10",
        "end_date": "2019-11-11"
    },
    {
        "start_date": "2019-11-12",
        "end_date": "2019-11-13"
    },
    {
        "start_date": "2019-11-14",
        "end_date": "2019-11-15"
    },
    {
        "start_date": "2019-11-16",
        "end_date": "2019-11-17"
    },
    {
        "start_date": "2019-11-18",
        "end_date": "2019-11-19"
    },
    {
        "start_date": "2019-11-20",
        "end_date": "2019-11-21"
    },
    {
        "start_date": "2019-11-22",
        "end_date": "2019-11-23"
    },
    {
        "start_date": "2019-11-24",
        "end_date": "2019-11-25"
    },
    {
        "start_date": "2019-11-26",
        "end_date": "2019-11-27"
    },
    {
        "start_date": "2019-11-28",
        "end_date": "2019-11-29"
    },
    {
        "start_date": "2019-11-30",
        "end_date": "2019-12-01"
    }

]
for date in list_date:
    print("start_date: ", date["start_date"])
    print("start_date: ", date["end_date"])
    data_objs = []
    for item in tweepy.Cursor(api.search, since_id=date["start_date"], until=date["end_date"], lang="id", q=hashtag).items():
        print("item", item)
        # for data_objs in page:
        #     user_info = api.get_user(data_objs._json["user"]["id"])
        #     print(data_objs._json["user"]["id"])
        #     print(data_objs._json["text"])
        #     result_analyze = analyze(data_objs._json["text"])
        #     print(result_analyze)
        #     date_time_str = data_objs._json["created_at"]
        #     created_at = date_time_str #datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
        #     csvWriter.writerow([created_at, result_analyze["compound"], result_analyze["pos"], result_analyze["neu"], result_analyze["neg"], result_analyze["clean_tweet"].encode('utf-8')])