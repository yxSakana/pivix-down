# -*- coding: utf-8 -*-
# @project pixiv-down
# @file mysql.py
# @brief
# @author yx
# @data 2024-11-03 15:59:36

from pprint import pprint
from typing import Optional, Dict

import pymysql.cursors

from ..parser.items import (UserItem, IllustItem, NovelItem, UserWorksItem)
import tools.logger


class MySql(object):
    def __init__(self, host="localhost", user="skn_p", password="skn",
                 database="pixiv", charset='utf8mb4'):
        self.connection = pymysql.connect(
            host=host, user=user, password=password, database=database, charset=charset)
        # self.del_all()  # FIXME
        self.logger = tools.logger.get_logger(__class__.__name__)

        self.init_db()

    def init_db(self):
        with self.connection.cursor() as cursor:
            # users
            sql = """
            CREATE TABLE IF NOT EXISTS users (
                uid            VARCHAR(255) PRIMARY KEY,
                name           VARCHAR(255) NULL,
                home           TEXT         NULL,
                image          TEXT         NULL,
                background     TEXT         NULL,
                description    TEXT         NULL,
                illust_ids     TEXT         NULL,
                novel_ids      TEXT         NULL,
                manga_ids      TEXT         NULL
            )
            """
            cursor.execute(sql)
            # illusts
            sql = """
            CREATE TABLE IF NOT EXISTS illusts (
                wid            VARCHAR(255) PRIMARY KEY,
                uid            VARCHAR(255) NOT NULL,
                title          VARCHAR(255) NULL,
                tags           TEXT         NULL,
                description    TEXT         NULL,
                images         TEXT         NULL,
                date           DATETIME     NULL,
                view_count     INT          NULL,
                bookmark_count INT          NULL,
                page_count     INT          NULL
            );
            """
            cursor.execute(sql)
            # novels
            sql = """
            CREATE TABLE IF NOT EXISTS novels (
                nid            VARCHAR(255) PRIMARY KEY,
                uid            VARCHAR(255) NOT NULL DEFAULT 0,
                date           DATETIME     NULL,
                title          VARCHAR(255) NULL DEFAULT '',
                tags           VARCHAR(255) NULL DEFAULT '',
                description    TEXT         NULL,
                content        LONGTEXT     NULL,
                view_count     INT          NULL DEFAULT 0,
                bookmark_count INT          NULL DEFAULT 0,
                word_count     INT          NULL DEFAULT 0
            );
            """
            cursor.execute(sql)
        self.connection.commit()

    def select_user(self, uid) -> Optional[UserItem]:
        self.logger.debug(f"From database select user({uid})")
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE uid = %s;"
            cursor.execute(sql, args=uid)
            res = cursor.fetchone()
            return (UserItem(
                uid=res[0], name=res[1],
                home=res[2], image=res[3],
                background=res[4], description=res[5],
                work_ids=UserWorksItem(
                    res[6].split(",") if res[6] else None,
                    res[7].split(",") if res[7] else None,
                    res[8].split(",") if res[8] else None))
                    if res else None)

    def select_illust(self, wid) -> Optional[IllustItem]:
        self.logger.debug(f"From database select illust({wid})")
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM illusts WHERE wid = %s;"
            cursor.execute(sql, args=wid)
            res = cursor.fetchone()
            return (IllustItem(
                uid=res[1],
                wid=res[0],
                title=res[2],
                tags=res[3],
                description=res[4],
                images=res[5],
                date=res[6],
                view_count=res[7],
                bookmark_count=res[8],
                page_count=res[9]
            ) if res else None)

    def select_novel(self, nid) -> Optional[NovelItem]:
        self.logger.debug(f"From database select novel({nid})")
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM novels WHERE nid = %s;"
            cursor.execute(sql, args=nid)
            res = cursor.fetchone()
            return (NovelItem(
                uid=res[1],
                nid=res[0],
                date=str(res[2]),
                title=res[3],
                tags=res[4],
                description=res[5],
                content=res[6],
                view_count=res[7],
                bookmark_count=res[8],
                word_count=res[9]) if res else None)

    def select_user_works(self, uid) -> Optional[UserWorksItem]:
        self.logger.debug(f"From database select user_works({uid})")
        with self.connection.cursor() as cursor:
            sql = "SELECT illust_ids, novel_ids, manga_ids FROM users WHERE uid = %s;"
            cursor.execute(sql, args=uid)
            res = cursor.fetchone()
            return (UserWorksItem(
                res[0].split(",") if res[0] else None,
                res[1].split(",") if res[1] else None,
                res[2].split(",") if res[2] else None)
                    if res else None)

    def insert_or_update(self, table: str, data: Dict):
        self.logger.debug(f"Update database {table}")
        with self.connection.cursor() as cursor:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data.keys()))
            updates = ", ".join([f"{k} = %s" for k in data.keys()])
            sql = f"""
            INSERT INTO {table}({columns}) VALUES({placeholders})
            ON DUPLICATE KEY UPDATE {updates}
            """
            cursor.execute(sql, args=list(data.values())*2)
        self.connection.commit()

    def __del_all(self):
        with self.connection.cursor() as cursor:
            for t in ["users", "illusts", "novels"]:
                cursor.execute(f"DROP TABLE IF EXISTS {t};")
        self.connection.commit()
