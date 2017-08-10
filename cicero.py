import datetime

import praw

from announcer import Announcer
from saveload import load_pickle, save_pickle


class Cicero:
    def __init__(self):
        self.date_file = '.last_date.p'
        self.cicero = praw.Reddit('Cicero')
        subreddit = input('Input the name of subreddit: ')
        self.subreddit = self.cicero.subreddit(subreddit)
        self.date = load_pickle(self.date_file)
        self.announcer = Announcer()
        if not self.date:
            self.save_last_date(datetime.datetime.timestamp(datetime.datetime.now()))
        self.monitor_for_posts()

    def monitor_for_posts(self):
        message_template = 'New post in SotS!\n\n' \
                           '[{0}]({1})\n' 
        url_header = 'https://www.reddit.com{}'

        for submission in self.subreddit.stream.submissions():
            if submission.created > self.date:
                self.save_last_date(submission.created)
                announcement = message_template.format(submission.title, submission.url)
                permalink = url_header.format(submission.permalink)
                if permalink != submission.url:
                    announcement += '\n[comments]({})'.format(permalink)
                self.announcer.announce(announcement)

    def save_last_date(self, new_date):
        self.date = new_date
        save_pickle(self.date, self.date_file)


if __name__ == '__main__':
    cicero = Cicero()
