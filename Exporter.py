# -*- coding: utf-8 -*-
import sys,getopt,datetime,codecs,re,string,tweepy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

analyzer = SentimentIntensityAnalyzer()

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

def analyze(sample):
	sample = clean_tweet(sample)
	compound = analyzer.polarity_scores(sample)["compound"]
	pos = analyzer.polarity_scores(sample)["pos"]
	neu = analyzer.polarity_scores(sample)["neu"]
	neg = analyzer.polarity_scores(sample)["neg"]
	result = {
		"compound": compound,
		"pos": pos,
		"neu": neu,
		"neg": neg,
		"clean_tweet": sample
	}
	return result

def main(argv):

	if len(argv) == 0:
		print('You must pass some parameters. Use \"-h\" to help.')
		return

	if len(argv) == 1 and argv[0] == '-h':
		f = open('exporter_help_text.txt', 'r')
		print(f.read())
		f.close()

		return

	try:
		opts, args = getopt.getopt(argv, "", ("username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output="))

		tweetCriteria = got.manager.TweetCriteria()
		outputFileName = "got.csv"

		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg

			elif opt == '--since':
				tweetCriteria.since = arg

			elif opt == '--until':
				tweetCriteria.until = arg

			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg

			elif opt == '--toptweets':
				tweetCriteria.topTweets = True

			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)
			
			elif opt == '--near':
				tweetCriteria.near = '"' + arg + '"'
			
			elif opt == '--within':
				tweetCriteria.within = '"' + arg + '"'

			elif opt == '--within':
				tweetCriteria.within = '"' + arg + '"'

			elif opt == '--output':
				outputFileName = arg
				
		outputFile = codecs.open(outputFileName, "w+", "utf-8")

		outputFile.write('compound;positive;neutral;negative;username;date;retweets;favorites;text:clean_text;geo;mentions;hashtags;id;permalink')

		print('Searching...\n')

		def receiveBuffer(tweets):
			# Authentication Data
			consumer_key = 'bSewMjpb0enxVAEGJujbJO0SA'
			consumer_secret = 'wVsEzlIshcgIUsc9SDNQWXKaNdL8reo2Jv70wZjUCQ662wlVIX'
			access_token = '238334622-8me025RTN9or9GX6znzp5PGoDQBO9uyxnZiGxaUu'
			access_token_secret = 'buKLU0LF0rX3cJgsjgCCGTbq1diEpvCZpaNFvGMyGtyfr'

			try:
				# Authorize
				auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
				auth.set_access_token(access_token, access_token_secret)
				api = tweepy.API(auth, wait_on_rate_limit=True)
			except:
				print("Error: Authentication Failed")

			for t in tweets:
				user_info = api.get_user(t.author_id)
				result_analyze = analyze(t.text)
				outputFile.write(('\n%s;%s;%s;%s;%s;%s;%s;%s;%s;"%s";%s;%s;%s;"%s";%s' % (result_analyze["compound"], result_analyze["pos"], result_analyze["neu"], result_analyze["neg"], t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, result_analyze["clean_tweet"], user_info._json["location"], t.mentions, t.hashtags, t.id, t.permalink)))
			outputFile.flush()
			print('More %d saved on file...\n' % len(tweets))

		got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

	except arg:
		print('Arguments parser error, try -h' + arg)
	finally:
		outputFile.close()
		print('Done. Output file generated "%s".' % outputFileName)

if __name__ == '__main__':
	main(sys.argv[1:])
