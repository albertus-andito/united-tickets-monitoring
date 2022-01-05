import logging
import praw

from datetime import datetime

from database import Database


class RedditAPI:

    def __init__(self, client_id: str, client_secret: str, user_agent: str, database: Database,
                 subreddits: list = None,
                 query: str = "ticket OR tickets"):
        if subreddits is None:
            subreddits = ["reddevils", "ManchesterUnited"]
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        self.subreddits = "+".join(subreddits)
        self.query = query
        self.database = database

        self.logger = logging.getLogger()

    def search(self, time_filter="day"):
        for submission in self.reddit.subreddit(self.subreddits).search(query=self.query, sort="new",
                                                                        time_filter=time_filter):
            try:
                if self.database.find_submission(submission.url) is None:
                    self.database.insert_submission(submission.title, submission.selftext, 'Reddit',
                                                    submission.subreddit.display_name, submission.author.name,
                                                    submission.url, datetime.fromtimestamp(submission.created_utc)
                                                    )
                    self.logger.info('Inserted Reddit submission: %s', submission.url)
            except Exception as e:
                self.logger.error(e)
