#!/usr/bin/env python
import argparse
import random
import re
import json
import os

def add_quote(file, quote, author):
    quotes = read_quotes(file)
    quotes[quote] = author
    if len(quotes):
        with open(file, 'w') as f:
            json.dump(quotes, f)

def random_quote(f):
    quotes = read_quotes(f)
    r = random.choice(list(quotes.keys()))
    return({'quote': r, 'author': quotes[r]})

def read_quotes(file):
    quotes = {}
    with open(file, 'r') as f:
        quotes = json.load(f)
    return quotes
    
def print_random_quote(file, width=0):
    q = random_quote(file)
    if width == 0:
        print("{0}\n-{1}".format(q['quote'], q['author']))
    else:
        import textwrap
        print("{0}\n-{1}".format(textwrap.fill(q['quote'], width), q['author']))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=os.path.expanduser('~/winequote.txt'))
    args = parser.parse_args()
    print_random_quote(file=args.file)

if __name__ == "__main__":
    main()
