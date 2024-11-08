# -*- coding: utf-8 -*-
# @project S-pixiv
# @file core.py
# @brief
# @author yx
# @data 2024-02-27 20:22:26

# import sys
#
# from PyQt5.QtCore import QUrl
# from PyQt5.QtQml import QQmlApplicationEngine
# from PyQt5.QtGui import QGuiApplication
#
#
# def main():
#     app = QGuiApplication(sys.argv)
#     engine = QQmlApplicationEngine()
#     engine.load(QUrl("Search.qml"))
#
#
# if __name__ == '__main__':

import sys
from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import QQuickView

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    # view = QQuickView()
    # view.setSource(QUrl('src/ui/qml/CoreTabBar.qml'))
    # view.show()

    engine = QQmlApplicationEngine()
    # engine.load(QUrl("src/ui/qml/test.qml"))
    engine.load(QUrl("src/ui/qml/CoreTabBar.qml"))
    # engine.load(QUrl('src/ui/qml/UserInfo.qml'))
    # engine.load(QUrl('src/ui/qml/Search.qml'))
    # root_obj = engine.rootContext()
    # print(root_obj)
    # user_input = root_obj.findChild(QObject, "search_bar")
    # print(user_input)
    # engine.load(QUrl('src/ui/qml/UserInfo.qml'))
    # print(engine.)

    sys.exit(app.exec_())
