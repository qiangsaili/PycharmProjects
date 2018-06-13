#!/usr/bin/env python
# encoding: utf-8
'''
@author: Sally
@time: 2018/6/7 19:47
'''
import requests

url = "https://oapi.dingtalk.com/robot/send?access_token=c8ee68a6f194deef432c5118e68b7a6f45ed7d0b0128c97b77e2c902526d0de2"
json_data = {
     "msgtype": "text",
     "text": {
         "content": "妈妈，你怎么不回家"
     }
}
requests.post(url, json=json_data)
