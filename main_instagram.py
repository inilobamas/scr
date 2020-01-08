from inscrawler import InsCrawler
from InstagramAPI import InstagramAPI
from datetime import datetime
import json, requests, time, csv

def login(username, password):
    debug = False
    ins_crawler = InsCrawler(has_screen=debug)
    return ins_crawler.login(username, password)

def get_posts_by_hashtag(tag, number, debug):
    ins_crawler = InsCrawler(has_screen=debug)
    return ins_crawler.get_latest_posts_by_tag(tag, number)

def get_media_id(url):
    base_url = "https://api.instagram.com/oembed/?url="
    req = requests.get(base_url + url)
    media_id = req.json()['media_id']
    return media_id

def get_all_comments(username, password, data):
    username = username
    pwd      = password

    API = InstagramAPI(username, pwd)
    API.login()

    row_list = [["URL", "Caption", "Image URL", "Username", "Full Name", "Comment", "Comment Created At"]]

    for post in data:
        try:
            media_id = get_media_id(post["key"])

            #stop conditions, the script will end when first of them will be true
            # until_date = None # '2017-03-31'
            count      = 100

            has_more_comments = True
            max_id            = ''
            comments          = []

            while has_more_comments:
                _ = API.getMediaComments(media_id,max_id=max_id)
                #comments' page come from older to newer, lets preserve desc order in full list
                for c in reversed(API.LastJson['comments']):
                    comments.append(c)
                has_more_comments = API.LastJson.get('has_more_comments',False)
                #evaluate stop conditions
                if count and len(comments)>=count:
                    comments = comments[:count]
                    #stop loop
                    has_more_comments = False
                    print("stopped by count")
                # if until_date:
                #     older_comment = comments[-1]
                #     dt=datetime.utcfromtimestamp(older_comment.get('created_at_utc',0))
                #     #only check all records if the last is older than stop condition
                #     if dt.isoformat()<=until_date:
                #         #keep comments after until_date
                #         comments = [
                #             c
                #             for c in comments
                #             if datetime.utcfromtimestamp(c.get('created_at_utc',0)) > until_date
                #         ]
                #         #stop loop
                #         has_more_comments = False
                #         print("stopped by until_date")
                #next page
                if has_more_comments:
                    max_id = API.LastJson.get('next_max_id','')
                    time.sleep(2)
        except Exception as e:
            print("media err", e)

        try:
            for comment in comments:
                row = [
                    post["key"],
                    post["caption"],
                    post["img_url"],
                    comment["user"]["username"],
                    comment["user"]["full_name"],
                    comment["text"],
                    comment["created_at"]
                ]
                row_list.append(row)
        except Exception as e:
            print("comment err", e)

    return row_list


def output(username, password, data, outputFileName):
    row_list = get_all_comments(username, password, data)

    with open(outputFileName, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_list)

def main(username, password, hashtag, number_post):
    output_file_name = hashtag + ".csv"

    try:
        number_post = number_post
        username = username
        password = password
        hashtag = hashtag.replace("#", "")

        output(
            username,
            password,
            get_posts_by_hashtag(hashtag, number_post, False), output_file_name
        )
    except Exception as e:
        print('Arguments parser error, try -h', e)
    finally:
        # outputFile.close()
        print('Done. Output file generated "%s".' % output_file_name)
        return output_file_name
