# -*- coding: utf-8 -*-
# @project pixiv-down
# @file analyser.py
# @brief
# @author yx
# @data 2024-11-04 19:35:10

from typing import Union

import pandas as pd

from ..parser.items import IllustItems, NovelItems


class Analyser:
    @staticmethod
    def analysis(items: NovelItems):
        pass

    @staticmethod
    def by_date(items: Union[IllustItems, NovelItems]) -> pd.Series:
        data = pd.DataFrame(items)
        data["date"] = pd.to_datetime(data["date"])
        monthly_counts = (data.groupby(data["date"].dt.to_period('M'))
                          .size()
                          .reset_index(name="count"))
        monthly_counts["date"] = monthly_counts["date"].dt.to_timestamp()
        monthly_counts.columns = ['month', 'count']
        monthly_counts.set_index("month", inplace=True)
        return monthly_counts["count"]

    @staticmethod
    def by_word_count(items: NovelItems) -> pd.Series:
        data = pd.DataFrame(items)
        return data["word_count"]

    @staticmethod
    def by_view_count(items: Union[IllustItems, NovelItems]) -> pd.Series:
        data = pd.DataFrame(items)
        return data["view_count"]

    @staticmethod
    def by_bookmark_count(items: Union[IllustItems, NovelItems]) -> pd.Series:
        data = pd.DataFrame(items)
        return data["bookmark_count"]

    @staticmethod
    def by_like_rate(items: Union[IllustItems, NovelItems]) -> pd.Series:
        data = pd.DataFrame(items)
        return (data["bookmark_count"] / data["view_count"]).round(2)

