from exceptions.crud import NotFound


class DBEntity(dict):
    @classmethod
    def get_mongo_collection(cls):
        raise NotImplementedError

    @classmethod
    def load_by_id(cls, _id: str):
        result = cls.get_mongo_collection().find_one({'_id': _id})
        if result is None:
            raise NotFound
        return cls(result)

    def save_by_id(self):
        self.get_mongo_collection().update_one({'_id': self["_id"]}, {'$set': self}, upsert=True)


class DBKeyEntity(DBEntity):
    @classmethod
    def get_mongo_collection(cls):
        raise NotImplementedError

    @classmethod
    def get_key(cls) -> str:
        raise NotImplementedError

    @classmethod
    def load_by_key(cls, key: str):
        result = cls.get_mongo_collection().find_one({cls.get_key(): key})
        if result is None:
            raise NotFound
        return cls(result)

    def save(self):
        self.get_mongo_collection().update_one({self.get_key(): self[self.get_key()]}, {'$set': self}, upsert=True)
