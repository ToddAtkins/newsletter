#!/usr/bin/env python
from icalendar import Calendar, vDatetime
import datetime
from operator import itemgetter
import urllib
import pytz
import tzlocal

def get_events(ical_url, days=7):
    today = datetime.date.today()
    max_date = today + datetime.timedelta(days)
    ltz = tzlocal.get_localzone()
    events = []
    ics = urllib.urlopen(ical_url).read()
    ical=Calendar.from_ical(ics)
    
    for e in ical.walk():
        if 'SUMMARY' in e and 'DTSTART' in e:
            event = { 
                'title': str(e['SUMMARY'].encode('utf-8')),
                'location': str(e['LOCATION'].encode('utf-8')),            
                'description': str(e['DESCRIPTION'].encode('utf-8')),
            }
            
            if type(e['DTSTART'].dt) is datetime.datetime:
                event['start'] = e['DTSTART'].dt.replace(tzinfo=pytz.utc)
                event['date'] = event['start'].astimezone(ltz).date()
            else:
                event['start'] = e['DTSTART'].dt
                event['date'] = event['start']
            
            if 'DTEND' in e:
                if type(e['DTEND'].dt) is datetime.datetime:
                    event['end'] = e['DTEND'].dt.replace(tzinfo=pytz.utc)
                else:
                    event['end'] = e['DTEND'].dt
            
            if today <= event['date'] and event['date'] <= max_date:
                events.append(event)
                
    return(sorted(events, key=itemgetter('date')))
    
def format_events(events, separator = '+'*24, date_format='%a %b %e, %Y at %I:%M %p'):
    ltz = tzlocal.get_localzone()
    event_text = ''
    for event in events:
        event_text += '\n{0}\n\n'.format(event['title'])
        
        if type(event['start']) is datetime.datetime:
            start = event['start'].astimezone(ltz).strftime(date_format)
        else:
            start = event['start'].strftime(date_format)
            
        if 'end' in event:
            if type(event['end']) is datetime.datetime:
                end = event['end'].astimezone(ltz).strftime(date_format)
            else:
                end = event['end'].strftime(date_format)
            event_text += 'When: {0} to {1}\n'.format(start, end)
        else:
            event_text += 'When: {0}\n'.format(start)
            
        event_text += 'Where: {0}\n'.format(event['location'])
        event_text += 'Why:\n\n{0}\n'.format(event['description'])
        event_text += '\n{0}\n'.format(separator)
        
    return event_text

if __name__ == '__main__':
    events = get_events()
    print(format_events(events))
    