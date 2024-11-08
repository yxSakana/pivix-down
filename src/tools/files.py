# -*- coding: utf-8 -*-
# @project snowm
# @file files.py
# @brief
# @author yx
# @resources 2024-01-30 18:15:41

import os
import re
import json
import logging
import threading
from typing import List
from pathlib import Path
import hashlib


def read(path, encoding="utf-8"):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding=encoding) as handle:
        return handle.read()


def save(path, content, append=False, encoding="utf-8", ensure_json=False):
    """会自动将非法字符替换为"""
    path = sanitize_path(path)
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(path, "a" if append else "w", encoding=encoding, newline="") as handle:
        handle.write(content if not ensure_json
                     else json.dumps(content, indent=2, ensure_ascii=False))


def save_multiple(path, contents: List, encoding="utf-8"):
    """(多线程)将一组数据保存到一个文件(不会清空文件)"""
    threads = []
    for content in contents:
        thread = threading.Thread(target=save, args=(path, content, True, encoding))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def save_media(path, content):
    path = sanitize_path(path)
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(content)


def save_multiple_media(data_pair: List):
    threads = []
    for path, content in data_pair:
        thread = threading.Thread(target=save_media, args=(path, content))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def download_media(url, path, headers=None, cookies=None, proxies=None):
    import requests
    res = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
    if res.ok:
        save_media(path, res.content)
    else:
        logging.warning(f"{url} requests failed: {res.status_code}")
        logging.warning(res.text)


def download_multiple_media_(dir_name: str, urls: List[str], **kwargs):
    """保存在一个目录中, 文件名从开始, 后缀名自动从url中匹配

    :param dir_name:
    :param urls:
    :return:
    """
    threads = []
    for i, url in enumerate(urls):
        thread = threading.Thread(target=download_media,
                                  args=(url, f"{dir_name}/{i}.{url.split('.')[-1]}"),
                                  kwargs=kwargs)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def download_multiple_media(data_pair: List, **kwargs):
    threads = []
    for url, path in data_pair:
        thread = threading.Thread(target=download_media,
                                  args=(url, path),
                                  kwargs=kwargs)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def _sanitize_filename(filename):
    return re.sub(r'[ \\/*?:"<>|]', '', filename)
    # return re.sub(r'[ \\/*?:"<>|]', '', filename)


def sanitize_path(path):
    path_list = path.split(os.path.sep)
    filename = _sanitize_filename(path_list.pop())
    path_list.append(filename)
    return os.path.sep.join(path_list)


def format_size(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
    size /= 1024.0


def format_words(size: float) -> str:
    if size > 10000.0:
        size /= 10000.0
        return f"{size} w"


def is_repeat(file: Path, content = None, encoding = "utf-8", md5_threshold = 100 * 2**20) -> bool:
    if not file.exists():
        return False
    if file.stat().st_size > md5_threshold or content is None:
        return True
    content_byte = content.encode(encoding) if isinstance(content, str) else content
    md5_hash = hashlib.md5(content_byte).hexdigest()
    with file.open("rb") as f:
        digest = hashlib.file_digest(f, "md5")
    return md5_hash == digest.hexdigest()
