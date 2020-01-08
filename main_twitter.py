# -*- coding: utf-8 -*-
import sys, getopt, datetime, codecs, re, string, tweepy, os, csv

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

def main(key, secret, token, token_secret, querysearch, since, until, maxtweets):
    try:
        tweetCriteria = got.manager.TweetCriteria()
        filename = querysearch + "-" + since + "-" + until
        outputFileName = filename + ".csv"

        tweetCriteria.since = since
        tweetCriteria.until = until
        tweetCriteria.querySearch = querysearch
        if maxtweets != "0" and maxtweets != "":
            tweetCriteria.maxTweets = int(maxtweets)

        print('Searching...\n')

        def receiveBuffer(tweets):
            # Authentication Data
            consumer_key = key
            consumer_secret = secret
            access_token = token
            access_token_secret = token_secret

            try:
                # Authorize
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth, wait_on_rate_limit=True)
            except:
                print("Error: Authentication Failed")

            row_list = [["Username", "Created At", "Retweets", "Favorites", "Tweet", "Location", "Mentions", "Hashtags", "ID Tweet", "Permalink"]]

            for t in tweets:
                user_info = api.get_user(t.author_id)
                row = [
                    t.username,
                    t.date.strftime("%Y-%m-%d %H:%M"),
                    t.retweets,
                    t.favorites,
                    t.text,
                    user_info._json["location"],
                    t.mentions,
                    t.hashtags,
                    t.id,
                    t.permalink
                ]
                row_list.append(row)

            with open(outputFileName, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(row_list)
            print('More %d saved on file...\n' % len(tweets))

        got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

    except Exception as e:
        print('Arguments parser error, try -h', e)
    finally:
        # outputFile.close()
        print('Done. Output file generated "%s".' % outputFileName)
        return outputFileName
