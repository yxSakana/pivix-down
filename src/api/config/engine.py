# -*- coding: utf-8 -*-
# @project pixiv-down
# @file engine.py
# @brief
# @author yx
# @data 2024-11-07 21:07:09

from pathlib import Path

from .loader import load_config_from_json
from .schema import ConfigSchema


class Config:
    def __init__(self):
        self._config = None

    def load(self, config_file: Path):
        self._config = load_config_from_json(config_file)

    def get(self) -> ConfigSchema:
        return self._config
