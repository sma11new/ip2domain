#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : Sma11New
# @Github : https://github.com/Sma11New

import os
import re
import csv
import time
import requests
import tldextract

from module.banner import banner
from module.argParse import parseArgs
from module.baiduRank import baiduRank
from module.icpRecord import searchRecord
from module.searchDomain import searchDomain

from colorama import init

init(autoreset=True)

from wcwidth import wcswidth as ww


def rpad(s, n, c=" "):
    return s + (n - ww(s)) * c


requests.packages.urllib3.disable_warnings()  # 抑制https错误信息


def init(parseClass):
    args = parseClass.parse_args()
    if not args.file and not args.target:
        print(parseClass.print_usage())
        exit(0)

    if args.file:
        if not os.path.isfile(args.file):
            print(
                f"\n[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[31m[ERRO] - Load file [{args.file}] Failed\033[0m")
            exit(0)

    targetList = loadTarget(args.file, args.target)  # 所有目标

    print(
        f"[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[36m[INFO] - Timeout:   {args.timeout}s\033[0m")
    print(
        f"[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[36m[INFO] - Delay:     {args.delay}s\033[0m")
    print(
        f"[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[36m[INFO] - Rank Size: >{args.rank}\033[0m")
    print(
        f"[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[36m[INFO] - ICP:       {args.icp}\033[0m")
    print(
        f"[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[36m[INFO] - ipCount:   {len(targetList)}\033[0m\n")

    return targetList


# 加载目标
def loadTarget(file, target):
    targetList = []

    # 解析输入目标数据
    def parseData(data):
        val = tldextract.extract(data)
        if not val.suffix:
            # 校验解析的数据
            if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                        val.domain):
                return f"{val.domain}"
            else:
                return ""
        else:
            return f"{val.domain}.{val.suffix}"

    if file:
        f = open(file, encoding="utf8")
        for line in f.readlines():
            target_ = parseData(line.strip())
            if target_:
                targetList.append(target_)
        f.close()

    if target:
        target_ = parseData(target.strip())
        if target_:
            targetList.append(target_)

    return list(set(targetList))


def outputResult(argsFile, argsOutput, resultList, icp):
    fileName = list(os.path.splitext(os.path.basename(argsFile)))[0]
    outputFile = f"./output/{fileName}_{argsOutput}.csv"
    if not os.path.isdir(r"./output"):
        os.mkdir(r"./output")
    with open(outputFile, "a", encoding="gbk", newline="") as f:
        csvWrite = csv.writer(f)
        if icp:
            csvWrite.writerow(["ip", "反查域名", "百度权重", "单位名称", "单位性质", "备案编号", "网站标题"])
        else:
            csvWrite.writerow(["ip", "反查域名", "百度权重"])
        for result in resultList:
            csvWrite.writerow(result)


def ip2domian(target, args, targetNum, targetCount):
    resultList = []
    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", target):
        searchDomainResult = searchDomain(target, args.timeout)
        time.sleep(args.delay)
        domainList = searchDomainResult["domainList"]
    else:
        domainList = [target]

    for domain in domainList:
        baiduRankResult = baiduRank(domain=domain, timeout=args.timeout)
        time.sleep(args.delay)
        if baiduRankResult["code"] == 1:
            if baiduRankResult["rank"] >= args.rank:
                resultList.append([target, domain, baiduRankResult["rank"]])
        elif baiduRankResult["code"] == -1:
            resultList.append([target, domain, "ConnError"])
        else: # 0 PageError
            resultList.append([target, domain, "PageError"])

    if args.icp:
        for result in resultList:
            icpResult = searchRecord(domain=result[1], timeout=args.timeout)
            time.sleep(args.delay)
            if icpResult["code"] == 1:
                result += [icpResult["unitName"], icpResult["unitType"], icpResult["unitICP"]]

    if len(resultList) == 0:
        print(f"\r({targetNum}/{targetCount})", end="", flush=True)

    return resultList


def printTitle(icp):
    if icp:
        msg = f"+{'-' * 17}+{'-' * 20}+{'-' * 10}+{'-' * 37}+{'-' * 10}+{'-' * 22}+\n"
        msg += f"|{rpad('ip/domain', 17)}|{rpad('反查域名', 20)}|{rpad('百度权重', 10)}|{rpad('单位名称', 37)}|{rpad('单位性质', 10)}|{rpad('备案编号', 22)}|\n"
        msg += f"+{'-' * 17}+{'-' * 20}+{'-' * 10}+{'-' * 37}+{'-' * 10}+{'-' * 22}+"
    else:
        msg = f"+{'-' * 17}+{'-' * 20}+{'-' * 10}+\n"
        msg += f"|{rpad('ip/domain', 17)}|{rpad('反查域名', 20)}|{rpad('百度权重', 10)}|\n"
        msg += f"+{'-' * 17}+{'-' * 20}+{'-' * 10}+"
    print(msg)


def printMsg(result, icp):
    rankColor = {
        0: "\033[37m",
        1: "\033[33m",
        2: "\033[32m",
        3: "\033[32m",
        4: "\033[34m",
        5: "\033[35m",
        6: "\033[36m",
        7: "\033[31m",
        8: "\033[31m",
        9: "\033[31m",
        10: "\033[31m",
        "ConnError": "\033[31m",
        "PageError": "\033[31m",
    }

    if icp:
        print(
            f"\r|{rpad(result[0], 17)}|{rpad(result[1], 20)}|{rankColor[result[2]]}{rpad('    ' + str(result[2]), 10)}\033[0m|{rpad(result[3], 37)}|{rpad(result[4], 10)}|{rpad(result[5], 22)}|")
        print(f"+{'-' * 17}+{'-' * 20}+{'-' * 10}+{'-' * 37}+{'-' * 10}+{'-' * 22}+")
    else:
        print(
            f"\r|{rpad(result[0], 17)}|{rpad(result[1], 20)}|{rankColor[result[2]]}{rpad('    ' + str(result[2]), 10)}\033[0m|")
        print(f"+{'-' * 17}+{'-' * 20}+{'-' * 10}+")


if __name__ == "__main__":
    banner()
    parseClass = parseArgs()
    args = parseClass.parse_args()
    targetList = init(parseClass)
    resultList = []
    printTitle(args.icp)
    targetCount = len(targetList)
    try:
        for i in range(len(targetList)):
            resultTmpList = []
            resultTmpList += ip2domian(targetList[i], args, targetNum=i+1, targetCount=targetCount)
            resultList += resultTmpList
            for i in resultTmpList:
                printMsg(i, args.icp)
        outputResult(args.file, args.output, resultList, args.icp)
    except KeyboardInterrupt:
        print("\nBye~")