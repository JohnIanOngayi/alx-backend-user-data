#!/usr/bin/env python3

"""Moduke defines a class BasicAuth"""

from typing import Any, Optional, TypeVar, Union

from flask import Request
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User


class BasicAuth(Auth):
    """class inherits from class Auth"""

    def extract_base64_authorization_header(
        self, authorization_header: Union[str, Any]
    ) -> Union[str, None]:
        """
        returns the Base64 part of the Authorization header
        for a Basic Authentication

        args:
            authorization_header (str): the value of the Authorization header

        returns:
            value of authorization_header or None
        """

        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith("Basic ")
        ):
            return None
        return authorization_header.split("Basic ")[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: Union[str, Any]
    ) -> Union[str, None]:
        """
        returns the decoded value of a Base64 string

        args:
           base64_authorization_header (str | None): encoded header

        returns:
            decoded string or None
        """
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None
        try:
            return b64decode(base64_authorization_header).decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> tuple:
        """
        returns user email and password from the Base64 decoded value

        args:
            decoded_base64_authorization_header (str): decoded authheader value

        returns:
            (none, none) if decoded_base64_authorization_header is None
            (none, none) if decoded_base64_authorization_header is not a string
            (none, none) if : not in decoded_base64_authorization_header
            else (email, password)
        """
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or decoded_base64_authorization_header.find(":") == -1
        ):
            return (None, None)
        else:
            return tuple(decoded_base64_authorization_header.split(":"))

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> Union[User, None]:
        """
        returns the User instance based on his email and password

        args:
            user_email (str): user's email
            user_pwd (str): user's password

        returns:
            None or User object if both user_email and user_pwd match
        """
        if (
            not user_email
            or not user_pwd
            or not isinstance(user_email, str)
            or not isinstance(user_pwd, str)
        ):
            return None
        users = User.search({"email": user_email})
        if (
            not users
            or len(users) == 0
            or not users[0]
            or not users[0].is_valid_password(user_pwd)
        ):
            return None
        return users[0]

    def current_user(self, request: Optional[Request]) -> TypeVar("User"):
        """
        Overloads Auth and retrieves User instance for the request

        args:
            request (Request): current flask.Request object

        returns:
            (User): user instance attached to request
        """
        authorization_header = self.authorization_header(request)
        if not authorization_header:
            return
        base64_authorization_header = self.extract_base64_authorization_header(
            authorization_header
        )
        if not base64_authorization_header:
            return
        decoded_base64_authorization_header = self.decode_base64_authorization_header(
            base64_authorization_header
        )
        if not decoded_base64_authorization_header:
            return
        user_credentials = self.extract_user_credentials(
            decoded_base64_authorization_header
        )
        if user_credentials == (None, None):
            return
        return self.user_object_from_credentials(
            user_credentials[0], user_credentials[1]
        )
