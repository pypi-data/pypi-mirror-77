#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : WeiWang Zhang
@Time    : 2019-09-19 14:33
@File    : wanmei_api_call.py
@Desc    : 完美世界签名接口调用方法
"""
import requests
from wmpy_util import hash_util
import json

# ai.wanmei.com设置
AI_WANMEI_HOST = "https://ai.wanmei.com/"
AI_ANY_CARD_OCR_URL = "ocr/anyCard"
AI_WANMEI_APPID = 3
AI_WANMEI_APPKEY = "66bb309c57124e529879296763a3c848"

# antispam.wanmei.com配置
ANTISPAM_WANMEI_HOST = "http://antispam.wanmei.com/"
ANTISPAM_WANMEI_HOST_HTTPS = "https://antispam.wanmei.com/"
ANTISPAM_CLASSIFIER_URL = "image/online/check/"
ANTISPAM_CLASSIFIER2_URL = "image/online/check/v2"
ANTISPAM_WANMEI_APPID = 1
ANTISPAM_WANMEI_APPKEY = "41c2bdac6a1b4cabbfc5d4b948d17233"

ANTISPAM_WANMEI_APPID_PROD = 1
ANTISPAM_WANMEI_APPKEY_PROD = "41c2bdac6a1b4cabbfc5d4b948d17233"


def call_wm_api(url, data, app_id=ANTISPAM_WANMEI_APPID, app_key=ANTISPAM_WANMEI_APPKEY, verbose=False):
    """
    访问完美api
    :param url: api地址
    :param data: 参数
    :param app_id: 应用ID
    :param app_key: 应用Key
    :return:
    """
    app_key = hash_util.process_appkey(app_key)
    if data is None or not isinstance(data, dict):
        print("Param not found")
        data = dict()
    data["appId"] = app_id
    data["timestamp"] = 10000
    sign = hash_util.wanmei_api_sign(data, app_key, verbose=verbose)
    data["sign"] = sign
    # headers = {"Content-Type": "application/json"}
    headers = dict()
    response = requests.post(url, data=data, verify=False, headers=headers)
    if verbose:
        print("Request url=%s  param=%s " % (url, get_cutted_param_string(data)))
    if not 200 == response.status_code:
        raise ValueError("Something error status code =%s" % str(response.status_code))
    text = response.text
    result = json.loads(text)
    if "code" not in result or result["code"] != 0:
        if "message" in result:
            message = result["message"]
        else:
            message = "未知网络错误"
        raise ValueError(message)
    else:
        print("Response result : %s" % str(result))
        return result


def get_cutted_param_string(param):
    new_param = dict()
    for key in param:
        value = str(param[key])
        if len(value) > 500:
            value = value[:500]
        new_param[key] = value
    return str(new_param)


if __name__ == '__main__':
    pass
