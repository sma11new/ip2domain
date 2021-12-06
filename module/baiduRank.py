import re
import requests



def baiduRank(domain, timeout):
    """
    利用爱站接口查询权重信息
    """
    reqURL = f"https://www.aizhan.com/cha/{domain}/"
    headers = {
        "Host": "www.aizhan.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    baiduRankResult = {"code": 1, "rank": -1}
    try:
        rep = requests.get(url=reqURL, headers=headers, timeout=timeout)
    except:
        baiduRankResult["code"] = -1
        return baiduRankResult
    # 百度权重正则
    # baiduRankRegular = re.compile(r'/images/br/([0-9]+).png')
    baiduRankRegular = re.compile(r'aizhan.com/images/br/(.*?).png')
    try:
        baiduRankResult["rank"] = int(baiduRankRegular.findall(rep.text)[0])
        return baiduRankResult
    except:
        baiduRankResult["code"] = 0
        return baiduRankResult

# def baiduRank(domain, timeout):
#     reqURL = f"https://baidurank.aizhan.com/baidu/{domain}"
#     headers = {
#         "Host": "baidurank.aizhan.com",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
#         "Content-Type": "application/x-www-form-urlencoded",
#     }
#
#     baiduRankResult = {"code":1, "rank":-1}
#     try:
#         rep = requests.get(url=reqURL, headers=headers, timeout=timeout)
#     except:
#         baiduRankResult["code"] = -1
#         return baiduRankResult
#     # 百度权重正则
#     baiduRankRegular = re.compile(r'/images/br/([0-9]+).png')
#     try:
#         baiduRankResult["rank"] = int(baiduRankRegular.findall(rep.text)[0])
#         return baiduRankResult
#     except:
#         baiduRankResult["code"] = 0
#         return baiduRankResult

if __name__ == '__main__':
    rank = baiduRank("fer.cn", 3)
    print(rank["rank"])

