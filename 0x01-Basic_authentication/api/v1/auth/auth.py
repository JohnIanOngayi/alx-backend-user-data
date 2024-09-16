#!/usr/bin/env python3
"""
Module defines authentication classes
"""
import flask
from typing import List, Optional, TypeVar, Union


# Task 3 Class
class Auth:
    """Authentication Class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """function"""
        return False

    def authorization_header(self, request=None) -> Union[str, None]:
        """function"""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """function"""
        return None
