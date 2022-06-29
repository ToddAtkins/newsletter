#!/usr/bin/env python
import argparse
import configparser
import datetime
from email.message import EmailMessage
import os
import re
import smtplib
import publish.pubcalendar
import publish.pubtwitter
import publish.pubquote
from pprint import pprint

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', '-c', type=str, metavar='newsletter_config_filename', default=os.path.expanduser('~/.newsletter.ini'))
    parser.add_argument('--happenings-note', '--events-note', type=str, default='')
    parser.add_argument('--ignore-tweets', action="store_true")
    parser.add_argument('--no-tls', action='store_true', default=False)
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    config = configparser.RawConfigParser()
    config.read(args.conf)
    calcfg = dict(config.items('calendar'))
    pubcfg = dict(config.items('publish'))
    quotcfg = dict(config.items('quotes'))
    twitcfg = dict(config.items('twitter'))

    separator = '+'*24
    subject = '{title} : {date}'.format(title=pubcfg['title'],
                                        date=datetime.date.today().strftime(pubcfg['date_format']))
    happenings = publish.pubcalendar.format_events(
                    events=publish.pubcalendar.get_events(
                                calcfg['url'],
                                int(calcfg['days_to_show'])),
                    separator=separator,
                    date_format=calcfg['date_format'],
                    note=args.happenings_note
                    )

    quote = publish.pubquote.random_quote(os.path.expanduser(quotcfg['file']))
    footer = pubcfg['footer']

    # build the newsletter
    newsletter = separator + '\n'
    if len(happenings):
        newsletter += 'Happenings\n'
        newsletter += separator + '\n'
        newsletter += happenings

    if not args.ignore_tweets:
        api = publish.pubtwitter.login(
                  consumer_key=twitcfg['consumer_key'],
                  consumer_secret=twitcfg['consumer_secret'],
                  access_token_key=twitcfg['access_token_key'],
                  access_token_secret=twitcfg['access_token_secret'])
        twitter_bookmark = publish.pubtwitter.get_bookmark(os.path.expanduser(twitcfg['bookmark_file']))
        statuses = api.GetUserTimeline(since_id=twitter_bookmark)

        sid = 0
        if len(statuses):
            newsletter += 'News and other Nonsense' + '\n'
            newsletter += separator + '\n\n'
            for s in statuses:
                if sid == 0:
                    sid = s.id
                txt = re.sub(r'^RT[^:]*:\s*', '', s.text)
                txt = re.sub(r' #winoinfo.*', '', txt)
                txt = re.sub(r' #winoinfo.*', '', txt)
                txt = re.sub(r'#', '', txt)
                newsletter += '{0}\n\n'.format(txt)
            newsletter += separator + '\n'

    newsletter += "{0}\n- {1}\n".format(quote['quote'], quote['author'])
    newsletter += separator + '\n\n'
    newsletter += footer + '\n'

    msg = EmailMessage()
    msg.set_content(newsletter)
    msg['Subject'] = subject
    msg['From'] = pubcfg['from']
    msg['To'] = pubcfg['to']
    #print(msg)
    print(msg.as_string())
    ans = input('Send out this newsletter? ')

    if ans == 'yes':
        if args.no_tls:
            mailer = smtplib.SMTP(pubcfg['smtp_server'])
        else:
            if args.verbose:
                print(pubcfg['smtp_server'])
            if 'smtp_port' in pubcfg:
                mailer = smtplib.SMTP(pubcfg['smtp_server'], pubcfg['smtp_port'])
            else:
                mailer = smtplib.SMTP(pubcfg['smtp_server'], 587)
            mailer.ehlo()
            mailer.starttls()
            if 'smtp_user' not in pubcfg:
                pubcfg['smtp_user'] = raw_input('username for %s smtp server? ' % pubcfg['smtp_server'])
            if 'smtp_password' not in pubcfg:
                pubcfg['smtp_password'] = getpass('password for %s smtp server? ' % pubcfg['smtp_server'])
            mailer.login(pubcfg['smtp_user'], pubcfg['smtp_password'])

        mailer.sendmail(pubcfg['from'], [pubcfg['to']], msg.__str__())
        mailer.quit()

        if sid:
            print('The first Twitter status ID used is {}'.format(twitter_bookmark))
            print('The latest Twitter status ID published is {}'.format(sid))
            ans = input('Update ID in {}? '.format(twitcfg['bookmark_file']))
            if ans == 'yes':
                publish.pubtwitter.save_bookmark(os.path.expanduser(twitcfg['bookmark_file']), sid)

if __name__ == '__main__':
    main()
