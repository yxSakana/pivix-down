# -*- coding: utf-8 -*-
# @project snowm
# @file headers.py
# @brief
# @author yx
# @resources 2024-01-30 22:41:43

import requests.cookies


UserAgent = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
]


def from_jar_get_cookie(cookie: requests.cookies.RequestsCookieJar) -> str:
    return ";".join((f"{k}={v}" for k, v in cookie.items()))


def get_cookies_from_str(s: str) -> requests.cookies.RequestsCookieJar:
    jar = requests.cookies.RequestsCookieJar()
    if not s:
        return jar
    [jar.set(*c.split("=", 1)) for c in s.split(";") if s and c]
    return jar


def user_agent():
    return UserAgent[0]
