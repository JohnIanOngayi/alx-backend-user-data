#!/usr/bin/env python3
"""
Module defines authentication classes
"""
from typing import List, Optional, Union
from flask import Request
from os import getenv
from models.user import User


class Auth:
    """Authentication Class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns if path requires authentication"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path.endswith("/"):
            path = path[:-1]
        for excluded_path in excluded_paths:
            if excluded_path.endswith("/"):
                excluded_path = excluded_path[:-1]
            if excluded_path.endswith("*"):
                if path.startswith(excluded_path[:-1]):
                    return False
            if path == excluded_path:
                return False
        return True

    def authorization_header(self, request):
        """
        validates all user requests to secure the API

        args:
            request (flask.request) the request

        returns:
            None if Authorization header is non-existent
            else value of Authorization header
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> Union[User, None]:
        """function returns current user attached to session"""
        return None

    def session_cookie(self, request: Optional[Request]) -> Union[str, None]:
        """
        Returns a cookie value from request

        args:
            request (flask.Request): client's request

        return:
            None if request is None or no key _my_session_id
            else (str) cookie value
        """
        session = getenv("SESSION_NAME")
        if not request or not session:
            return None
        return request.cookies.get(session)
