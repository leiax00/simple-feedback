# !/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import TypeVar, Generic, Optional

from pydantic import BaseModel
from fastapi import status

T = TypeVar('T')


class RCode(BaseModel):
    code: int = status.HTTP_200_OK


class RBase(RCode):
    msg: Optional[str] = None


class R(RBase, Generic[T]):
    data: Optional[T] = None

class PageR(RBase, Generic[T]):
    rows: Optional[T] = None
    total: Optional[int] = 0