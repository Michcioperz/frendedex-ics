import feedparser
from icalendar import Calendar, Event
from datetime import datetime, timezone
#from flask import Flask, Response
#import schedule
import os
import email.utils

#app = Flask(__name__)

def dbg(x):
    print(x)
    return x

def retrieve_calendar_data(rss_feed_url):
    # Parse the RSS feed
    feed = feedparser.parse(rss_feed_url)
    
    events = []
    for entry in feed.entries:
        event = {}
        event['title'] = "frendedex event" #entry.summary #entry.title
        event['description'] = entry.summary
        event['start_time'] = email.utils.parsedate_to_datetime(entry.published)
        event['end_time'] = email.utils.parsedate_to_datetime(entry.published)  # You might need to adjust this based on your RSS feed structure
        events.append(event)
    
    return events

def generate_ics_feed(events):
    cal = Calendar()
    cal.add('prodid', '-//My Calendar//example.com//')
    cal.add('version', '2.0')

    for event in events:
        ical_event = Event()
        ical_event.add('summary', event['title'])
        ical_event.add('description', event['description'])
        ical_event.add('dtstart', event['start_time'])
        ical_event.add('dtend', event['end_time'])
        cal.add_component(ical_event)

    return cal.to_ical()

def update_ics_feed():
    rss_feed_url = os.getenv("FEED_URL", "https://mastodon.social/tags/rsstoicstesttag.rss")  # Replace with your actual RSS feed URL
    events = retrieve_calendar_data(rss_feed_url)
    ics_feed = generate_ics_feed(events)

    with open("calendar.ics", "wb") as f:
        f.write(ics_feed)

#@app.route('/calendar.ics')
#def serve_ics_feed():
#    with open("calendar.ics", "rb") as f:
#        ics_feed = f.read()
#
#    return Response(ics_feed, mimetype='text/calendar')

if __name__ == "__main__":
    update_ics_feed()  # Initial update
    #schedule.every().hour.do(update_ics_feed)  # Schedule update every hour

    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)
