from modules.config import Config
from modules.meilisearch_helper import MeiliSearchHelper

"""
todo: use a database interface instead for this and code everything to that interface, then rename this class to Redis
What is this database supposed to do?
store metadata while making sure searching is blazing fast
searching will be like:
search_term given
this should be searched as a wildcard, kind of like a fuzzy searching algorithm


"""


class Database:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.client = MeiliSearchHelper(config)
