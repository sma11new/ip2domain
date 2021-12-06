#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : Sma11New
# @Github : https://github.com/Sma11New

import time
from argparse import ArgumentParser

def parseArgs():
    date = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    parser = ArgumentParser()
    parser.add_argument("-t", "--target", required=False, type=str, help=f"Target ip/domain")
    parser.add_argument("-f", "--file", dest="file", required=False, type=str, default="", help=f"Target ip/domain file")
    parser.add_argument("-s", "--delay", dest="delay", required=False, type=int, default=2, help=f"Request delay (default 2s)")
    parser.add_argument("-T", "--Timeout", dest="timeout", required=False, type=int, default=3, help="Request timeout (default 3s)")
    parser.add_argument("-r", "--rank", required=False, type=int, default=0, help="Show baiduRank size (default 0)")
    parser.add_argument("-o", "--output", dest="output", required=False, type=str, default=f"{date}", help="output file (default ./output/ip2domain_{fileName}_{date}.csv)")
    parser.add_argument("--icp", required=False, action="store_true", default=False, help="With search icp (default false)")
    return parser

if __name__ == "__main__":
    args = parseArgs()

