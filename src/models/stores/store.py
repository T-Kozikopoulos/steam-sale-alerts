from uuid import uuid4
from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors


class Store(object):

    def __init__(self, name, url_prefix, tag_name, query, tag_name2, query2, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self.tag_name2 = tag_name2
        self.query2 = query2
        self._id = uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {"_id": self._id,
                "name": self.name,
                "url_prefix": self.url_prefix,
                "tag_name": self.tag_name,
                "query": self.query,
                "tag_name2": self.tag_name2,
                "query2": self.query2}

    def delete(self):
        Database.remove(StoreConstants.COLLECTION, {'_id': self._id})

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"_id": id}))

    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION, {'_id': self._id}, self.json())

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name": store_name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": '{}'.format(url_prefix)}}))

    @classmethod
    def find_by_url(cls, url):
        for i in range(0, len(url) + 1):
            try:
                store = cls.get_by_url_prefix(url[:i])
                return store
            except:
                raise StoreErrors.StoreNotFoundException("The URL Prefix used to find the store didn't give us any results!")
