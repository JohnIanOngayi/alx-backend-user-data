#!/usr/bin/env python3
"""
Module defines authentication classes
"""
import flask
from typing import List, Optional, TypeVar, Union


# Task 3 Class
# class Auth:
#     """Authentication Class"""
#
#     def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
#         """function"""
#         return False
#
#     def authorization_header(self, request=None) -> str:
#         """function"""
#         return None
#
#     def current_user(self, request=None) -> TypeVar("User"):
#         """function"""
#         return None


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

    def authorization_header(
        self, request: Optional[flask.Request]
    ) -> Union[str, None]:
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

    def current_user(self, request: Optional[flask.Request]) -> TypeVar("User"):
        """function"""
        return None
