import re
import requests
from uuid import uuid4
from bs4 import BeautifulSoup
from src.common.database import Database
import src.models.items.constants as ItemConstants
from src.models.stores.store import Store


class Item(object):

    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.tag_name2 = store.tag_name2
        self.query2 = store.query2
        self.price = None if price is None else price
        self._id = uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        try:
            element = soup.find(self.tag_name, self.query)
        except:
            element = soup.find(self.tag_name2, self.query2)
        string_price = element.text.strip()
        pattern = re.compile("([0-9]{1,2}([,.][0-9]{1,2}))")
        match = pattern.search(string_price)
        match = match.group().replace(',', '.')
        self.price = float(match)

        return self.price

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {"_id": self._id,
                "name": self.name,
                "url": self.url,
                "price": self.price}

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))
