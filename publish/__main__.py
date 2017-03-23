#!/usr/bin/env python
import argparse
from mycalendar import get_events, format_events
import ConfigParser
import datetime
from email.mime.text import MIMEText
import os
import re
import smtplib
import mytwitter
import twitter
from quote import random_quote

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', '-c', type=str, metavar='newsletter_config_filename', default=os.path.expanduser('~/.newsletter.ini'))
    parser.add_argument('--ignore-tweets', action="store_true")
    parser.add_argument('--no-tls', action='store_true', default=False)
    args = parser.parse_args()
     
    config = ConfigParser.ConfigParser()
    config.readfp(open(args.conf))
    calcfg = dict(config.items('calendar'))
    pubcfg = dict(config.items('publish'))
    quotcfg = dict(config.items('quotes'))
    twitcfg = dict(config.items('twitter'))
    
    separator = '+'*24
    subject = '{title} : {date}'.format(title=pubcfg['title'], 
                                        date=datetime.date.today().strftime(pubcfg['date_format']))
    quote = random_quote(os.path.expanduser(quotcfg['file']))
    footer = pubcfg['footer']
    
    # build the newsletter
    newsletter = separator + '\n'
    newsletter += 'Happenings\n'
    newsletter += separator + '\n'
    newsletter += format_events(events=get_events(calcfg['url'], int(calcfg['days_to_show'])), 
                                separator=separator,
                                date_format=calcfg['date_format'])
    
    if args.no_tls:
        mailer = smtplib.SMTP(pubcfg['smtp_server'])
    else:
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

    if not args.ignore_tweets:
        api = mytwitter.login(consumer_key=twitcfg['consumer_key'],
                              consumer_secret=twitcfg['consumer_secret'],
                              access_token_key=twitcfg['access_token_key'],
                              access_token_secret=twitcfg['access_token_secret'])
        twitter_bookmark = mytwitter.get_bookmark(os.path.expanduser(twitcfg['bookmark_file']))
        statuses = api.GetUserTimeline(since_id=twitter_bookmark)
    
        sid = 0
        if len(statuses):
            newsletter += 'News and other Nonsense' + '\n'
            newsletter += separator + '\n\n'
            for s in statuses:
                if sid == 0:
                    sid = s.id
                txt = re.sub(r' #winoinfo.*', '', s.text)
                txt = re.sub(r'#', '', txt)
                newsletter += txt.encode('utf-8') + '\n\n'
            
    newsletter += separator + '\n'
    newsletter += "{0}\n- {1}\n".format(quote['quote'], quote['author'])
    newsletter += separator + '\n\n'
    newsletter += footer + '\n'
    
    msg = MIMEText(newsletter)
    msg['Subject'] = subject
    msg['From'] = pubcfg['from']
    msg['To'] = pubcfg['to']
    print msg.as_string()
    ans = raw_input('Send out this newsletter? ')
    if ans == 'yes':
        mailer.sendmail(pubcfg['from'], [pubcfg['to']], msg.as_string())
        mailer.quit()
        
        if sid:
            print 'The latest Twitter status ID published is {}'.format(sid)
            ans = raw_input('Update ID in {}? '.format(twitcfg['bookmark_file']))
            if ans == 'yes':
                mytwitter.save_bookmark(os.path.expanduser(twitcfg['bookmark_file']), sid)
                
if __name__ == '__main__':
    main()
