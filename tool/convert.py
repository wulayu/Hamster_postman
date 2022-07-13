import base64
from io import BytesIO

from PIL import Image

from rembg import remove
from utils import save_to_seaweed


def convert(image_base64):
    image = Image.open(BytesIO(image_base64))
    output = remove(image)
    return save_to_seaweed(output)


def convert_return_image(image_base64):
    image = Image.open(BytesIO(image_base64))
    output = remove(image)
    return output


def transparence2white(image_base64):
    img = Image.open(BytesIO(image_base64))
    # img = img.convert('RGBA')  # 此步骤是将图像转为灰度(RGBA表示4x8位像素，带透明度掩模的真彩色；CMYK为4x8位像素，分色等)，可以省略
    sp = img.size
    width = sp[0]
    height = sp[1]
    # print(sp)
    for yh in range(height):
        for xw in range(width):
            dot = (xw, yh)
            color_d = img.getpixel(dot)  # 与cv2不同的是，这里需要用getpixel方法来获取维度数据
            if color_d[3] == 0:
                color_d = (255, 255, 255, 255)
                img.putpixel(dot, color_d)  # 赋值的方法是通过putpixel
    return save_to_seaweed(img)
