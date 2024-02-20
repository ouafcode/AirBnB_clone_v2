#!/usr/bin/python3
"""Define DBStorage"""
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class DBStorage:
    """database storage

    Attributes:
        __engine (sqlalchemy.Engine): SQLAlchemy engine.
        __session (sqlalchemy.Session): SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage instance."""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the curret database sessio

        If cls is None, queries all types of objects

        Return:
            return a dictionary.
        """
        if cls is None:
            objct = self.__session.query(State).all()
            objct.extend(self.__session.query(City).all())
            objct.extend(self.__session.query(User).all())
            objct.extend(self.__session.query(Place).all())
            objct.extend(self.__session.query(Review).all())
            objct.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objct = self.__session.query(cls)
        return {"{}.{}".format(type(e).__name__, e.id): e for e in objct}

    def new(self, obj):
        """Add obj to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()
