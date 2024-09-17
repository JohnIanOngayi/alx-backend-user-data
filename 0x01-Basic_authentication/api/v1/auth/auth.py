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
        if path and not path.endswith("/"):
            path += "/"
        if (
            path is None
            or excluded_paths is None
            or len(excluded_paths) == 0
            or path not in excluded_paths
        ):
            return True
        return False

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
