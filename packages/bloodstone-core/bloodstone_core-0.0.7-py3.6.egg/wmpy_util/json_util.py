#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : WeiWang Zhang
@Time    : 2019-09-19 14:33
@File    : json_util.py
@Desc    : json序列化工具类
"""
import os
import json
import numpy as np


def json_dump_file(file, data, minify=False):
    prefix, ext = os.path.splitext(file)
    if minify:
        if ext == "":
            ext = ".min.json"
        file = prefix + ext
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    else:
        if ext == "":
            ext = ".json"
        file = prefix + ext
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    return file


def minify_json_file(from_file, to_file):
    """
    压缩某个json文件
    :param from_file:
    :param to_file:
    :return:
    """
    with open(from_file, "r", encoding="utf-8") as f:
        datas = json.load(f)
        json_dump_file(to_file, datas, minify=True)


def read_json_file(file_path):
    if not os.path.isfile(file_path):
        raise IOError("File not existed! %s" % file_path)
    result = None
    with open(file_path, "r", encoding="utf-8") as f:
        result = json.load(f)
    return result


def json_power_dump(obj):
    """
    处理numpy无法序列化的问题
    :param obj:
    :return:
    """
    # ensure_ascii=False 选项保证中文不会被转成ascii码
    return json.dumps(obj, cls=NumpyEncoder, ensure_ascii=False)


# @timer(batch=100*1000)
def get_dict_type(dict_obj: dict):
    key, value = next(dict_obj.items().__iter__())
    return type(key), type(value)


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.core.floating):
            return float(obj)
        elif isinstance(obj, np.core.signedinteger):
            return int(obj)
        elif isinstance(obj, np.core.unsignedinteger):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    a = dict((i, 2 * i) for i in range(1000000))
    for i in range(1000 * 1000):
        get_dict_type(a)
