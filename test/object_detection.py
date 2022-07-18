import os
import cv2
import numpy as np

np.set_printoptions(threshold=np.inf)

source = "../output/rembg/"
out_path = "../output/object_detection/"
if not os.path.isdir(out_path):
    os.mkdir(out_path)


def add_alpha_channel(img):
    """ 为jpg图像添加alpha通道 """
    b_channel, g_channel, r_channel = cv2.split(img)  # 剥离jpg图像通道
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255  # 创建Alpha通道
    img_new = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))  # 融合通道
    return img_new


def object_detect(img):
    sp = img.shape
    print(sp)
    width = sp[1]
    height = sp[0]
    top = -1
    bottom = -1
    left = -1
    right = -1
    judge = 10  # 判决门限,门限值越大框越小

    for yh in range(height):
        count = 0
        for xw in range(width):
            color_a = img[yh][xw][3]
            if color_a != 0:
                count += 1
                if count > judge:
                    top = yh
                    break
        if top != -1:
            break
    for yh in reversed(range(height)):
        count = 0
        for xw in range(width):
            color_a = img[yh][xw][3]
            if color_a != 0:
                count += 1
                if count > judge:
                    bottom = yh
                    break
        if bottom != -1:
            break
    for xw in range(width):
        count = 0
        for yh in range(height):
            color_a = img[yh][xw][3]
            if color_a != 0:
                count += 1
                if count > judge:
                    left = xw
                    break
        if left != -1:
            break
    for xw in reversed(range(width)):
        count = 0
        for yh in range(height):
            color_a = img[yh][xw][3]
            if color_a != 0:
                count += 1
                if count > judge:
                    right = xw
                    break
        if right != -1:
            break

    # center = ((left + right) / 2, (top + bottom) / 2)
    _box = [left, top, right, bottom]
    print('box =', _box)
    return _box


if __name__ == "__main__":
    for index, file_name in enumerate(os.listdir(source)):
        if file_name != 'output_10.png':
            continue
        input_path = file_name
        output_name = 'output_with_box_' + str(index) + '.png'
        output_part_name = 'output_part_' + str(index) + '.png'

        _input = cv2.imread(os.path.join(source, input_path),  # 读入商品透明图图片
                            flags=cv2.IMREAD_UNCHANGED)  # "IMREAD_UNCHANGED"指定用图片的原来格式打开，以读取透明度，不加时只有rgb

        box = object_detect(_input)  # 识别box位置
        box_color = (255, 0, 255, 255)  # 设置box参数，必须设置不透明度
        result = cv2.rectangle(_input, (box[0], box[1]), (box[2], box[3]), color=box_color, thickness=2)  # 给商品加box
        part_box = _input[box[1] + 2:box[3] - 2, box[0] + 2:box[2] - 2]  # 得到box中的商品图
        part_resize = cv2.resize(part_box, (370, 370), interpolation=cv2.INTER_AREA)  # 将商品图调整大小

        background = cv2.imread("thumbnail.jpg", flags=cv2.IMREAD_UNCHANGED)  # 读取背景图
        background = add_alpha_channel(background)  # 背景图为jpg需要添加alpha通道
        # 将png商品图贴到jpg背景
        alpha_png = part_resize[:, :, 3] / 255.0  # alpha通道归一化为0-1
        print(part_resize[0: 370, 0: 370, 3])
        alpha_jpg = 1 - alpha_png
        for c in range(0, 3):
            background[410:780, 20:390, c] = (
                    alpha_jpg * background[410:780, 20:390, c] + alpha_png * part_resize[:, :, c])

        # cv2.imshow('object', _input)
        # cv2.imshow('part', part_box)
        # cv2.imshow('part_resize', part_resize)
        cv2.imshow('pasted', background)
        cv2.waitKey(10000)
        cv2.imwrite(os.path.join(out_path, output_name), _input)
        cv2.imwrite(os.path.join(out_path, output_part_name), part_box)
