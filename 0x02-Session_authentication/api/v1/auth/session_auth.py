#!/usr/bin/env python3

"""
Module defines class SessionAuth that inherits from Auth
"""

from typing import Dict, Optional, Union

from api.v1.auth.auth import Auth
import uuid

from models.user import User


class SessionAuth(Auth):
    """
    Class for Session Authentication
    """

    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: Optional[str]) -> Union[str, None]:
        """
        Creates a Session id for a user_id

        args:
            user_id (str): user id starting session

        return:
            None if user_id is None or user_id not str
            else session_id (str) stringified uuid.UUID obj
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: Optional[str]):
        """
        Returns user_id based on a session_id

        args:
            session_id (str): Session id in question

        returns:
            None if session_id is None or session_id is not str
            else (str) the user_id attached to the session
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> Union[User, None]:
        """
        returns User instance based on cookie value

        args:
            request (flask.Request): client's request

        returns:
            user (User) attached to current session
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id:
            return User.get(user_id)
        else:
            return None

    def destroy_session(self, request=None) -> bool:
        """
        Destroys session
        """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del SessionAuth.user_id_by_session_id[session_id]
        return True
