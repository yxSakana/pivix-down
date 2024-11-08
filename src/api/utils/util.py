# -*- coding: utf-8 -*-
# @project pixiv-down
# @file util.py
# @brief
# @author yx
# @data 2024-11-03 23:33:10

from datetime import datetime

index = "https://www.pixiv.net"


def fmt_illust_url(i):
    return f"{index}/artworks/{i}"


def fmt_novel_url(i):
    return f"{index}/novel/show.php?id={i}" if is_id(i) else i


def is_valid_url(i: str) -> bool:
    return is_id(i) or i[:21] == index


def is_id(i) -> bool:
    try:
        return bool(int(i))
    except ValueError:
        return False


def fmt_timestamp(timestamp: str) -> str:
    return datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')
