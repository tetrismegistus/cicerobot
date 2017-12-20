import datetime
import logging

import praw
ipmort prawcore

from announcer import Announcer
from saveload import load_pickle, save_pickle
from logconfig import setup_logger

class Cicero:
    def __init__(self):
        self.date_file = '.last_date.p'
        self.cicero = praw.Reddit('Cicero')
        
        subreddit = input('Input the name of subreddit: ')
        self.subreddit = self.cicero.subreddit(subreddit)
        logging.info('Setting subreddit to {}'.format(subreddit))
        
        self.date = load_pickle(self.date_file)
        
        if not self.date:
            now = datetime.datetime.now()
            self.save_last_date(datetime.datetime.timestamp(now))        
        
        self.announcer = Announcer()
        self.monitor_for_posts()

    def monitor_for_posts(self):
        message_template = 'New in SotS: [{0}]({1})\n' 
        url_header = 'https://www.reddit.com{}'
        
        logging.info('Monitoring subreddit for new posts')

        try:
            for submission in self.subreddit.stream.submissions():
                if submission.created > self.date:
                    self.save_last_date(submission.created)
                    announcement = message_template.format(submission.title, submission.url)
                    permalink = url_header.format(submission.permalink)
                    if permalink != submission.url:
                        announcement += '\n[comments]({})'.format(permalink)
                    self.announcer.announce(announcement)
        except PrawcoreException as e: 
            logging.error('Error: {}'.format(e))    

    def save_last_date(self, new_date):
        self.date = new_date
        save_pickle(self.date, self.date_file)


if __name__ == '__main__':
    setup_logger('cicero')
    cicero = Cicero()
