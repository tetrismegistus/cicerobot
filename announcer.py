import sys

import telepot
from telepot.loop import MessageLoop

from saveload import load_pickle, save_pickle


class Announcer:
    def __init__(self):
        token = self.load_token()
        self.chat_ids_file = '.chat_ids.p'
        self.bot = telepot.Bot(token)
        self.chat_ids = load_pickle(self.chat_ids_file)
        if not self.chat_ids:
            self.chat_ids = []

        MessageLoop(self.bot, self.check_chat_id).run_as_thread()

    def load_token(self):
        token_file = '.token.p'
        token = load_pickle(token_file)
        while not token:
            token = input('Please enter your telegram api token: ')
            save_pickle(token, token_file)
        return token

    def check_chat_id(self, message):
        content_type, chat_type, chat_id = telepot.glance(message)
        if chat_id not in self.chat_ids:
            print('Adding chat_id {}'.format(chat_id))
            self.add_chat_id(chat_id)

    def add_chat_id(self, chat_id):
        self.chat_ids.append(chat_id)
        save_pickle(self.chat_ids, self.chat_ids_file)

    def announce(self, message):
        for chat_id in self.chat_ids:
            self.bot.sendMessage(chat_id, message,parse_mode='Markdown')
