# -*- coding: utf-8 -*-
# @project pixiv-down
# @file view.py
# @brief
# @author yx
# @data 2024-11-04 23:07:39

from typing import Callable, Any

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd


class View:
    @staticmethod
    def plot_count(ax: plt.Axes, data: pd.Series, title: str,
                   xl: str = "Index",
                   yl: str = "Count",
                   label: Callable[[Any, Any], str] = lambda x, y: f'{x},{y}',
                   offset: float = .0,
                   is_mean: bool = True,
                   is_y_integer: bool = False):
        data.plot(ax=ax, marker='o', linestyle='-', color='blue')
        add_coordinate_text(ax, data, label=label, offset=offset)
        ax.set_title(title, fontsize=16)
        ax.set_xlabel(xl, fontsize=14)
        ax.set_ylabel(yl, fontsize=14)
        if is_mean:
            ax.axhline(data.mean(), color='red', linestyle='--', label='Mean')
        if is_y_integer:
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.legend()


def add_coordinate_text(ax, data, offset = 0.2, is_interactive = True,
                        label: Callable[[Any, Any], str] = lambda x, y: f'{x}, {y}'):
    for i, (x, y) in enumerate(data.items()):
        offset = -offset if is_interactive and (i % 2 == 0) else offset
        ax.text(x, y + offset, label(x, y), ha='center', fontsize=12)
