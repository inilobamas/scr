import sys
import time
import requests
import lxml.html
import csv
from urllib.request import Request, urlopen
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import ast
import json
import os
from urllib.request import Request, urlopen

from lxml.cssselect import CSSSelector

YOUTUBE_COMMENTS_URL = 'https://www.youtube.com/all_comments?v={youtube_id}'
YOUTUBE_COMMENTS_AJAX_URL = 'https://www.youtube.com/comment_ajax'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'

def get_info_video(url):
    # For ignoring SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Making the website believe that you are accessing it using a mozilla browser
    req = Request(url, headers={'User-Agent': USER_AGENT})
    webpage = urlopen(req).read()

    # Creating a BeautifulSoup object of the html page for easy extraction of data.
    soup = BeautifulSoup(webpage, 'html.parser')
    html = soup.prettify('utf-8')
    video_details = {}
    other_details = {}

    video_details['TITLE'] = ""
    for span in soup.findAll('span', attrs={'class': 'watch-title'}):
        video_details['TITLE'] = span.text.strip()

    video_details['CHANNEL_NAME'] = ""
    for script in soup.findAll('script', attrs={'type': 'application/ld+json'}):
        channelDesctiption = json.loads(script.text.strip())
        video_details['CHANNEL_NAME'] = channelDesctiption['itemListElement'][0]['item']['name']

    video_details['NUMBER_OF_VIEWS'] = ""
    for div in soup.findAll('div', attrs={'class': 'watch-view-count'}):
        video_details['NUMBER_OF_VIEWS'] = div.text.strip()

    video_details['LIKES'] = ""
    for button in soup.findAll('button', attrs={'title': 'I like this'}):
        video_details['LIKES'] = button.text.strip()

    video_details['DISLIKES'] = ""
    for button in soup.findAll('button', attrs={'title': 'I dislike this'}):
        video_details['DISLIKES'] = button.text.strip()

    video_details['NUMBER_OF_SUBSCRIPTIONS'] = ""
    for span in soup.findAll('span', attrs={
        'class': 'yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count'}):
        video_details['NUMBER_OF_SUBSCRIPTIONS'] = span.text.strip()

    hashtags = []
    for span in soup.findAll('span', attrs={'class': 'standalone-collection-badge-renderer-text'}):
        for a in span.findAll('a', attrs={'class': 'yt-uix-sessionlink'}):
            hashtags.append(a.text.strip())
    video_details['HASH_TAGS'] = hashtags

    # with open('data.json', 'w', encoding='utf8') as outfile:
    #     json.dump(video_details, outfile, ensure_ascii=False, indent=4)

    print('----------Extraction of data is complete. Check json file.----------')
    return video_details


def find_value(html, key, num_chars=2):
    pos_begin = html.find(key) + len(key) + num_chars
    pos_end = html.find('"', pos_begin)
    return html[pos_begin: pos_end]


def extract_comments(html):
    tree = lxml.html.fromstring(html)
    item_sel = CSSSelector('.comment-item')
    text_sel = CSSSelector('.comment-text-content')
    time_sel = CSSSelector('.time')
    author_sel = CSSSelector('.user-name')

    for item in item_sel(tree):
        yield {'cid': item.get('data-cid'),
               'text': text_sel(item)[0].text_content(),
               'time': time_sel(item)[0].text_content().strip(),
               'author': author_sel(item)[0].text_content()}


def extract_reply_cids(html):
    tree = lxml.html.fromstring(html)
    sel = CSSSelector('.comment-replies-header > .load-comments')
    return [i.get('data-cid') for i in sel(tree)]


def ajax_request(session, url, params, data, retries=10, sleep=20):
    for _ in range(retries):
        response = session.post(url, params=params, data=data)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            return response_dict.get('page_token', None), response_dict['html_content']
        else:
            time.sleep(sleep)


def download_comments(youtube_id, sleep=1):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT

    # Get Youtube page with initial comments
    response = session.get(YOUTUBE_COMMENTS_URL.format(youtube_id=youtube_id))
    html = response.text
    reply_cids = extract_reply_cids(html)

    ret_cids = []
    for comment in extract_comments(html):
        ret_cids.append(comment['cid'])
        yield comment

    page_token = find_value(html, 'data-token')
    session_token = find_value(html, 'XSRF_TOKEN', 4)

    first_iteration = True

    # Get remaining comments (the same as pressing the 'Show more' button)
    while page_token:
        data = {'video_id': youtube_id,
                'session_token': session_token}

        params = {'action_load_comments': 1,
                  'order_by_time': True,
                  'filter': youtube_id}

        if first_iteration:
            params['order_menu'] = True
        else:
            data['page_token'] = page_token

        response = ajax_request(session, YOUTUBE_COMMENTS_AJAX_URL, params, data)
        if not response:
            break

        page_token, html = response

        reply_cids += extract_reply_cids(html)
        for comment in extract_comments(html):
            if comment['cid'] not in ret_cids:
                ret_cids.append(comment['cid'])
                yield comment

        first_iteration = False
        time.sleep(sleep)

    # Get replies (the same as pressing the 'View all X replies' link)
    for cid in reply_cids:
        data = {'comment_id': cid,
                'video_id': youtube_id,
                'can_reply': 1,
                'session_token': session_token}

        params = {'action_load_replies': 1,
                  'order_by_time': True,
                  'filter': youtube_id,
                  'tab': 'inbox'}

        response = ajax_request(session, YOUTUBE_COMMENTS_AJAX_URL, params, data)
        if not response:
            break

        _, html = response

        for comment in extract_comments(html):
            if comment['cid'] not in ret_cids:
                ret_cids.append(comment['cid'])
                yield comment
        time.sleep(sleep)


def main(youtube_id, output, limit):
# zCYN4KtreYk
# downloader.py --youtubeid zCYN4KtreYk --output zCYN4KtreYk [--youtubeid YOUTUBEID] [--output OUTPUT]
# parser = argparse.ArgumentParser(add_help=False, description=('Download Youtube comments without using the Youtube API'))
# parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
# parser.add_argument('--youtubeid', '-y', help='ID of Youtube video for which to download the comments')
# parser.add_argument('--output', '-o', help='Output filename (output format is line delimited JSON)')
# parser.add_argument('--limit', '-l', type=int, help='Limit the number of comments')

    try:
        # args = parser.parse_args(sys.argv[1:])
        row_list = [["Channel", "Title", "Number Of Views", "Number Of Subscriptions", "Hashtag", "Comment ID", "Author", "Comment", "Time"]]

        info_video = get_info_video(YOUTUBE_COMMENTS_URL.format(youtube_id=youtube_id))

        if not youtube_id or not output:
            raise ValueError('you need to specify a Youtube ID and an output filename')

        print('Downloading Youtube comments for video:', youtube_id)
        count = 0
        # with io.open(output, 'w', encoding='utf8') as fp:
        for comment in download_comments(youtube_id):

            row = [
                info_video["CHANNEL_NAME"],
                info_video["TITLE"],
                info_video["NUMBER_OF_VIEWS"],
                info_video["NUMBER_OF_SUBSCRIPTIONS"],
                info_video["HASH_TAGS"],
                comment["cid"],
                comment["author"],
                comment["text"],
                comment["time"]
            ]
            row_list.append(row)

            count += 1
            sys.stdout.write('Downloaded %d comment(s)\r' % count)
            sys.stdout.flush()
            if limit and (limit != 0 and count >= limit):
                break
        print('\nDone!')
        with open(output, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(row_list)

        return output


    except Exception as e:
        print('Error:', str(e))