#!/usr/bin/env python3

"""
Module defines class SessionExpAuth
"""

from typing import Optional, Union
from os import getenv
from flask import request
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    A session class with an expiration date that inherits from SessionAuth
    """

    def __init__(self) -> None:
        """instaniates SessionExpAuth object"""
        super().__init__()
        session_duration_str = getenv("SESSION_DURATION", "0")
        try:
            session_duration = int(session_duration_str)
            self.session_duration = session_duration
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: Optional[str]) -> Union[str, None]:
        """
        creates a session with an expiration date

        args:
            user_id (str) default=None : id of user attached to current request

        return:
            None if no current user or session cannot be created
            else session_id (str) if session successfully created
                and updates user_id_by_session_id dict with session_dictionary
                for current user
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
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
        if session_id not in self.user_id_by_session_id.keys():
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id].get("user_id")
        if "created_at" not in self.user_id_by_session_id[session_id].keys():
            return None
        if (
            self.user_id_by_session_id[session_id]["created_at"]
            + timedelta(seconds=self.session_duration)
        ) < datetime.now():
            return None
        return self.user_id_by_session_id[session_id]["user_id"]
