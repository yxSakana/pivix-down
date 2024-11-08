# -*- coding: utf-8 -*-
# @project bilibili-down
# @file ffmpeg.py
# @brief
# @author yx
# @data 2024-02-05 23:01:19

import os

import ffmpeg

import tools.files


def merge(
        video: str,
        audio: str,
        output: str,
        overwrite_output: bool = True,
        keep_origin = False
) -> None:
    """

    :param video:
    :param audio:
    :param output:
    :param overwrite_output: 是否忽略已存在文件
    :param keep_origin: 是否保留video、audio
    :return:
    """
    video, audio, output = map(tools.files.sanitize_path, [video, audio, output])
    (
        ffmpeg
        .output(
            ffmpeg.input(video), ffmpeg.input(audio),
            output,
            vcodec="copy")
        .run(capture_stdout=True, capture_stderr=True,
             overwrite_output=overwrite_output)
    )
    if not keep_origin:
        for f in [video, audio]:
            os.remove(f)
