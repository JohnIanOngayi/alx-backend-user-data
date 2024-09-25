#!/usr/bin/env python3

"""
Module defines class User
"""
from typing import Any
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base: Any = declarative_base()


class User(Base):
    """Class describes a user"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
