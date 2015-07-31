#!/usr/bin/env python
import twitter
import time
import sys
import pprint as pp

def login(consumer_key, consumer_secret, access_token_key, access_token_secret):
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)
    return(api)

def get_bookmark(file):
    b = 0
    with open(file, 'rt') as f:
        b = int(f.readline())
        f.close()
    return b

def get_statuses(api, user):
    statuses = api.GetUserTimeline(user)
    return statuses

def save_bookmark(file, b):
    with open(file, 'wt') as f:
        f.write(str(b))
        f.close()

def main():
    api = get_api()
    statuses = get_statuses(api, user='SB_Wino')
    for s in statuses:
        print(s.id)
        print(s.created_at)
        print(s.text + '\n')
    
if __name__ == "__main__":
    main()
    