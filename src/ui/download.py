# -*- coding: utf-8 -*-
# @project S-pixiv
# @file download.py
# @brief
# @author yx
# @data 2024-02-07 20:38:06

from PyQt5.QtWidgets import \
    QApplication, QWidget, QTabWidget, \
    QPushButton, QRadioButton, QLineEdit, QLabel, QMessageBox, \
    QVBoxLayout, QHBoxLayout, \
    QHeaderView, QSizePolicy
from PyQt5.QtGui import QIcon

from api.pixiv_api import PixivApi


class BaseDownloadUi(QWidget):
    def __init__(self, api: PixivApi, parent=None):
        super().__init__(parent)

        self.api = api


class WorkDownloadUi(BaseDownloadUi):
    def __init__(self, api: PixivApi, parent=None):
        super().__init__(api, parent)

        self.api = api
