#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : WeiWang Zhang
@Time    : 2019-09-19 14:33
@File    : img_util.py
@Desc    : 图片处理工具类
"""
import os
import cv2
from numpy import ndarray, array
import numpy as np
import sys
import time
import base64
from PIL import Image
from collections import Iterable
from wmpy_util import hash_util
import re
import logging

logger = logging.getLogger("wmpy_util.img_util")

# 只在windows或mac环境绘制图像，linux省去该步骤
SHOW_IMG = sys.platform == "win32" or sys.platform == 'darwin'


def read_img(file_path, width=None, flags=1):
    if not os.path.exists(file_path):
        return None
    image = cv2.imread(file_path, flags=flags)
    if width is not None:
        shape = image.shape
        h_after_resize = int(shape[0] / shape[1] * width)
        image = cv2.resize(image, (width, h_after_resize))
    return image


def write_image(img, file_path, file_name):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    cv2.imwrite(os.path.join(file_path, file_name), img)


save_result = write_image


def write_tif_image(img, path, file_name):
    """
    存放tif格式的图片
    :param img:
    :param file_path:
    :param file_name:
    :return:
    """
    from libtiff import TIFF
    if not os.path.exists(path):
        os.makedirs(path)
    # 存储图片文件必须为tif格式
    if file_name.find(".tif") < 0:
        file_name += ".tif"
    file_path = os.path.join(path, file_name)
    out_tiff = TIFF.open(file_path, mode='w')
    out_tiff.write_image(img, compression=None, write_rgb=True)
    out_tiff.close()


def img_resize(img, dwidth=None, dheight=None):
    """
    :param img:
    :param dwidth:
    :param dheight: 如果只传高宽中的一个，则表示锁定高宽比
    :return:
    """
    height, width = img.shape[0:2]
    new_img = img
    # 如果参数为全None则返回原图
    if dwidth is None and dheight is None:
        return img
    elif dwidth is None:
        dheight = int(dheight)
        dwidth = int(dheight / height * width)
    elif dheight is None:
        dwidth = int(dwidth)
        dheight = int(dwidth / width * height)
    else:
        dwidth = int(dwidth)
        dheight = int(dheight)
    new_img = cv2.resize(img, dsize=(dwidth, dheight), interpolation=cv2.INTER_CUBIC)
    return new_img


def img_resize_with_shpae_zoom(img, shape_zoom):
    if not isinstance(shape_zoom, tuple):
        return img
    h_zoom, w_zoom = shape_zoom[0:2]
    height, width = img.shape[0:2]
    return cv2.resize(img, dsize=(int(width * w_zoom), int(height * h_zoom)), interpolation=cv2.INTER_CUBIC)


def extend_img(img, len=0, axis=0, align=0.5, fill_pix=0):
    """
    将图片沿指定坐标轴方向伸展
    :param img:
    :param len: 需要拓展的长度(支持负数，裁剪相应的长度)
    :param axis: 0-纵向拓展（增加height） 1-横向拓展（增加width）
    :param align: 0—1 拓展像素位于上方的比例，0-全部在下方拓展，1-全部在上方拓展
    :param fill_pix: 填充的像素颜色 0-255 0为黑色
    :return:
    """
    shape = np.asarray(img.shape, dtype=np.int32)
    if len == 0:
        return img
    if (len + shape[axis]) <= 0:
        raise ValueError("Error extend length = %s" % str(len))
    len_up = int(len * align)
    len_down = len - len_up

    if len_up > 0:
        shape[axis] = len_up
        up_part = np.ones(shape, dtype=np.uint8) * fill_pix
        img = np.concatenate((up_part, img), axis=axis)
    if len_down > 0:
        shape[axis] = len_down
        down_part = np.ones(shape, dtype=np.uint8) * fill_pix
        img = np.concatenate((img, down_part), axis=axis)
    # 支持图片裁剪
    if len < 0:
        low = abs(len_up)
        high = shape[axis] - abs(len_down)
        if axis == 0:
            img = img[low:high, :]
        else:
            img = img[:, low:high]
    return img


def img_resize_with_scale(img, dwidth, restrict_width_to_long_side=False):
    """
    :param img:
    :param dwidth:
    :param restrict_width_to_long_side
    :return:
    """
    if isinstance(img, ndarray):
        size = img.shape
    elif isinstance(img, list):
        img = array(img)
        size = img.size
        if len(size) < 2:
            return None
    else:
        return None
    height, width = size[0:2]
    if restrict_width_to_long_side:
        scale = dwidth / max(height, width)
    else:
        scale = dwidth / width
    dheight = int(height * scale)
    dwidth = int(width * scale)
    nImg = cv2.resize(img, dsize=(dwidth, dheight), interpolation=cv2.INTER_CUBIC)
    return nImg, scale


def draw_rectangle(image, region, fill=255, outline=1):
    """
    在图片上画一个矩形
    :param image:
    :param region:
    :return:
    """
    if region is not None:
        x, y, w, h = region
        cv2.rectangle(image, (x, y), (x + w, y + h), fill, outline)


def draw_rect_by_box(image, box, color=255, thickness=1):
    """
    根据cv2的Box对象(旋转矩阵)来绘制一个矩形框
    :param image:
    :param box:
    :param color: 填充的颜色
    :param thickness: 边缘的宽度，-1表示填满
    :return:
    """
    if len(box) == 5:
        box = ((box[0], box[1]), (box[2], box[3]), box[4])
    points = cv2.boxPoints(box)
    min_x, min_y = np.min(points, axis=0)
    max_x, max_y = np.max(points, axis=0)
    cv2.rectangle(image, (min_x, min_y), (max_x, max_y), color, thickness)


def draw_rect_for_text(img, text_result, location_multi=1):
    img_clone = np.array(img, dtype=np.uint8)
    for label in text_result:
        location = text_result[label]["location"]
        top = int(location["top"] * location_multi)
        left = int(location["left"] * location_multi)
        width = int(location["width"] * location_multi)
        height = int(location["height"] * location_multi)
        cv2.rectangle(img_clone, (left, top), (left + width, top + height), 128, 2)
    showimg(img_clone, "box_text")


max_win_width = 1000
max_win_height = 800
min_win_width = 150


def showimg(img, win_name=None, wait_flag=True):
    # linux环境不画图
    if not SHOW_IMG:
        return
    if isinstance(img, Image.Image):
        img = np.array(img, dtype=np.uint8)
    if win_name is None:
        win_name = "test_%d" % int(time.time())
    height, width = img.shape[0:2]
    if width > max_win_width:
        height = int(height / width * max_win_width)
        width = max_win_width
    if height > max_win_height:
        width = int(width / height * max_win_height)
        height = max_win_height
    if width < min_win_width:
        height = int(height * min_win_width / width)
        width = min_win_width
        img = img_resize(img, width)
    win_name = str(win_name)
    cv2.namedWindow(win_name, cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow(win_name, width, height)
    cv2.imshow(win_name, img)
    if wait_flag:
        cv2.waitKey(-1)


def animate(imgs, interval=50, win_name=None):
    assert interval > 0
    if win_name is None:
        win_name = "test_%d" % int(time.time())
    for img in imgs:
        cv2.imshow(win_name, img)
        cv2.waitKey(interval)


def img_joint(img_turple, axis=0, align=0.5, fill_pix=0):
    """
    横向拼接图片元组生成一张大图
    :param img_turple: array like object
    :param axis: 0-纵向拼接  1-横向拼接
    :param align: 0-向小坐标对其 0.5-居中 1-向大坐标对其
    :return:
    """
    if len(img_turple) < 1:
        raise ValueError("no pic param")
    if len(img_turple) == 1:
        return img_turple[0]

    # 选取图片数组当中维度最大的图片作为最终图片维度标准
    # 即如果有彩图则最后拼接结果为彩图，如果全是灰度图则最后的结果为灰度图
    max_shape_len = 0
    min_shape_len = 100
    for img in img_turple:
        img_shape_len = len(img.shape)
        max_shape_len = img_shape_len if img_shape_len > max_shape_len else max_shape_len
        min_shape_len = img_shape_len if img_shape_len < min_shape_len else min_shape_len

    if max_shape_len > 3 or min_shape_len < 2:
        raise ValueError("img joint error at wrong shape len: max=%d, min=%d" % (max_shape_len, min_shape_len))

    mask = np.ones((max_shape_len,), dtype=np.int32)
    mask[axis] = 0
    final_img = None
    for img in img_turple:
        shape = img.shape
        if len(shape) == 2 and max_shape_len == 3:
            img = img[:, :, np.newaxis]
            # 将灰度图转成伪彩图
            img = np.concatenate((img, img, img), axis=2)
        # elif len(shape) == 3 and max_shape_len == 2:
        #     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if final_img is None:
            # 初始化拼接整图
            final_shape = img.shape * mask
            final_img = np.zeros(final_shape, dtype=np.uint8)
        # 计算整图和待拼接图片的尺寸差
        shape_dif = (np.asarray(final_img.shape) - np.asarray(img.shape)) * mask
        # 补全尺寸
        for i in range(max_shape_len):
            dif_i = shape_dif[i]
            if dif_i > 0:
                img = enlarge(img, len=dif_i, axis=i, align=align, fill_pix=fill_pix)
            else:
                final_img = enlarge(final_img, len=-dif_i, axis=i, align=align, fill_pix=fill_pix)
        # 拼接图片
        final_img = np.concatenate((final_img, img), axis=axis)
    return final_img


def img_joint_with_colorgap(img_turple, axis=0, align=0.5, fill_pix=0, gap=2, gap_color=[0, 0, 0]):
    """
    拼接图片元组生成一张大图，并且在两张图片当中添加彩色的条状分割带
    :param img_turple: array like object
    :param axis: 0-纵向拼接  1-横向拼接
    :param align: 0-向小坐标对齐 0.5-居中 1-向大坐标对齐
    :param fill_pix: 填充像素的值 0-白色  255-黑色
    :param gap: 图片拼接的间隙
    :param gap_color: 间隙的颜色
    :return:
    """
    if len(img_turple) < 1:
        print("Error no pic to joint!")
        return None
    if len(img_turple) == 1:
        return img_turple[0]
    # 选取图片数组当中维度最大的图片作为最终图片维度标准
    # 即如果有彩图则最后拼接结果为彩图，如果全是灰度图则最后的结果为灰度图
    max_shape_len = 0
    final_shape = [0, 0]
    for img in img_turple:
        if img is None:
            continue
        img_shape_len = len(img.shape)
        max_shape_len = max(img_shape_len, max_shape_len)
        # final_shape[axis] += img.shape[axis] + gap
        final_shape[1 - axis] = max(final_shape[1 - axis], img.shape[1 - axis])
    if max_shape_len == 3:
        final_shape.append(3)
    final_img = np.ones(final_shape, dtype=np.uint8) * fill_pix
    final_shape[axis] = gap
    # 生成用于分割图片的彩条
    color_gap = gen_color_bar(final_shape, color=gap_color)

    for i in range(len(img_turple)):
        img = img_turple[i]
        if img is None:
            continue
        shape = img.shape
        if len(shape) == 2 and max_shape_len == 3:
            img = img[:, :, np.newaxis]
            # 将灰度图转成伪彩图
            img = np.concatenate((img, img, img), axis=2)
        # 计算整图和待拼接图片的尺寸差
        shape_dif = final_shape[1 - axis] - img.shape[1 - axis]
        # 补全尺寸
        img = extend_img(img, len=shape_dif, axis=1 - axis, align=align, fill_pix=fill_pix)
        # 拼接图片
        if i < len(img_turple) - 1:
            final_img = np.concatenate((final_img, img, color_gap), axis=axis)
        else:
            final_img = np.concatenate((final_img, img), axis=axis)
    return final_img


def gen_color_bar(shape, color):
    """
    得到一个纯色的图片条带
    :param shape:
    :param color:
    :return:
    """
    img_mat = None
    if len(shape) == 3:
        if not isinstance(color, Iterable):
            color = single_gray_to_bgr(color)
        img_mat = np.zeros(shape, dtype=np.uint8)
        img_mat[:, :, 0:3] = color
    elif len(shape) == 2:
        if isinstance(color, Iterable):
            color = single_bgr_to_gray(color)
        img_mat = np.ones(shape, dtype=np.uint8) * color
    return img_mat


def single_bgr_to_gray(color):
    """
    将bgr色彩转成灰度色彩
    :param color:
    :return:
    """
    if isinstance(color, list) or isinstance(color, tuple):
        b, g, r = color
        gray = (r * 19595 + g * 38469 + b * 7472) >> 16
    else:
        gray = color
    return gray


def single_gray_to_bgr(gray):
    """
    将灰度颜色值转成三原色表示
    :param gray:
    :return:
    """
    if isinstance(gray, list) or isinstance(gray, tuple):
        return gray
    return [gray, gray, gray]


def enlarge(img, len=0, axis=0, align=0.5, fill_pix=0):
    """
    将图片沿指定坐标轴方向伸展
    :param img:
    :param len:
    :param axis:
    :param align: 0-原图置顶，即全部向下延伸
                1-全部向上延伸
                0.5-均匀往两边延伸
    :return:
    """
    if len == 0:
        return img
    len_up = int(len * align)
    len_down = len - len_up
    shape = np.asarray(img.shape, dtype=np.int32)
    shape[axis] = len_up
    up_part = np.ones(shape, dtype=np.uint8) * fill_pix
    img = np.concatenate((up_part, img), axis=axis)
    shape[axis] = len_down
    down_part = np.ones(shape, dtype=np.uint8) * fill_pix
    img = np.concatenate((img, down_part), axis=axis)
    return img


def get_angle_from_transform(mat):
    """
    通过变换矩阵得到图片的旋转角度
    :param mat:
    :return:
    """
    mat = np.array(mat)
    if len(mat.shape) != 2:
        return 0
    h, w = mat.shape
    if h != 3 or w != 3:
        return 0
    # 抽取旋转矩阵
    rot_mat = mat[0:2, 0:2]
    # 缩放矩阵数值，确保旋转矩阵中sin和cos的平方和为1
    square_sum = np.sum(rot_mat * rot_mat)
    ratio = np.sqrt(2 / square_sum)
    rot_mat = rot_mat * ratio
    cos = rot_mat[0][0]
    sin = rot_mat[0][1]
    if cos > 1:
        cos = 1
    elif cos < -1:
        cos = -1
    angle = np.arccos(cos) / np.pi * 180
    if sin < 0:
        angle = -1 * angle
    return angle


def find_max_region(region_list):
    """
    找到能够包围区域的最大区域
    :param region_list: [region1,region2,....] region:[x,y,w,h]
    :return:
    """
    if len(region_list) == 0:
        raise ValueError("region list is empty")
    if len(region_list) == 1:
        return region_list[0]
    box_point_list = []
    for region in region_list:
        box_point_list.append(region_to_boxPoints(region))
    points = np.concatenate(box_point_list)
    xmin, ymin = np.min(points, axis=0)
    xmax, ymax = np.max(points, axis=0)
    max_region = [xmin, ymin, xmax - xmin, ymax - ymin]
    return max_region


def region_to_boxPoints(region, closed=False):
    """
    [x,y,w,h] -->  [point1, point2, point3, point4]
    :param region:
    :param closed: 曲线是否闭合
    :return:
    """
    if region is None:
        raise ValueError("region can not be None")
    if not len(region) == 4:
        raise ValueError("region size error")
    x_min, y_min, width, height = region
    x_max = x_min + width
    y_max = y_min + height
    # 逆时针走点
    points = [[x_min, y_min], [x_min, y_max], [x_max, y_max], [x_max, y_min]]
    if closed:
        points.append(points[0])
    return np.intp(points)


def boxPoints_to_region(bbox):
    """
    todo
    :param bbox:
    :return:
    """
    pass


def rect_to_region(rect):
    """
    todo
    :param rect:
    :return:
    """
    pass


def rect_to_array(rects):
    """
    将cv RotatedRect转换成为1*5的平铺向量
    :param rects:
    :return:
    """
    rect_array = []
    if rects is not None:
        for rect in rects:
            ang = None
            try:
                ((x, y), (w, h), ang) = rect
            except:
                if len(rect) == 5:
                    x, y, w, h, ang = rect
            if ang is not None:
                rect_array.append((x, y, w, h, ang))
    return rect_array


def rect_to_boxPoint(rects):
    """
    转换旋转矩形对象为边缘点集合
    :param rects:
    :return:
    """
    bboxes = []
    if rects is not None:
        for rect in rects:
            try:
                ((x, y), (w, h), ang) = rect
            except:
                if len(rect) == 5:
                    x, y, w, h, ang = rect
                else:
                    logger.error("Rect fomat error {}".format(str(rect)))
                    continue
            box = cv2.boxPoints(((x, y), (w, h), ang))
            bboxes.append(box)
    return bboxes


def get_fft_from_img(img_gray, show_it=False):
    """
    得到图片的傅里叶域分量，暂时只实现灰度图片的计算
    :param img_gray:
    :return:
    """
    f = np.fft.fft2(img_gray)
    fshift = np.fft.fftshift(f)
    if show_it:
        show_fft_result(fshift)
    return fshift


def show_fft_result(fft_result, win_name="fft", hold_window=True):
    # 取绝对值：将复数变化成实数
    # 取对数的目的为了将数据变化到0-255
    s1 = np.log(np.abs(fft_result))
    _max = np.max(s1)
    s1 = s1 / _max * 255
    s1 = np.array(s1, dtype=np.uint8)
    showimg(s1, win_name=win_name, wait_flag=hold_window)


def hist_equal(img):
    # hist_start = time.time()
    # clahe_size = 8
    # clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(clahe_size, clahe_size))
    # result = clahe.apply(img)
    # test

    # result = cv2.equalizeHist(img)
    image = img
    # if isinstance(img, cv2.UMat):
    #     image = img.get()  # UMat to Mat
    # else:
    #     image = img
    # result = cv2.equalizeHist(image)
    lut = np.ones(256, dtype=image.dtype)  # 创建空的查找表
    # lut = np.zeros(256)
    hist = cv2.calcHist([image],  # 计算图像的直方图
                        [0],  # 使用的通道
                        None,  # 没有使用mask
                        [256],  # it is a 1D histogram
                        [0, 256])
    minBinNo, maxBinNo = 0, 255
    # 计算从左起第一个不为0的直方图柱的位置
    for binNo, binValue in enumerate(hist):
        if binValue != 0:
            minBinNo = binNo
            break
    # 计算从右起第一个不为0的直方图柱的位置
    for binNo, binValue in enumerate(reversed(hist)):
        if binValue != 0:
            maxBinNo = 255 - binNo
            break
    # print minBinNo, maxBinNo
    # 生成查找表
    if maxBinNo == minBinNo:
        # 如果图像只有一种颜色，则直接返回原图
        return image
    for i, v in enumerate(lut):
        if i < minBinNo:
            lut[i] = 0
        elif i > maxBinNo:
            lut[i] = 255
        else:
            lut[i] = int(255.0 * (i - minBinNo) / (maxBinNo - minBinNo) + 0.5)
    # 计算,调用OpenCV cv2.LUT函数,参数 image --  输入图像，lut -- 查找表
    # print lut
    # TODO 这步影响很大，搞清楚为什么
    result = cv2.LUT(image, lut)
    # print type(result)
    # showimg(result)
    # hist_spend = time.time() - hist_start
    # logger.info("hist_equal spend = %d ms" % (int(hist_spend * 1000)))
    return result


def erode_in_region(image, pts, element, iter, recover=True):
    """
    在图片的指定区域内进行腐蚀
    :param image: 目标图片
    :param pts: list(point2f)
    :param element: 腐蚀或膨胀核函数
    :param iter: 迭代次数
    :param recover: 是否进行逆操作恢复
    :return:
    """
    np_pts = np.array(pts)
    max_x, max_y = np_pts.max(axis=0)
    min_x, min_y = np_pts.min(axis=0)
    # 选取区域并对其进行深拷贝
    region = image[min_y:max_y, min_x:max_x]
    reg_erode1 = cv2.erode(region, element, iterations=iter)
    if recover:
        # 做相同核函数的逆操作进行恢复
        reg_erode2 = cv2.dilate(reg_erode1, element, iterations=iter, borderType=cv2.BORDER_REPLICATE)
    else:
        reg_erode2 = reg_erode1
    # 塞入原图
    image[min_y:max_y, min_x:max_x] = reg_erode2
    return image


def img_file_to_base64(img_path):
    """
    将图片文件转成base64格式编码
    :param img_path:
    :return:
    """
    with open(img_path, "rb") as fp:
        base64_data = base64.b64encode(fp.read())
        base64_data = base64_data.decode("utf-8")
        return base64_data


def img_to_base64(img):
    """
    将ndarray格式的图片转为base64编码
    :param img:
    :return:
    """
    img_str = cv2.imencode(".jpg", img)[1].tostring()
    b64_code = base64.b64encode(img_str)
    return b64_code.decode("utf-8")


def get_card_xfeature_from_regions(img, regions, xfeature_width=600):
    """
    基于区域列表计算指定区域内的sift特征
    :param img:
    :param regions:   [region1,region2,region3,.....,regionx]， region格式[x,y,width,height]
    :param xfeature_width:
    :return:
    """
    if regions is not None and len(regions) > 0:
        mask = np.zeros(img.shape[0:2], dtype="uint8")
        for region in regions:
            draw_rectangle(mask, region, 255, -1)
        # showimg(mask, "Mask", True)
        get_card_xfeature(img, mask=mask, xfeature_width=xfeature_width)
    else:
        get_card_xfeature(img, mask=None, xfeature_width=xfeature_width)


def get_card_xfeature(img, mask=None, xfeature_width=None):
    """
    得到图片的sift特征
    :param img: 原图
    :param mask: 特征掩模，计算特征感兴趣区域
        Mask specifying where to look for keypoints (optional). It must be a 8-bit integer
        .   matrix with non-zero values in the region of interest.
    :param xfeature_width: 计算特征时原图的宽度尺寸,用更小的图片计算特征可以加速计算
    :return:
    """
    sift = cv2.xfeatures2d.SIFT_create()
    img_region = img
    if xfeature_width is not None:
        img_region = img_resize(img_region, xfeature_width)
        if mask is not None:
            mask = img_resize(mask, xfeature_width)
    # 确保掩模和图片是同一尺寸
    if mask is not None and (not img_region.shape[0:2] == mask.shape[0:2]):
        print("Error: mask for sift size wrong!!!")
        mask = cv2.resize(mask, img_region.shape[0:2])
    kp, des = sift.detectAndCompute(img_region, mask=mask)
    return kp, des


get_feature = get_card_xfeature


def get_img_from_request(request, key="image", max_size=4,
                         max_side_len=4096,
                         min_side_len=15,
                         rgb=False):
    """
    从post请求对象中获取图片参数，返回为标准cv2格式mat，颜色模式为BGR
    :param request:
    :param key:
    :param max_size: 图片最大体积 单位MB
    :param max_side_len: 图片最长边限制
    :param min_side_len: 图片最短边限制
    :param rgb: 是否以rgb模式返回，如果否则返回gbr形式
    :return:
    """
    img_file = request.FILES[key]
    file_size = img_file.size / 1048576
    if file_size > max_size:
        max_size_str = "%.1f" % max_size
        raise ValueError("图片体积过大，请缩小图片至 %s MB 以内" % max_size_str)
    image = Image.open(img_file, mode="r").convert("RGB")
    img_mat = np.asarray(image)
    if max(img_mat.shape[0:2]) > max_side_len or min(img_mat.shape[0:2]) < min_side_len:
        raise ValueError("图片最长边不能超过 %s，最短边不能小于 %s " % (max_side_len, min_side_len))
    if not rgb:
        img_mat = cv2.cvtColor(img_mat, cv2.COLOR_RGB2BGR)
    return img_mat


def img_resize_longer_size(img, d_width):
    """
    图片的长边缩放到dwidth长度
    :param img:
    :param d_width:
    :return: 返回缩放后的图片，以及该图片是原图片的多少倍
    """
    size = None
    if isinstance(img, np.ndarray):
        size = img.shape
    elif isinstance(img, list):
        img = np.array(img)
        if len(img.size) >= 2:
            size = img.size
    if size is None:
        raise ValueError("Illegal img param")
    height, width = size[0:2]
    scale = d_width / max(height, width)
    d_height = int(height * scale)
    d_width = int(width * scale)
    n_img = cv2.resize(img, dsize=(d_width, d_height), interpolation=cv2.INTER_CUBIC)
    return n_img, scale


def img_hash(img_array, *args, **kwargs):
    """
    计算图片的md5
    :param img_array:
    :return:
    """
    img_str = str(img_array)
    if args:
        img_str += str(args)
    if kwargs:
        img_str += str(kwargs)
    return hash_util.md5(img_str)


def draw_label_on_img(img, label, bg_color=(255, 0, 0), word_color=(255, 255, 255), scale=0.3, thickness=1,
                      position="top-left"):
    """
    在图片上绘制指定的label信息
    :param img:
    :param label: 要绘制的文字
    :param bg_color: 文字绘制的背景
    :param scale: 字体缩放，使用cv2默认字体
    :param position: 标签位置的文字性描述，方位词只包括 top,left,bottom,right
                    写法：top-left,left-top均可
                    连接词：bottom-right,bottom_right,bottom.right均可
    :return:
    """
    shape = img.shape
    if len(shape) == 2:
        if isinstance(bg_color, list) or isinstance(bg_color, tuple):
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    else:
        bg_color = single_gray_to_bgr(bg_color)
    font = cv2.FONT_HERSHEY_SIMPLEX  # 使用默认字体
    size, textSize = cv2.getTextSize(label, font, scale, thickness)
    img_height, img_width = shape[0:2]
    text_width, text_height = size
    padding = [0, 0, 2, 0]  # top, right, bottom, left
    top, right, bottom, left = (0, img_width - 1, img_height - 1, 0)
    position = str(position).lower()
    reg = r"^(top|right|bottom|left)[_\-\.](top|right|bottom|left)$"
    match = re.match(reg, position)
    if match is None or (match.group(1) == match.group(2)):
        print("Position =%s error" % position)
        return None
    if "top" in position:
        bottom = top + text_height + padding[0] + padding[2]
    if "right" in position:
        left = right - text_width - padding[1] - padding[3]
    if "bottom" in position:
        top = bottom - text_height - padding[0] - padding[2]
    if "left" in position:
        right = left + text_width + padding[1] + padding[3]
    cv2.rectangle(img, (left, top), (right, bottom), bg_color, thickness=-1)
    cv2.putText(img, label, (left + padding[3], bottom - padding[2]), fontFace=font, fontScale=scale,
                color=word_color, thickness=thickness)
    return img


def draw_text(image, text, center=None, font=None, color=(255, 255, 255), size=1, thickness=3):
    """

    :param image:
    :param text:
    :param center:
    :param font:
    :param color:
    :param size:
    :param thickness:
    :return:
    """
    img_h, img_w = image.shape[:2]
    if center is None:
        center = [img_w / 2, img_h / 2]
    if font is None:
        font = cv2.FONT_HERSHEY_SIMPLEX
    # 检测绘制文字大小
    box_size, _ = cv2.getTextSize(text, font, size, thickness)
    text_width, text_height = box_size
    left, bottom = center[0] - text_width / 2, center[1] + text_height / 2
    left, bottom = int(left), int(bottom)
    cv2.putText(image, text, (left, bottom), fontFace=font, fontScale=size,
                color=color, thickness=thickness)


def crop_from_image(image, rect):
    """
    根据矩形框从图像上切除相应的像素区域
    :param image:
    :param rect: cv2 RotatedRect旋转矩形对象，数据格式如此:((x,y), (w,h), angle)
    :return:
    """
    h, w = image.shape[:2]
    try:
        cx, cy, wb, hb, angle = rect
    except Exception as error:
        (cx, cy), (wb, hb), angle = rect
    if abs(angle) > 5:
        rotate_mat = cv2.getRotationMatrix2D((cx, cy), angle, 1)
        rotated = cv2.warpAffine(image, rotate_mat, (w, h), borderValue=(255, 255, 255))
    else:
        rotated = image
    left = max(0, round(cx - wb / 2))
    top = max(0, round(cy - hb / 2))
    right = min(w, round(cx + wb / 2))
    bottom = min(h, round(cy + hb / 2))
    cropped = rotated[top:bottom, left:right, :]
    return cropped


def crop_from_image_faster(image, rect):
    """
    根据矩形框从图像上切除相应的像素区域, 加速版
    :param image:
    :param rect: cv2 RotatedRect旋转矩形对象，数据格式如此:((x,y), (w,h), angle)
    :return:
    """
    try:
        rect_x, rect_y, rect_w, rect_h, angle = rect
    except:
        (rect_x, rect_y), (rect_w, rect_h), angle = rect
    bboxes = cv2.boxPoints(((rect_x, rect_y), (rect_w, rect_h), angle))
    left, top = np.intp(np.min(bboxes, axis=0))
    right, bottom = np.intp(np.max(bboxes, axis=0))
    # 先获取近似剪切框，在旋转角度不大时可以省去旋转时间
    cropped = image[top:bottom, left:right, :]
    if abs(angle) > 1:
        # 对于旋转角度大于1度的图片，对近似剪切框进行旋转（避免了对原图旋转浪费算力），而后进行剪裁
        crop_h, crop_w = cropped.shape[:2]
        rotate_mat = cv2.getRotationMatrix2D((crop_w / 2, crop_h / 2), angle, 1)
        cropped = cv2.warpAffine(cropped, rotate_mat, (crop_w, crop_h), borderValue=(255, 255, 255))
        bboxes = cv2.boxPoints(((crop_w / 2, crop_h / 2), (rect_w, rect_h), 0))
        left, top = np.intp(np.min(bboxes, axis=0))
        right, bottom = np.intp(np.max(bboxes, axis=0))
        cropped = cropped[top:bottom, left:right, :]
    return cropped


if __name__ == '__main__':
    pass
