import logging
import praw

from datetime import datetime

from database import Database


class RedditAPI:

    def __init__(self, client_id: str, client_secret: str, user_agent: str, database: Database,
                 subreddits: list = None,
                 query: str = 'ticket'):
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

    def search(self, mode='search', time_filter='day', limit=100):
        if mode == 'search':
            submissions = self.reddit.subreddit(self.subreddits).search(query=self.query, sort="new",
                                                                        syntax='lucene', time_filter=time_filter)
        else:
            submissions = self.reddit.subreddit(self.subreddits).new(limit=limit)
            submissions = [submission for submission in submissions
                           if self.query.casefold() in submission.title.casefold() or
                           self.query.casefold() in submission.selftext.casefold()]
        for submission in submissions:
            try:
                if self.database.find_submission(submission.url) is None:
                    self.database.insert_submission(submission.title, submission.selftext, 'Reddit',
                                                    submission.subreddit.display_name, submission.author.name,
                                                    submission.url, datetime.fromtimestamp(submission.created_utc)
                                                    )
                    self.logger.info('Inserted Reddit submission: %s', submission.url)
            except Exception as e:
                self.logger.error(e)
