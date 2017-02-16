import configparser
from datetime import datetime, timedelta

import twitter


def fetch_disruptions_for_sbahn_line():
    result = {'s1': False, 's2': False, 's3': False, 's4': False, 's5': False, 's6': False}
    timeline = _get_vvs_twitter_timeline()

    # check the text for occurrences of sbahn lines
    for post in timeline:
        text = post.text.lower()
        if 's1' in text:
            result['s1'] = True
        if 's2' in text:
            result['s2'] = True
        if 's3' in text:
            result['s3'] = True
        if 's4' in text:
            result['s4'] = True
        if 's5' in text:
            result['s5'] = True
        if 's6' in text or 's60' in text:
            result['s6'] = True

    return result


def fetch_disruption_message():
    timeline = _get_vvs_twitter_timeline()
    message = ''

    for post in timeline:
        text_lower = post.text.lower()
        if 's1' in text_lower or 's2' in text_lower or 's3' in text_lower or 's4' in text_lower \
                or 's5' in text_lower or 's6' in text_lower or 's60' in text_lower:
            if message != '':
                message += ' --- '
            message += post.text

    return message


def _get_vvs_twitter_timeline():
    # read twitter api keys from config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    api = twitter.Api(consumer_key=config['twitter']['ConsumerKey'],
                      consumer_secret=config['twitter']['ConsumerSecret'],
                      access_token_key=config['twitter']['AccessTokenKey'],
                      access_token_secret=config['twitter']['AccessTokenConfig'])
    timeline = api.GetUserTimeline(screen_name='VVS')
    relevant_posts = []
    for status in timeline:
        tweet_timestamp = datetime.fromtimestamp(status.created_at_in_seconds)
        limit = datetime.now() - timedelta(hours=2)
        if tweet_timestamp > limit:
            relevant_posts.append(status)
    return relevant_posts


def is_disruption(message):
    return message != ''
