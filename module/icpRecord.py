#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : Sma11New
# @Github : https://github.com/Sma11New

import requests

# vvhan查询备案信息
def searchRecord(domain, timeout):
    # By Vvhan
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    }
    resultDic = {"code":1, "domain":domain, "unitName": "", "unitType": "", "unitICP": "", "title": ""}
    try:
        rep = requests.get(url=f"https://api.vvhan.com/api/icp?url={domain}", headers=header, timeout=timeout)
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
        resultDic["code"] = -1
        return resultDic

if __name__ == "__main__":
    for i in searchRecord("itcast.cn", 3).values():
        print(i)
