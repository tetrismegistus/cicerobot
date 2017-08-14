import sys
import logging

import telepot
from telepot.loop import MessageLoop

from saveload import load_pickle, save_pickle


class Announcer:
    def __init__(self):
        token = self.load_token()
        self.bot = telepot.Bot(token)
        logging.info('started bot with token {0}'.format(token))
        
        self.chat_ids_file = '.chat_ids.p'
        self.chat_ids = load_pickle(self.chat_ids_file)        
        
        if not self.chat_ids:
            logging.warning('file {0} does not exist, initializing self.chat_ids with a blank list'.format(self.chat_ids_file))
            self.chat_ids = []

        logging.info('monitoring for new chat_ids')
        MessageLoop(self.bot, self.check_chat_id).run_as_thread()

    def load_token(self):
        token_file = '.token.p'
        token = load_pickle(token_file)
        while not token:
            logging.warning('token file {0} does not exist'.format(token_file))
            token = input('Please enter your telegram api token: ')
            save_pickle(token, token_file)
            logging.warning('created token file {0}'.format(token_file))
        return token

    def check_chat_id(self, message):
        content_type, chat_type, chat_id = telepot.glance(message)
        if chat_id not in self.chat_ids:
            self.add_chat_id(chat_id)

    def add_chat_id(self, chat_id):
        self.chat_ids.append(chat_id)
        logging.info('Appended chat_id {0}'.format(chat_id))
        save_pickle(self.chat_ids, self.chat_ids_file)

    def remove_chat_id(self, chat_id):
        self.chat_ids.remove(chat_id)
        logging.info('Removed chat_id {0}'.format(chat_id))
        save_pickle(self.chat_ids, self.chat_ids_file)


    def announce(self, message):        
        for chat_id in self.chat_ids:
            logging.info('Announcing {}'.format(message))
            try:
                self.bot.sendMessage(chat_id, message,parse_mode='Markdown')
                logging.info('Announced to chat_id {}'.format(chat_id))
            except (telepot.exception.BotWasBlockedError,
                    telepot.exception.BotWasKickedError ) as e:
                logging.warning('Bot was kicked or blocked from {}'.format(chat_id))
                self.remove_chat_id(chat_id)

