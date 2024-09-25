#!/usr/bin/env python3
"""DB module
"""
from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError

# from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Saves User with email and hashed_password to database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> Union[User, None]:
        """returns the first row found in the users table as
        filtered by the method’s input arguments"""
        if kwargs is None or len(kwargs) == 0:
            raise InvalidRequestError("Search parameters required")
        if not set(kwargs.keys()).issubset(set(User.__dict__.keys())):
            raise InvalidRequestError("Invalid parameters passed")
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound("No user found with peovided parameters")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates user matching user_id with kwargs"""
        try:
            user_kwargs = {"user_id": user_id}
            user = self.find_user_by(**user_kwargs)
        except Exception:
            return None
        if user:
            user.update(kwargs, synchronize_session=False)
        self._session.commit()
        return None
