# -*- coding: utf-8 -*-
# @project snowm
# @file media.py
# @brief
# @author yx
# @resources 2024-01-30 19:24:32

import os
import subprocess


def from_dir_merge(src_path, output_file="video/output.mp4") -> bool:
    if os.path.dirname(output_file):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
    files = [f for f in os.listdir(src_path) if os.path.isfile(os.path.join(src_path, f))]
    files = sorted(files, key=lambda item: int(item.split(".")[0]))
    files = [os.path.join(src_path, f) for f in files]
    command = [
        "ffmpeg",
        "-i",
        f"concat:{'|'.join(files)}",
        "-c",
        "copy",
        "-y",
        output_file
    ]
    return subprocess.run(command, stdout=False, stderr=False).returncode == 0


if __name__ == "__main__":
    from_dir_merge("../../resources/video")
