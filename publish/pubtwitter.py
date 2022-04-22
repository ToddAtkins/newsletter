#!/usr/bin/env python
import argparse
import configparser
import os
import twitter
import time
import pprint as pp

def login(consumer_key, consumer_secret, access_token_key, access_token_secret):
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)
    return(api)

def get_bookmark(file):
    bookmark = 0
    if os.path.exists(file):
        with open(file, 'rt') as f:
            bookmark = int(f.readline())
            f.close()
    return bookmark

def get_statuses(api, user=None):
    statuses = api.GetUserTimeline(user_id=user)
    return statuses

def save_bookmark(file, bookmark):
    with open(file, 'wt') as f:
        f.write(str(bookmark))
        f.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', type=str, default=os.path.expanduser('~/.newsletter.ini'))
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.readfp(open(args.config))
    twitcfg = dict(config.items('twitter'))
    api = login(consumer_key=twitcfg['consumer_key'],
                consumer_secret=twitcfg['consumer_secret'],
                access_token_key=twitcfg['access_token_key'],
                access_token_secret=twitcfg['access_token_secret'])

    statuses = api.GetUserTimeline()
    for s in statuses:
        print(s.id)
        print(s.created_at)
        print(s.text + '\n')

if __name__ == "__main__":
    main()
