from pymongo import MongoClient
from pymongo.read_concern import ReadConcern


class Database:

    def __init__(self, host="localhost", port=27017, replica_set='rs0'):
        client = MongoClient(host=host, port=port, replicaSet=replica_set)
        database = client.get_database('united-tickets-monitoring')
        self.submissions = database.get_collection('submissions', read_concern=ReadConcern('majority'))
        self.submissions.create_index('url', unique=True)

    def find_submission(self, url):
        return self.submissions.find_one({'url': url})

    def insert_submission(self, title, content, platform, channel, author, url, submission_date):
        self.submissions.insert_one({
            'title': title,
            'content': content,
            'platform': platform,
            'channel': channel,
            'author': author,
            'url': url,
            'submission_date': submission_date
        })
