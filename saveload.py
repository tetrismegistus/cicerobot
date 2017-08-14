import pickle
import logging

def save_pickle(data, filename):
    with open(filename, 'wb') as f:
        logging.info('updating file {}'.format(filename))
        pickle.dump(data, f)


def load_pickle(filename):
    try:
        with open(filename, 'rb') as f:
            logging.info('loading file {}'.format(filename))
            return pickle.load(f)
    except FileNotFoundError:
        logging.warn('File not found {}'.format(filename))
        return False

