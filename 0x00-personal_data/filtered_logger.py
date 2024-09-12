#!/usr/bin/env python3

"""Module defines function that obufscates sensitive info"""
from typing import List
import re
import os
import logging
from mysql.connector import MySQLConnection

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    returns obfuscated message

    args:
        fields (List[str]): fields to be obfuscated
        redaction (str): obfsuscation string
        message (str): string to be obfuscated
        separator (str): character that separates fields in message

    returns:
        str : obfuscated message
    """
    pattern = "|".join([f"{field}=[^\\{separator}]*" for field in fields])
    return re.sub(
        pattern,
        lambda m: f"{m.group(0).split('=')[0]}={redaction}",
        message
    )


def get_logger() -> logging.Logger:
    """returns a logger object"""
    user_data = logging.getLogger("user_data")
    user_data.setLevel(logging.INFO)
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    user_data.addHandler(stream_handler)
    user_data.propagate = False

    return user_data


def get_db() -> MySQLConnection:
    """Returns a MySQLConnection object to connect to the database"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    return MySQLConnection(
        user=username, password=password, host=db_host, database=db_name
    )


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(
            fields=self.fields,
            redaction=self.REDACTION,
            message=record.msg,
            separator=self.SEPARATOR,
        )
        return super(RedactingFormatter, self).format(record=record)
