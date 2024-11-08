# -*- coding: utf-8 -*-
# @project S-pixiv
# @file pixiv_parser.py
# @brief
# @author yx
# @data 2024-02-06 15:02:14

import re
import json
import urllib.parse
from pprint import pprint
from typing import Dict

from lxml import etree

from .items import (
    UserItem, IllustItem, NovelItem,
    FollowUsersItem, TrendsItem,
    UserWorksItem, FollowUsersItems
)
from ..utils.util import fmt_timestamp
import tools.logger


JsonData = Dict


def match_uid(cookie: str) -> str:
    return re.search("PHPSESSID=(\\d+?)_", cookie).group(1)


def match_wid(url: str) -> str:
    base_url = "https://www.pixiv.net/artworks/"
    url = urllib.parse.urljoin(base_url, url)
    return url.split("/")[-1]


def join_wid(wid: str) -> str:
    return f"https://www.pixiv.net/artworks/{wid}"


def match_nid(url: str) -> str:
    try:
        return re.search("\\?id=(\\d+)", url).group(1)
    except AttributeError:
        tools.logger.get_logger(__name__).error(f"failed match_nid: {url}")


def join_nid(nid: str) -> str:
    return f"https://www.pixiv.net/novel/show.php?id={nid}"


def parse_illust_doc(text: str, wid: str) -> IllustItem:
    docs = etree.HTML(text)
    preload_data = json.loads(docs.xpath('//*[@id="meta-preload-data"]/@content')[0])
    body = preload_data["illust"][wid]
    start_url = body["urls"]["original"]
    page_count = int(body["pageCount"])
    return IllustItem(
        uid            = list(preload_data["user"].keys())[0],
        wid            = wid,
        title          = body["title"],
        tags           = [tag["tag"] for tag in body["tags"]["tags"]],
        description    = body["description"] or body["illustComment"],
        images         = [re.sub("_p\\d+", f"_p{str(i)}", start_url, count=1)
                          for i in range(page_count)],
        date           = fmt_timestamp(body["createDate"]),
        view_count     = int(body["viewCount"]),
        bookmark_count = int(body["bookmarkCount"]),
        page_count     = int(body["pageCount"]),
    )


def parse_user_doc(data: JsonData) -> UserItem:
    meta = data["body"]["extraData"]["meta"]
    return UserItem(
        uid          = meta["canonical"].split("/")[-1],
        name         = meta["ogp"]["title"],
        home         = meta["canonical"],
        image        = "",
        background   = meta["twitter"]["image"],
        description  = meta["ogp"]["description"]
    )


def parse_novel_doc(text: str, nid: str) -> NovelItem:
    docs = etree.HTML(text)
    content = docs.xpath('//*[@id="meta-preload-data"]/@content')[0]
    data = json.loads(content)

    novel_id, novel_data = tuple(data["novel"].items())[0]
    user_id, user_data = tuple(data["user"].items())[0]
    return NovelItem(
        uid             = user_id,
        nid             = nid,
        title           = novel_data["title"],
        tags            = [item["tag"] for item in novel_data["tags"]["tags"]],
        date            = fmt_timestamp(novel_data["createDate"]),
        description     = novel_data["extraData"]["meta"]["description"],
        content         = novel_data["content"],
        # novel_ids= list(novel_data["userNovels"].keys()),
        view_count      = novel_data["viewCount"],
        bookmark_count  = novel_data["bookmarkCount"],
        word_count      = novel_data["characterCount"],
    )


def parse_follow_users_doc(data: JsonData) -> FollowUsersItems:
    users = data["body"]["users"]
    return [FollowUsersItem(
        user_info = UserItem(
            uid         = item["userId"],
            name= item["userName"],
            image= item["profileImageUrl"],
            description = item["userComment"]
        ),
        novels = [
            NovelItem(
                uid         = item["userId"],
                nid         = novel["id"],
                title       = novel["title"],
                tags        = novel["tags"],
                description = novel["description"],
                content     = "",
                # novel_ids= [],
            )
            for novel in item.get("novels", [])
        ],
        novel_ids = [novel["id"] for novel in item.get("novels", [])],
        illusts= [
            IllustItem(
                uid         = item["userId"],
                wid         = work["id"],
                title       = work["title"],
                tags        = work["tags"],
                description = work["description"],
                images= []
            )
            for work in item.get("illusts", [])
        ],
        illust_ids= [work["id"] for work in item.get("illusts", [])],
    )
        for item in users
    ]


def parse_trends_doc(data: JsonData) -> TrendsItem:
    main_data = data["body"]
    return TrendsItem(
        ids = main_data["page"]["ids"],
        illusts= [IllustItem(
            uid = item["userId"],
            wid   = item["id"],
            title = item["title"],
            tags  = item["tags"],

        ) for item in main_data["thumbnails"]["illust"]]
    )


def parse_user_works_doc(data: JsonData) -> UserWorksItem:
    import tools.files
    tools.files.save("tmp/user_works_novel.json", data, ensure_json=True)
    works  = data["body"]["illusts"]
    novels = data["body"]["novels"]
    mangas = data["body"]["manga"]
    return UserWorksItem(
        illust_ids= list(works.keys()) if isinstance(works, dict) else [],
        novel_ids = list(novels.keys()) if isinstance(novels, dict) else [],
        manga_ids = list(mangas.keys()) if isinstance(mangas, dict) else [],
    )
