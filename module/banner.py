#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : Sma11New
# @Github : https://github.com/Sma11New

def banner():
    logo = f"""
                  _________
                      |
                      |
                     _|_
                ///\(\033[0m\033[31mo\033[0m\033[92m_\033[0m\033[31mo\033[0m\033[92m)/\\\\\\
                |||  ` '  |||
     ip2domain                 Author: Sma11New
                    v0.2
    """
    msg = f"""  ip2domain：IP反查域名，查询备案信息、查询百度权重
            
 (由于接口对请求频率有限制，故查询速率较慢，请耐心等待)
    """
    print("\033[92m" + logo + "\033[0m")
    print(msg)

if __name__ == "__main__":
    pass
