from io import BytesIO

from PIL import Image

from rembg import remove
from utils import save_to_seaweed


def convert(image_base64):
    image = Image.open(BytesIO(image_base64))
    output = remove(image)
    return save_to_seaweed(output)
