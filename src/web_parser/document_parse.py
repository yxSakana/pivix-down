# -*- coding: utf-8 -*-
# @project bilibili-down
# @file document_parse.py
# @brief
# @author yx
# @data 2024-02-05 21:55:19

import re
from typing import Dict

from lxml import etree
from lxml.html import HtmlElement


def get_title(html: HtmlElement) -> str:
    """获取标题"""
    return etree.HTML(html).xpath("/html/head/title/text()")[0]


def parse_m3u(content: str) -> Dict:
    parents = [r"#EXT-X-VERSION:(\d+)", r'#EXT-X-TARGETDURATION:(\d+)', r'#EXT-X-MEDIA-SEQUENCE:(\d+)']
    names = ["version", "target_duration", "media_sequence"]
    info = {}
    for p, n in zip(parents, names):
        match = re.search(r"#EXT-X-VERSION:(\d+)", content)
        if match:
            info[n] = int(match.group(1))

    extinf_matches = re.finditer(r'#EXTINF:(\d+\.\d+),\n(.+)', content)
    info["content"] = []
    for match in extinf_matches:
        duration = float(match.group(1))
        ts_file_path = match.group(2)
        info["content"].append((duration, ts_file_path))
    return info

