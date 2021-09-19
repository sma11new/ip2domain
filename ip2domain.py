#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : Sma11New
# @Github : https://github.com/Sma11New

import os
import re
import csv
import time
import requests
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, wait
from argparse import ArgumentParser
from fake_useragent import UserAgent

from colorama import init
init(autoreset=True)

from wcwidth import wcswidth as ww
def rpad(s, n, c=" "):
    return s + (n - ww(s)) * c

requests.packages.urllib3.disable_warnings()    # 抑制https错误信息

class IP2Domain:
    def __init__(self):
        self.banner()
        self.args = self.parseArgs()
        self.init()
        self.multiRun()

    def banner(self):
        logo = rf"""
           _      ___     __                _    
          (_)__  |_  |___/ /__  __ _  ___ _(_)__ 
         / / _ \/ __// _  / _ \/  ' \/ _ `/ / _ \
        /_/ .__/____/\_,_/\___/_/_/_/\_,_/_/_//_/    Author: Sma11New
         /_/ """
        msg = f"""
   ip2domain：调用WebScan接口批量IP反查域名，调用vvhan接口批量查备案信息
"""
        print("\033[93m" + logo + "\033[0m")
        print(msg)

    def init(self):
        if not os.path.isfile(self.args.file):
            print(f"\n\033[31m[!]  Load file [{self.args.file}] Failed\033[0m")
            exit(0)
        self.ipList = self.loadTarget()  # 所有目标
        print(f"\033[36m[*]  Thread : {self.args.thread}")
        print(f"\033[36m[*]  Timeout: {self.args.Timeout}")
        print(f"\033[36m[*]  ipCount: {len(self.ipList)}\033[0m\n")

    def parseArgs(self):
        date = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        parser = ArgumentParser()
        parser.add_argument("-f", "--file", metavar="", required=True, type=str, help=f"Target IP file")
        parser.add_argument("-t", "--thread", metavar="", required=False, type=int, default=32, help=f"Number of thread (default 32)")
        parser.add_argument("-T", "--Timeout", metavar="", required=False, type=int, default=3,  help="request timeout (default 3)")
        parser.add_argument("-o", "--output", metavar="", required=False, type=str, default=f"title_{date}",  help="output file (default ./output/{fileName}_title_{date}.csv)")
        return parser.parse_args()

    # vvhan查询备案信息
    def searchRecordByVvhan(self, domain):
        header = {
            "user-agent": UserAgent().random
        }
        resultDic = {"unitName": "", "unitType": "", "unitICP": "", "title": ""}
        try:
            rep = requests.get(url=f"https://api.vvhan.com/api/icp?url={domain}", headers=header, timeout=3)
            try:
                resultDic["unitName"] = rep.json()["info"]["name"]
            except:
                pass
            try:
                resultDic["unitType"] = rep.json()["info"]["nature"]
            except:
                pass
            try:
                resultDic["unitICP"] = rep.json()["info"]["icp"]
            except:
                pass
            try:
                resultDic["title"] = rep.json()["info"]["title"]
            except:
                pass
            return resultDic
        except:
            resultDic["unitName"] = f"{' '*8}-- Connect Failed --"
            return resultDic

    # webscan反查域名
    def searchDomain(self, ip):
        headers = {"user-agent": UserAgent().random}
        try:
            rep = requests.get(url=f"http://api.webscan.cc/?action=query&ip={ip}", headers=headers)
            if rep.text != "null":
                results = rep.json()
                for result in results:
                    domainName = result["domain"]
                    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", domainName):
                        continue
                    if domainName  in self.mainDomainNameList:
                        continue
                    icpDataDic = self.searchRecordByVvhan(domainName)
                    icpDataList = list(icpDataDic.values())
                    webDataList = [ip, domainName] + icpDataList
                    msg = f"|{rpad(webDataList[0], 17)}|{rpad(webDataList[1], 22)}|{rpad(webDataList[2], 37)}|{rpad(webDataList[3], 10)}|{rpad(webDataList[4], 22)}|{rpad(webDataList[5], 30)}|\n"
                    msg += f"+{'-' * 17}+{'-' * 22}+{'-' * 37}+{'-' * 10}+{'-' * 22}+{'-' * 30}+"
                    self.lock.acquire()
                    try:
                        self.mainDomainNameList.append(domainName)
                        self.domainResultList.append(webDataList)
                        print(msg)
                    finally:
                        self.lock.release()
        except:
            msg = f"|{rpad(ip, 17)}|{rpad(' -- Connect Failed --', 22)}|{rpad(' ', 37)}|{rpad(' ', 10)}|{rpad(' ', 22)}|{rpad(' ', 30)}|\n"
            msg += f"+{'-' * 17}+{'-' * 22}+{'-' * 37}+{'-' * 10}+{'-' * 22}+{'-' * 30}+"
            self.lock.acquire()
            try:
                print(msg)
            finally:
                self.lock.release()

    # 加载ip地址、去重
    def loadTarget(self):
        targetList = []
        with open(self.args.file) as f:
            for line in f.readlines():
                line = line.strip()
                if "https://" in line:
                    line = line.replace("https://", "")
                if "http://"  in line:
                    line = line.replace("http://", "")
                try:
                    # 允许IP文件中放入带端口的数据，如127.0.0.1:8080，截取IP
                    targetList.append(line.split(":")[0])
                except:
                    targetList.append(line)
        return list(set(targetList))

    # 多线程运行
    def multiRun(self):
        self.start = time.time()
        self.mainDomainNameList = []
        self.domainResultList = []
        self.lock = Lock()
        executor = ThreadPoolExecutor(max_workers=self.args.thread)
        msg = f"+{'-' * 17}+{'-' * 22}+{'-' * 37}+{'-' * 10}+{'-' * 22}+{'-' * 30}+\n"
        msg += f"|{rpad('ip', 17)}|{rpad('反查域名', 22)}|{rpad('单位名称', 37)}|{rpad('单位性质', 10)}|{rpad('备案编号', 22)}|{rpad('网站标题', 30)}|\n"
        msg += f"+{'-' * 17}+{'-' * 22}+{'-' * 37}+{'-' * 10}+{'-' * 22}+{'-' * 30}+"
        print(msg)
        all = [executor.submit(self.searchDomain, (url)) for url in self.ipList]
        wait(all)
        self.outputResult()

    # 输出结果
    def outputResult(self):
        fileName = list(os.path.splitext(os.path.basename(self.args.file)))[0]
        self.outputFile = f"./output/{fileName}_{self.args.output}.csv"
        if not os.path.isdir(r"./output"):
            os.mkdir(r"./output")
        with open(self.outputFile, "a", encoding="gbk", newline="") as f:
            csvWrite = csv.writer(f)
            csvWrite.writerow(["ip", "反查域名", "单位名称", "单位性质", "备案编号", "网站标题"])
            for result in self.domainResultList:
                csvWrite.writerow(result)
        self.end = time.time()
        print("\nTime Spent: %.2f s" % (self.end - self.start))
        print(f"{'-' * 20}\nThe result has been saved in \033[36m{self.outputFile}\033[0m\n")

if __name__ == "__main__":
    IP2Domain()