from modules.config import Config
from modules.meilisearch_helper import MeiliSearchHelper

"""
TODO: use a database interface instead for this and code everything to that interface. concrete class can inherit this interface instead of initializing it's object in this class
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

    def upsert_documents(self, documents: list[dict], primary_key: str) -> None:
        self.client.upsert_documents(documents, primary_key=primary_key)

    def search(self, key: str):
        return self.client.search(key)

    def close(self):
        self.client.close()
