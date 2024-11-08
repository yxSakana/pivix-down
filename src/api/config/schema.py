# -*- coding: utf-8 -*-
# @project pixiv-down
# @file schema.py
# @brief
# @author yx
# @data 2024-11-06 11:18:33

from dataclasses import dataclass
from typing import Dict
from pathlib import Path

from requests.cookies import RequestsCookieJar

from ..utils.headers import get_cookies_from_str


@dataclass
class RequestConfigSchema:
    user_agent:  str
    proxies:     Dict[str, str]
    cookie:     RequestsCookieJar
    key:         str

    def __init__(self, user_agent: str, proxies: Dict[str, str],
                 cookie_file: str, key: str):
        self.user_agent = user_agent
        self.proxies = proxies
        cookie_file = Path(cookie_file)
        if not cookie_file.is_file():
            self.cookie = RequestsCookieJar()
        self.cookie = get_cookies_from_str(cookie_file.read_text())
        self.key = key


@dataclass
class DownloaderConfigSchema:
    path: Path

    def __init__(self, path: str):
        self.path = Path(path)


@dataclass
class DatabaseConfigSchema:
    engine:   str
    database: str
    host:     str
    username: str
    password: str


@dataclass
class ConfigSchema:
    request:    RequestConfigSchema
    downloader: DownloaderConfigSchema
    database:   DatabaseConfigSchema

    def __init__(self, request, downloader, database):
        self.request = RequestConfigSchema(**request)
        self.downloader = DownloaderConfigSchema(**downloader)
        self.database = DatabaseConfigSchema(**database)
