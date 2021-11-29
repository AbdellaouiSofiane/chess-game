from abc import ABC
from dataclasses import dataclass, field
from dataclass_factory import Factory
from tinydb import TinyDB
from tinydb.table import Document

from settings import DATABASE_NAME


db = TinyDB(DATABASE_NAME)


@dataclass
class BaseModel(ABC):
    """ Abstract class for handling database operations. """
    id: int = field(default=None, init=False, repr=True)

    @classmethod
    def _table(cls):
        """ Return the model's database table. """
        return db.table(cls.__name__.lower())

    @classmethod
    def get(cls, id):
        """ Return model's instance from database by its id"""
        data = cls._table().get(doc_id=id)
        if data:
            instance = Factory().load(data, cls) # get_object from data
            instance.id = id
            return instance
        return None

    @classmethod
    def all(cls):
        """ get all objects from database"""
        return [cls.get(id=entry.doc_id) for entry in cls._table().all()]

    @property
    def dict(self):
        """ Return model's attributes as dict"""
        return Factory().dump(self)

    def save(self):
        """ Create a new database entry or update an existing one"""
        if self.id:
            self._table().upsert(Document(self.dict, doc_id=self.id))
        else:
            self.id = self._table().insert(self.dict)
        return self
