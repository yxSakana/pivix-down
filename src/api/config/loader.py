# -*- coding: utf-8 -*-
# @project pixiv-down
# @file loader.py
# @brief
# @author yx
# @data 2024-11-07 20:41:28

import json
from pathlib import Path

from .schema import ConfigSchema


def load_config_from_json(path: Path):
    if not path.is_file():
        return
    config_data = json.loads(path.read_text())
    return ConfigSchema(**config_data)
