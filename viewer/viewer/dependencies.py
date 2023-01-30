import datetime
from typing import Optional, Union

from fastapi import Query
from pydantic.validators import str_validator

from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class EmptyString(str):
    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield lambda v: None if v == '' else v


class QueryParams:
    def __init__(
            self, keyword: str = Query(default=''),
            date_from: Union[None, datetime.date, EmptyString] = Query(default=None),
            date_till: Union[None, datetime.date, EmptyString] = Query(default=None),
    ):
        self.keyword = keyword
        self.date_from = date_from
        self.date_till = date_till
