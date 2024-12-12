# -*- coding: utf-8 -*-
# @project pixiv-down
# @file cli.py
# @brief
# @author yx
# @data 2024-09-22 16:18:02


import os
import argparse
from pprint import pprint
from dataclasses import asdict

import api.pixiv_api
import tools.files
from api.utils.headers import from_jar_get_cookie

cookie = tools.files.read("config/cookie")
proxies = {
    "http": "127.0.0.1:7890",
    "https": "127.0.0.1:7890"
}
pixiv_api = api.pixiv_api.PixivApi()


def config(args):
    if args.show:
        pprint(asdict(pixiv_api.config))
    if args.cookie and os.path.exists(args.cookie):
        pixiv_api.config.request.cookies = from_jar_get_cookie(args.cookie)
    if args.proxy:
        p = args.proxy.split(";")
        pixiv_api.config.request.proxies = {
            "http": p[0],
            "https": p[1]
        }
    if args.directory:
        pixiv_api.config.downloader.path = args.directory


def search(args):
    out = None
    if args.type == "illust":
        out = pixiv_api.search_illust(args.i)
    elif args.type == "user":
        out = pixiv_api.search_user(args.i)
    elif args.type == "novel":
        out = pixiv_api.search_novel(args.i)
    pprint(asdict(out))


def download(args):
    if args.type == "illust":
        pixiv_api.download_illust(args.i)
    # elif args.type == "user":
    #     pixiv_api.download.user_works(args.i)
    elif args.type == "novel":
        pixiv_api.download_novel(args.i)
    elif args.type == "all":
        pixiv_api.download_user_works(args.i)
    else:
        print(f"{args.type} is not supported")


def scan(args):
    if args.type == "all":
        pixiv_api.scan(args.uid)
    elif args.type == "illust":
        pixiv_api.scan_illust(args.uid)
    elif args.type == "novel":
        pixiv_api.scan_novel(args.uid)


def analyse(args):
    if args.type == "all":
        pixiv_api.analyse(args.uid)
    elif args.type == "illust":
        pixiv_api.analyse_illust(args.uid)
    elif args.type == "novel":
        pixiv_api.analyse_novel(args.uid)


def test(args):
    pass


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    # configure
    cli_config = subparsers.add_parser("config", help="Configure pixiv_api")
    cli_config.add_argument("--show", action="store_true", help="Show")
    cli_config.add_argument("-c", "--cookie", type=str, help="Cookie")
    cli_config.add_argument("-d", "--directory", type=str, help="Directory where pixiv_api will be saved")
    cli_config.add_argument("-p", "--proxy", type=str, help="Proxy [http;https]")
    cli_config.set_defaults(func=config)
    # search
    cli_search = subparsers.add_parser('search', help='Search for user/illust/novel')
    cli_search.add_argument("-t", "--type",
                            type=str, choices=["illust", "user", "novel"], default="illust",
                            help="search by [illust, user, novel]")
    cli_search.add_argument("-i", type=str, help="url or id", required=True)
    cli_search.set_defaults(func=search)
    # download
    cli_download = subparsers.add_parser('download', help='Download for user/illust/novel')
    cli_download.add_argument("-t", "--type",
                              type=str, choices=["all", "illust", "novel"], default="illust",
                              help="search by [illust, user, novel]")
    cli_download.add_argument("-i", type=str, help="url or id", required=True)
    cli_download.set_defaults(func=download)
    # scan
    cli_scan = subparsers.add_parser('scan', help='scan user illust/novel/manga/all work')
    cli_scan.add_argument("-u", "--uid", type=str, help="uid", required=True)
    cli_scan.add_argument("-t", "--type",
                          choices=["illust", "novel", "manga", "all"], default="novel")
    cli_scan.set_defaults(func=scan)
    # data analyse
    cli_analyse = subparsers.add_parser('analyse', help='analyse data')
    cli_analyse.add_argument("-u", "--uid", type=str, help="uid", required=True)
    cli_analyse.add_argument("-t", "--type",
                             choices=["illust", "novel", "manga", "all"], default="novel")
    cli_analyse.set_defaults(func=analyse)
    # test
    cli_test = subparsers.add_parser('test', help='Test pixiv_api')
    cli_test.set_defaults(func=test)
    # parse
    args = parser.parse_args()
    if not vars(args):
        parser.print_help()
        return
    args.func(args)
