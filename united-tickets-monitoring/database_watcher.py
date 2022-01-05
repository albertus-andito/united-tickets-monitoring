import logging.config
import os
import pymongo

from dotenv import load_dotenv

from definitions import ROOT_DIR, LOGGER_CONFIG_PATH
from database import Database
from mail_sender import MailSender


class DatabaseWatcher:

    LOGFILE_PATH = os.path.join(ROOT_DIR, 'logs', 'database-watcher.log').replace("\\", "/")
    os.makedirs(os.path.dirname(LOGFILE_PATH), exist_ok=True)
    logging.config.fileConfig(LOGGER_CONFIG_PATH,
                              defaults={'logfilename': LOGFILE_PATH},
                              disable_existing_loggers=False)

    def __init__(self):
        load_dotenv()

        self.logger = logging.getLogger()

        self.mail_service = MailSender()
        self.database = Database()
        self.mail_to = os.getenv('MAIL_TO')

    def watch(self):
        self.logger.info('Starting database watcher...')
        try:
            with self.database.submissions.watch([{'$match': {'operationType': 'insert'}}]) as stream:
                for insert_change in stream:
                    self.mail_service.send_instant_notification(self.mail_to, insert_change['fullDocument'])
                    self.logger.info('Sent mail to %s for submission: %s',
                                     self.mail_to, insert_change['fullDocument']['url'])
        except pymongo.errors.PyMongoError as e:
            self.logger.error(e)


if __name__ == '__main__':
    watcher = DatabaseWatcher()
    watcher.watch()
