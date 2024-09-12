#!/usr/bin/env python3
"""module secures passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a pwd"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(str.encode(password), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks if pwd is valid"""
    return bcrypt.checkpw(str.encode(password), hashed_password)
