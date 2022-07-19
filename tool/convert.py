import cv2
from io import BytesIO
import numpy as np

from PIL import Image

from rembg import remove
from utils import save_to_seaweed


def convert_url(image_base64):
    image = Image.open(BytesIO(image_base64))
    output = remove(image)
    return save_to_seaweed(output)


def convert_image(image_base64):
    image = Image.open(BytesIO(image_base64))
    output = remove(image)
    return output


def add_white_bg(image_base64):
    img = Image.open(BytesIO(image_base64))
    width = img.size[0]
    height = img.size[1]
    r, g, b, a = img.split()
    result = Image.new("RGB", (width, height), (255, 255, 255))
    result.paste(img, mask=a)

    return save_to_seaweed(result)


def object_detect(image_base64):  # 返回box的四周坐标
    img = cv2.imdecode(np.array(bytearray(image_base64), dtype='uint8'), cv2.IMREAD_UNCHANGED)  # 从二进制图片数据中读取
    sp = img.shape
    # print('img.shape =', sp)
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
    box = [left, top, right, bottom]
    box_color = (255, 0, 255, 255)  # 设置box参数，必须设置不透明度

    result = cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color=box_color, thickness=2)  # 给商品加box
    part_box = img[box[1] + 2:box[3] - 2, box[0] + 2:box[2] - 2]  # 得到box中的商品图
    part_resize = cv2.resize(part_box, (370, 370), interpolation=cv2.INTER_AREA)  # 将商品图调整大小

    return save_to_seaweed(part_box)
