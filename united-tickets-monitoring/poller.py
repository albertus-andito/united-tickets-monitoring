import logging.config
import os
import schedule
import time

from dotenv import load_dotenv

from definitions import ROOT_DIR, LOGGER_CONFIG_PATH
from database import Database
from reddit_api import RedditAPI


class Poller:

    def __init__(self):
        load_dotenv()

        logfile_path = os.path.join(ROOT_DIR, 'logs', 'poller.log').replace("\\", "/")
        os.makedirs(os.path.dirname(logfile_path), exist_ok=True)
        logging.config.fileConfig(LOGGER_CONFIG_PATH,
                                  defaults={'logfilename': logfile_path},
                                  disable_existing_loggers=False)

        self.database = Database()
        self.logger = logging.getLogger()

    def start(self):
        self.logger.info('Starting poller...')
        reddit = RedditAPI(os.getenv('REDDIT_CLIENT_ID'), os.getenv('REDDIT_CLIENT_SECRET'),
                           os.getenv('REDDIT_USER_AGENT'), self.database)
        reddit.search(mode='new')
        schedule.every().minute.do(reddit.search)

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    poller = Poller()
    poller.start()
