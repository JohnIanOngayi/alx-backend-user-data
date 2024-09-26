#!/usr/bin/env python3

"""
Module defines class Auth
"""
from uuid import uuid4
import bcrypt
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Instaniates an Auth object"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[User, None]:
        """Registers User object into the database"""
        user_kwargs = {"email": email}
        if not email:
            raise ValueError("email missing")
        if not password:
            raise ValueError("password missing")
        try:
            self._db.find_user_by(**user_kwargs)
        except Exception:
            pass
        else:
            raise ValueError(f"User {email} already exists")
        hashed_password = _hash_password(password)
        if hashed_password:
            return self._db.add_user(email, hashed_password.decode())
        return None

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login for a user"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        return _is_valid(user.hashed_password.encode(), password)

    def create_session(self, email: str) -> Union[str, None]:
        """creates session for attached user"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        if user:
            session_id = str(_generate_uuid())
            self._db.update_user(user_id=user.id, session_id=session_id)
            return session_id
        return None

    def get_reset_password_token(self, email: str) -> Union[str, None]:
        """Generates and updates User password reset token"""
        if not email or not isinstance(email, str):
            return None
        try:
            user = self._db.find_user_by(email=email)
        except ValueError:
            raise ValueError(f"User with email {email} doesn't exist")
        password_token = _generate_uuid()
        token_dict = {"password_token": password_token}
        self._db.update_user(user.id, **token_dict)
        return password_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Verifies reset password token and updates password"""
        if not password or len(password) == 0 or not isinstance(password, str):
            raise ValueError
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        # update password and delete reset_token
        hashed_password_dict = {
            "hashed_password": _hash_password(password),
            "reset_token": None,
        }
        self._db.update_user(user.id, **hashed_password_dict)
        return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """finds a User by session_id"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """destroys current session"""
        try:
            self._db.find_user_by(user_id=user_id)
        except NoResultFound:
            raise ValueError("user_id not found")
        return self._db.update_user(user_id=user_id, session_id=None)


def _hash_password(password: str) -> Union[bytes, None]:
    """hashes a password"""
    if not password or len(password) == 0:
        return None
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _is_valid(hashed_password: bytes, password: str) -> bool:
    """validates password"""
    return bcrypt.checkpw(password.encode(), hashed_password)


def _generate_uuid() -> str:
    """return uuid's"""
    return str(uuid4())
