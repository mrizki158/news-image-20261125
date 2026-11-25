#!/usr/bin/env python3
"""Copy entry.png to the output directory.

Reads MAKEFUN_OUTPUT_DIR (default /output) and copies the entry image
(entry.png, next to this file) there. Standard library only.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("copied {} -> {}".format(src, dst))


if __name__ == "__main__":
    main()
