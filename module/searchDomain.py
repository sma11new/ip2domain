#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : Sma11New
# @Github : https://github.com/Sma11New

import re
import tldextract
import requests

def searchDomain(ip, timeout):
    mainDomainNameList = []
    searchDomainResult = {"code": 0, "ip":ip, "domainList": []}

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
    }
    try:
        rep = requests.get(url=f"http://api.webscan.cc/?action=query&ip={ip}", headers=headers, timeout=timeout)
        if rep.text != "null":
            results = rep.json()
            for result in results:
                domainName = result["domain"]
                if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", domainName):
                    continue
                if domainName  in mainDomainNameList:
                    continue
                # 取主域
                val = tldextract.extract(domainName)
                if f"{val.domain}.{val.suffix}" not in mainDomainNameList:
                    mainDomainNameList.append(f"{val.domain}.{val.suffix}")
            searchDomainResult["code"] = 1
            searchDomainResult["domainList"] = mainDomainNameList
        else:
            searchDomainResult["code"] = 0
    except:
        searchDomainResult["code"] = -1

    return searchDomainResult

if __name__ == "__main__":
    s = searchDomain("211.103.136.242", 3)
    if s["code"] == 1:
        for i in s["domainList"]:
            print(f"{s['ip']}  {i}")