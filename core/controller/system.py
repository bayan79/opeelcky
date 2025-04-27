from typing import List, Dict, Optional

import pydantic
from pydantic import BaseModel, Field

from database.db import mongo_db
from database.entity import DBKeyEntity
from exceptions.crud import NotFound, AlreadyExists


class SystemSchema(BaseModel):
    name: str
    config: dict


class SystemModel(DBKeyEntity):
    @classmethod
    def get_mongo_collection(cls):
        return SystemController.db

    @classmethod
    def get_key(cls) -> str:
        return 'name'


class SystemController:
    db = mongo_db['systems']

    def __init__(self, model: Optional[SystemModel]):
        self.model = model

    @property
    def system(self):
        return self.model[self.model.get_key()]

    @property
    def config(self):
        return self.model['config']

    @classmethod
    def load(cls, system: str):
        return SystemController(SystemModel.load_by_key(system))

    def save(self):
        self.model.save()

    @classmethod
    def create(cls, system: str, config: dict):
        try:
            SystemModel.load_by_key(system)
            raise AlreadyExists
        except NotFound:
            SystemModel({'name': system, 'config': config}).save()
        return SystemController.load(system)

    @classmethod
    def list_systems(cls) -> Dict[str, 'SystemController']:
        return {
            i['name']: cls(SystemModel(i))
            for i in cls.db.find()
        }


SystemController.db.create_index('name', unique=True)
