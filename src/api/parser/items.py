# -*- coding: utf-8 -*-
# @project S-pixiv
# @file items.py
# @brief
# @author yx
# @data 2024-02-06 15:09:34

from typing import List, Dict
from dataclasses import dataclass, field, asdict


@dataclass
class UserWorksItem:
    illust_ids:  List[str] = field(default_factory=list)
    novel_ids:   List[str] = field(default_factory=list)
    manga_ids:   List[str] = field(default_factory=list)

    def __bool__(self):
        return bool(self.illust_ids or self.novel_ids or self.manga_ids)

    def to_db_schema(self) -> Dict:
        if not self:
            return {}
        res = asdict(self)
        res["illust_ids"] = ",".join(self.illust_ids)
        res["novel_ids"] = ",".join(self.novel_ids)
        res["manga_ids"] = ",".join(self.manga_ids)
        return res


@dataclass
class UserItem:
    uid:            str
    name:           str
    home:           str = ""
    image:          str = ""
    background:     str = ""
    description:    str = ""
    work_ids:       UserWorksItem = field(default_factory=UserWorksItem)

    def to_db_schema(self) -> Dict:
        work_ids = self.work_ids.to_db_schema()
        res = {k: v for k, v in asdict(self).items() if v}
        res.pop("work_ids")
        res.update(work_ids)
        return res


@dataclass
class IllustItem:
    wid:             str
    uid:             str
    title:           str
    tags:            List[str]
    description:     str = ""
    images:          List[str] = field(default_factory=list)
    date:            str = "",
    view_count:      int = 0,
    bookmark_count:  int = 0,
    page_count:      int = 0,

    def to_db_schema(self) -> Dict:
        res = {k: v for k, v in asdict(self).items() if v}
        res["tags"] = ",".join(self.tags)
        res["images"] = ",".join(self.images)
        return res


IllustItems = List[IllustItem]


@dataclass
class NovelItem:
    nid:             str
    uid:             str
    title:           str
    tags:            List[str]
    date:            str = ""
    description:     str = ""
    content:         str = ""  # 小说内容
    # novel_ids:       List[str] = field(default_factory=list)  # 该用户其他小说的id
    view_count:      int = 0
    bookmark_count:  int = 0
    word_count:      int = 0

    def to_db_schema(self) -> Dict:
        res = {k: v for k, v in asdict(self).items() if v}
        res["tags"] = ",".join(self.tags)
        return res


NovelItems = List[NovelItem]


@dataclass
class FollowUsersItem:
    user_info:   UserItem
    novels:      NovelItems
    novel_ids:   List[str]
    illusts:     IllustItems
    illust_ids:  List[str]


FollowUsersItems = List[FollowUsersItem]


@dataclass
class TrendsItem:
    ids:      List[str]
    illusts:  IllustItems

