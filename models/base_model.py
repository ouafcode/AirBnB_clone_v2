#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DATETIME
from models import storage_type


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models

    Attribute:
        id (sqlalchemy String): The BaseModel id.
        created_at (sqlalchemy DateTime): The creation datetime
        updated_at (sqlalchemy DateTime): The updated datetime
    """
    id = Column(String(60),
                nullable=False,
                primary_key=True,
                unique=True)
    created_at = Column(DATETIME,
                        nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DATETIME,
                        nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for kw in kwargs:
                if kw in ['created_at', 'updated_at']:
                    setattr(self, kw, datetime.fromisoformat(kwargs[kw]))
                elif kw != '__class__':
                    setattr(self, kw, kwargs[kw])
            if storage_type == 'db':
                if not hasattr(kwargs, 'id'):
                    setattr(self, 'id', str(uuid.uuid4()))
                if not hasattr(kwargs, 'created_at'):
                    setattr(self, 'created_at', datetime.now())
                if not hasattr(kwargs, 'updated_at'):
                    setattr(self, 'updated_at', datetime.now())

    def __str__(self):
        """Returns a string representation of the instance"""
        return '[{}] ({}) {}'.format(
             self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dcty = self.__dict__.copy()
        dcty['__class__'] = self.__class__.__name__
        for kw in dcty:
            if type(dcty[kw]) is datetime:
                dcty[kw] = dcty[kw].isoformat()
        if '_sa_instance_state' in dcty.keys():
            del(dcty['_sa_instance_state'])
        return dcty

    def delete(self):
        '''deletes instance from storage'''
        from models import storage
        storage.delete(self)
