# -*- coding: utf-8 -*-
# @project S-pixiv
# @file test_download.py
# @brief
# @author yx
# @data 2024-02-06 22:35:49

import os
import dataclasses
import json
from dataclasses import asdict

from .config.schema import DownloaderConfigSchema
from .serach import SearchApi
from .parser.items import IllustItem, NovelItem, UserItem
import tools.files
import tools.logger


class DownloadApi(object):
    def __init__(self, search_api: SearchApi, config: DownloaderConfigSchema):
        self.headers = search_api.session.headers
        self.proxies = search_api.session.proxies
        self.base_path = config.path
        self.logger = tools.logger.get_logger(__class__.__name__)

    def userinfo(self, itme: UserItem):
        filename = self.base_path.joinpath(itme.uid, "data.json")
        if tools.files.is_repeat(filename, json.dumps(asdict(itme), indent=2, ensure_ascii=False)):
            return
        tools.files.save(str(filename), asdict(itme), ensure_json=True)

    def illust(self, item: IllustItem) -> None:
        self.logger.info(f"download base directory {os.path.abspath(self.base_path)}")
        self.logger.info(f"illust {item.wid} downloading...")
        dir_path = self.base_path.joinpath(item.uid, "image", item.wid)
        if dir_path.exists():
            self.logger.info(f"illust {item.wid} finish(exists)")
            self.logger.info(f"download directory {dir_path.absolute()}(exists)")
            return
        tools.files.download_multiple_media_(
            f"{dir_path.absolute()}",
            item.images,
            headers=self.headers,
            proxies=self.proxies
        )
        tools.files.save(f"{dir_path.absolute()}/data.txt", dataclasses.asdict(item), ensure_json=True)
        self.logger.info(f"illust {item.wid} finish")
        self.logger.info(f"download directory {dir_path.absolute()}")

    def novel(self, item: NovelItem) -> None:
        self.logger.info(f"download base directory {os.path.abspath(self.base_path)}")
        self.logger.info(f"novel {item.nid} downloading...")
        dir_path = self.base_path.joinpath(item.uid, "novel", item.nid)
        if dir_path.exists():
            self.logger.info(f"novel {item.nid} finish(exists)")
            self.logger.info(f"download directory {dir_path.absolute()}(exists)")
            return
        tools.files.save(f"{dir_path}/{item.nid}.txt",
                         f"""
                         title: {item.title}\n
                         tags: {item.tags}\n
                         words: {tools.files.format_words(len(item.content))}\n
                         {item.content}
                         """)
        tools.files.save(f"{dir_path}/data.txt",
                         {k: v for k, v in dataclasses.asdict(item).items() if k != "content"},
                         ensure_json=True)
        self.logger.info(f"novel {item.nid} finish")
        self.logger.info(f"download directory {dir_path.absolute()}")

    # def user_works(self, uid: str) -> None:
    #     item = self.search_api.search_user_works(uid)
    #     if item is None:
    #         return
    #     for i in item.illust_ids:
    #         self.illust(pixiv_parser.join_wid(i))
    #     for i in item.novel_ids:
    #         self.novel(pixiv_parser.join_nid(i))
