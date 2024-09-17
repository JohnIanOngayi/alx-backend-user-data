#!/usr/bin/env python3
"""
Module defines authentication classes
"""
from typing import List
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

    def current_user(self, request=None) -> User:
        """function returns current user attached to session"""
        return None
