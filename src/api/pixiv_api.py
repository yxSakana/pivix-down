# -*- coding: utf-8 -*-
# @project S-pixiv
# @file pixiv_api.py
# @brief
# @author yx
# @data 2024-02-07 20:44:32

from pprint import pprint
from typing import Optional, Union
from pathlib import Path

from matplotlib import pyplot as plt

from .serach import SearchApi
from .parser import pixiv_parser
from .parser.items import (UserItem, IllustItem, NovelItem,
                           UserWorksItem, IllustItems, NovelItems)
from .download import DownloadApi
from .db.database import Database
from .data_analyse.analyser import Analyser
from .config.engine import Config
from .view.view import View
from .utils.util import fmt_novel_url, is_id, fmt_illust_url
import tools.logger


class PixivApi(object):
    def __init__(self):
        self.config = Config()
        self.config.load(Path("config/config.json"))
        self.config = self.config.get()
        self.search = SearchApi(self.config.request)
        self.download = DownloadApi(self.search, self.config.downloader)
        self.db_handler = Database(self.config.database)
        self.db = self.db_handler.db
        self.analyser = Analyser
        self.view = View()
        self.logger = tools.logger.get_logger(__class__.__name__)

    def search_user(self, uid: str) -> Optional[UserItem]:
        db_res = self.db.select_user(uid)
        if db_res:
            return db_res
        res = self.search.search_user(uid)
        if res is not None:
            self.db.insert_or_update("users", res.to_db_schema())
        return res

    def search_illust(self, url: str) -> Optional[IllustItem]:
        if is_id(url):
            url = fmt_illust_url(url)
        self.logger.info(f"Searching illust {url}...")
        wid = pixiv_parser.match_wid(url)
        db_res = self.db.select_illust(wid)
        if db_res:
            return db_res
        res = self.search.search_illust(url)
        if res is not None:
            self.search_user(res.uid)
            self.db.insert_or_update("illusts", res.to_db_schema())
        return res

    def search_novel(self, url: str) -> Optional[NovelItem]:
        if is_id(url):
            url = fmt_novel_url(url)
        self.logger.info(f"Searching novel {url}...")
        nid = pixiv_parser.match_nid(url)
        db_res = self.db.select_novel(nid)
        if db_res:
            return db_res
        res = self.search.search_novel(url)
        if res is not None:
            self.search_user(res.uid)
            self.db.insert_or_update("novels", res.to_db_schema())
        return res

    def search_user_works(self, uid: str) -> Optional[UserWorksItem]:
        db_res = self.db.select_user_works(uid)
        if db_res:
            return db_res
        res = self.search.search_user_works(uid)
        if res is not None:
            self.search_user(uid)
            data = res.to_db_schema()
            data.update({"uid": uid})
            self.db.insert_or_update("users", data)
        return res

    def download_userinfo(self, uid: str):
        item = self.search_user(uid)
        if not item:
            return
        self.download.userinfo(item)

    def download_illust(self, illust_id_or_url: str):
        item = self.search_illust(illust_id_or_url)
        if not item:
            return
        self.download.illust(item)
        self.download_userinfo(item.uid)

    def download_novel(self, novel_id_or_url: str):
        item = self.search_novel(novel_id_or_url)
        if not item:
            return
        self.download.novel(item)
        self.download_userinfo(item.uid)

    def download_user_works(self, uid: str):
        all_work_ids = self.search_user_works(uid)
        iids = all_work_ids.illust_ids if all_work_ids.illust_ids else []
        nids = all_work_ids.novel_ids if all_work_ids.novel_ids else []
        mids = all_work_ids.manga_ids if all_work_ids.manga_ids else []
        for wid in iids:
            self.download_illust(wid)
        for nid in nids:
            self.download_novel(nid)
        for mid in mids:
            pass

    def scan(self, uid):
        self.scan_illust(uid)
        self.scan_novel(uid)

    def scan_illust(self, uid) -> Optional[IllustItems]:
        all_work_ids = self.search_user_works(uid)
        if (not all_work_ids) or (not all_work_ids.illust_ids):
            return
        illust_ids = all_work_ids.illust_ids
        return [self.search_illust(fmt_illust_url(wid)) for wid in illust_ids]

    def scan_novel(self, uid) -> Optional[NovelItems]:
        all_work_ids = self.search_user_works(uid)
        if (not all_work_ids) or (not all_work_ids.novel_ids):
            return
        novel_ids = all_work_ids.novel_ids
        return [self.search_novel(fmt_novel_url(nid)) for nid in novel_ids]

    def analyse(self, uid):
        self.analyse_illust(uid)
        self.analyse_novel(uid)

    def analyse_illust(self, uid):
        items = self.scan_illust(uid)
        if not items:
            return
        fig = self.__analyse_data(items)
        f = self.config.downloader.path.joinpath(uid, "illust_analyser.png")
        f.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(f)
        fig.show()

    def analyse_novel(self, uid):
        items = self.scan_novel(uid)
        if not items:
            return
        fig = self.__analyse_data(items)
        f = self.config.downloader.path.joinpath(uid, "novel_analyser.png")
        f.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(f)
        fig.show()

    def __analyse_data(self, items: Union[IllustItems, NovelItems]):
        # by date
        fig, axes = plt.subplots(3, 2, figsize=(20, 10))
        data = self.analyser.by_date(items)
        self.view.plot_count(
            axes[0][0], data, "Count by Month", "Count", "Month",
            is_mean=False, is_y_integer=True,
            label=lambda x, y: f'{x.strftime("%Y-%m")[2:]}, {y}')
        # by word count
        # import matplotlib
        # matplotlib.use('TkAgg')
        if isinstance(items[0], NovelItem):
            data = self.analyser.by_word_count(items)
            data /= 1000
            data = data.round(1)
            self.view.plot_count(axes[0][1], data, title="Word Count", label=lambda x, y: f'{y}k')
        # by view count
        data = self.analyser.by_view_count(items)
        self.view.plot_count(axes[1][0], data, "View Count", label=lambda x, y: f'{y}')
        # by bookmark count
        data = self.analyser.by_bookmark_count(items)
        self.view.plot_count(axes[1][1], data, "Bookmark Count", label=lambda x, y: f'{y}')
        # by like rate
        data = self.analyser.by_like_rate(items)
        self.view.plot_count(axes[2][0], data, "Like Rate", label=lambda x, y: f'{y}')
        fig.tight_layout()
        return fig
