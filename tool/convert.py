import base64
from io import BytesIO

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
