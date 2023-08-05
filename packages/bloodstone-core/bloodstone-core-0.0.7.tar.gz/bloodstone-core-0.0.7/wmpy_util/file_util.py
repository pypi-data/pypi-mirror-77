#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : WeiWang Zhang
@Time    : 2019-09-19 14:33
@File    : file_util.py
@Desc    : 文件操作工具类
"""
import os
import sys
import random
import shutil
from wmpy_util.time_util import timer
import time
import re
from wmpy_util import sys_util as su


class FilePrinter:
    __stdout_write__ = sys.stdout.write

    def __init__(self, file_path, mode='w', console=False, **kwargs):
        """
        将print形式输出的文字输出到文件中
        -------使用方式-------
        with(FilePrinter(file_path, "w")):
            print("Hello World")
        ---------------------
        :param file_path:
        :param mode:
        :param console: 是否同时输出文件和console
        """
        file_path = os.path.abspath(file_path)
        self.file_path = file_path
        check_dir(os.path.dirname(file_path), create=True)
        self.mode = mode
        self.fopen = None
        self.console = console

    def __enter__(self):
        # 重定向标准输出流
        sys.stdout.write = self.file_write
        self.fopen = open(self.file_path, mode=self.mode, encoding="utf-8")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.write = FilePrinter.__stdout_write__
        self.fopen.flush()
        self.fopen.close()

    def file_write(self, *args, **kwargs):
        arg_list = list(args)
        for index, arg in enumerate(arg_list):
            if not isinstance(arg, str):
                arg_list[index] = str(arg)
        message = " ".join(arg_list)
        # if message.strip() == "":
        #     # 通过print()打印信息时，会在输出完一行之后，再次调用输出换行符，导致logger中出现空白行
        #     return
        self.fopen.write(message)
        if self.console:
            FilePrinter.__stdout_write__(*args, **kwargs)


def get_temp_path(relative_folder=None):
    """
    获取一个临时文件目录
    :param relative_folder: 临时路径下的，相对路径
    :return:
    """
    # 根据不同的平台指定
    platform = sys.platform
    if platform == "darwin":
        # Mac系统
        temp_path = os.path.join(os.path.expanduser('~'), "temp")
    elif platform.startswith("win"):
        # Windows 系统
        # TODO 待定
        raise NotImplementedError("windows 临时路径待定")
    elif platform == "linux":
        temp_path = os.path.join(os.path.expanduser('~'), "temp")
    else:
        raise ValueError("未知系统平台:%s" % platform)
    check_dir(temp_path, create=True)
    # 补上相对路径
    if relative_folder is not None:
        temp_path = os.path.join(temp_path, relative_folder)
        check_dir(temp_path, create=True)
    print("Get tmp path：%s" % os.path.abspath(temp_path))
    return temp_path


def get_file_name(file_path):
    """
    返回不带路径及拓展名的文件名
    :param file_path:
    :return:
    """
    file_name = os.path.split(file_path)[1]
    file_name = os.path.splitext(file_name)[0]
    return file_name


def read_file(file_path):
    """
    读取文件
    :param file_path:
    :return:
    """
    fopen = open(file_path, 'r')
    result = ""
    for eachline in fopen:
        result += eachline
    return result


def read_file_lines(file_path):
    """
       按行读取文件
       :param file_path:
       :return:
       """
    fopen = open(file_path, 'r', encoding="UTF-8")
    for eachline in fopen:
        yield eachline
    fopen.close()


def write_to_file(file_path, data, encoding="utf-8", mode='w'):
    """
    往文件里写入信息
    :param filename:
    :param data:
    :return:
    """
    path = os.path.dirname(file_path)
    if not os.path.exists(path):
        os.mkdir(path)
    fopen = open(file_path, mode=mode, encoding=encoding)
    fopen.write(data)
    fopen.flush()
    fopen.close()


def write_array_to_file(file_path, array_data, split="\n", encoding="utf-8"):
    """
    往文件里写入信息
    :param filename:
    :param array_data:
    :return:
    """
    path = os.path.dirname(file_path)
    if not os.path.exists(path):
        os.mkdir(path)
    fopen = open(file_path, 'w', encoding=encoding)
    for text in array_data:
        fopen.write(text + split)
    fopen.flush()
    fopen.close()


def get_img_from_url(url, path, file_name):
    """
    从url上下载图片
    :param url:
    :param path:
    :param file_name:
    :return:
    """
    pass


def filter_image(files):
    """
    图片文件过滤器
    :param files:
    :return:
    """
    if not files:
        return
    for file in files:
        if is_image_file(file):
            yield file


def get_files(paths, filter_func=filter_image):
    """
    将目录下的所有文件返回为一个可迭代对象
    :param paths: 可以是一个路径列表，或是单条路径
    :param filter_func: 过滤函数接，接收一个文件名的list，返回另一个list或
    :return:
    """
    if isinstance(paths, str):
        paths = [paths]
    # 防止相同目录下的文件被重复加载
    root_set = set()
    for path in paths:
        for root, dirs, files in os.walk(path):
            if root in root_set:
                continue
            else:
                root_set.add(root)
            if callable(filter_func) and files is not None:
                files = filter_func(files)
            for file in files:
                yield os.path.join(root, file)


def is_image_file(file_name):
    if file_name is None:
        return False
    ext = file_name.split(".")[-1]
    if ext in IMG_FILE_EX:
        return True
    else:
        return False


def check_file(file_path):
    if file_path is None:
        return False
    if os.path.isfile(file_path):
        return True
    else:
        print("file not found path=%s" % str(file_path))
        return False


def check_dir(dir, create=False):
    if dir is None:
        return False
    if os.path.exists(dir):
        return True
    else:
        if create:
            # 为确保安全，一次只建一层路径
            os.mkdir(dir)
        return os.path.exists(dir)


def check_dirs(dir, *args, create=False):
    check_dir(dir, create)
    for arg in args:
        check_dir(arg, create)


def clear_path_file(path):
    """
    删除该目录下的所有文件
    :param path:
    :return:
    """
    if not os.path.isdir(path):
        return
    count = 0
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            count += 1
    print("Delete %d files under: %s" % (count, path))


def clear_path(path):
    """
    删除该目录下的所有文件及路径
    :param path:
    :return:
    """
    del_file_num, del_dir_num = __clear_path_iter(path, 0, 0)
    print("Delete %d files, %d dirs under: %s" % (del_file_num, del_dir_num, path))


def __clear_path_iter(path, del_file_num, del_dir_num):
    """
    清除目录的递归函数
    :param path: 待清除的目标路径
    :param del_file_num: 已经清除的文件数量
    :param del_dir_num: 已经清除的路径数量
    :return:
    """
    if not os.path.isdir(path):
        return del_file_num, del_dir_num
    files = os.listdir(path)
    files.sort(reverse=True)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            del_file_num += 1
        elif os.path.isdir(file_path):
            del_file_num, del_dir_num = __clear_path_iter(file_path, del_file_num, del_dir_num)
            try:
                os.removedirs(file_path)
            except FileNotFoundError as error:
                # something maybe wrong due to .DS_store on mac os, but doesn't matter.
                pass
            del_dir_num += 1
    return del_file_num, del_dir_num


def part_copy(from_path, to_path, ratio=1, sample_ext=("jpg", "png", "jpeg")):
    """
    按概率复制部分文件到指定路径，
    应用场景：线上数据集过大，想在本机做简单测试，奈何无法完成copy数据集合，智能先用脚本随机挑选出十分之一的数据
    然后搬移到线下做测试。
    :param from_path:
    :param to_path:
    :param ratio:
    :param sample_ext: 进行采样的文件拓展名，不在此列表里的文件则全部保留
    :return:
    """
    # 拓展名全部取小写
    sample_ext = [ext.lower() for ext in sample_ext]
    random.seed = time.time()
    ratio = float(ratio)
    from_abs = os.path.abspath(from_path)
    to_abs = os.path.abspath(to_path)
    check_dir(to_path, True)
    count = 0
    if not os.path.isdir(to_abs):
        raise ValueError("path: %s not a illegal" % to_abs)
    for root, dirs, files in os.walk(from_path):
        for directory in dirs:
            to_dir = replace_head_path(os.path.join(root, directory), from_abs, to_abs)
            check_dir(to_dir, create=True)
        for file in files:
            extend = os.path.splitext(file)[1]
            # 如果拓展名满足要求则随机选取，如果不满足要求则直接复制
            if extend.lower() in sample_ext:
                rand = random.random()
            else:
                rand = -1
            # 按概率选择文件
            if rand < ratio:
                from_file = os.path.abspath(os.path.join(root, file))
                to_file = replace_head_path(from_file, from_abs, to_abs)
                shutil.copy(from_file, to_file)
                if (count + 1) % 100 == 0:
                    print("Copy %d files" % count)
                count += 1


@timer(combine=True, batch=100)
def replace_head_path(path, old, new):
    """
    将地址的前缀替换
    FIXME 考虑之后替换成更高效的算法
    :param path:
    :param old:
    :param new:
    :return:
    """
    path = os.path.abspath(path)
    return path.replace(old, new)


def copy_file(file_src, to_file):
    to_path = os.path.split(to_file)[0]
    if not os.path.exists(to_path):
        os.makedirs(to_path)
    shutil.copy(file_src, to_file)


def compare_dir_based_on_name(dir1, dir2):
    """
    基于名称比较两个路径下的文件
    :param dir1:
    :param dir2:
    :return:
    """
    dir_files1 = os.listdir(dir1)
    dir_files2 = os.listdir(dir2)
    if not len(dir_files1) == len(dir_files2):
        return False
    dir_files1.sort(key=lambda x: str(x))
    dir_files2.sort(key=lambda x: str(x))
    return dir_files1 == dir_files2


IMG_FILE_EX = ["jpeg", 'jpg', 'png', 'bmp', 'jif']


def turn_py2_to_py3(dirname):
    for root, dirs, files in os.walk(dirname):
        for file in files:
            if not file.endswith(".py"):
                continue
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as fp:
                contents, flag = _scan_file(fp)
            # new_file_path = os.path.splitext(file_path)[0]+"_tmp.py"
            new_file_path = file_path
            if flag:
                print("Change file {}".format(new_file_path))
                write_array_to_file(new_file_path, contents)


def _scan_file(fp):
    content_list = list()
    change = False
    while True:
        line = fp.readline()
        if not line:
            break
        line, tmp = _print_transform(line)
        change |= tmp
        line, tmp = _xrange_transform(line)
        change |= tmp
        content_list.append(line.rstrip())
    return content_list, change


def _print_transform(line):
    change = False
    if line.strip().startswith("print"):
        index = line.find("print")
        rest = line[index + 5:]
        if not rest.strip().startswith("(") or not rest.strip().endswith(")"):
            line = line[:index + 5] + "(" + line[index + 5:].strip() + ")" + "\n"
            change = True
    return line, change


xrange_re = r"(?<![\w-])xrange(?![\w-])"


def _xrange_transform(line):
    line_new, num = re.subn(xrange_re, 'range', line, count=0)
    return line_new, num > 0


@timer
def count_line(file):
    count = 0
    for line in read_file_lines(file):
        count += 1
    return count


@timer
def count_line_faster(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    cmd = "wc -l {:s}".format(os.path.abspath(file_path))
    line = su.excute(cmd)
    number = line.strip().split(" ")[0]
    return int(number)


@timer
def split_file_to(source_file, start_line, end_line, target_file):
    """
    将文件中间的若干行分到另一个文件
    :param source_file:
    :param start_line: include
    :param end_line: include
    :param target_file:
    :return:
    """
    assert os.path.isfile(source_file)
    source_file = os.path.abspath(source_file)
    target_file = os.path.abspath(target_file)
    lines = end_line - start_line + 1
    cmd = "head -n {:d} {:s}|tail -n {:d} >> {:s}".format(end_line, source_file, lines, target_file)
    print(cmd)
    ret = su.excute(cmd)
    return ret


if __name__ == '__main__':
    import sys

    path = os.path.abspath(".")
    argv = sys.argv
    if len(argv) > 1:
        func = argv[1]
        args = argv[2:]
        eval_value = "%s(*args)" % func
        print("%s going to execute" % eval_value)
        print("Args = %s" % args)
        eval("%s(*args)" % func)
    else:
        # clear_path("/Users/zhangweiwang/workspace/dataset/segmentation1/")
        turn_py2_to_py3("./test")
        pass
