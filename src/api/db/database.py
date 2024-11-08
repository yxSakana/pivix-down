# -*- coding: utf-8 -*-
# @project pixiv-down
# @file database.py
# @brief
# @author yx
# @data 2024-11-04 19:59:31

from .mysql import MySql
from ..config.schema import DatabaseConfigSchema


class Database:
    def __init__(self, config: DatabaseConfigSchema):
        database = config.database
        host = config.host
        user = config.username
        password = config.password
        if "mysql" == config.engine.lower():
            self._db = MySql(host, user, password, database)
        else:
            self._db = MySql(host, user, password, database)

    @property
    def db(self):
        return self._db
