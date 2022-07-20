import os
import sys
import uuid
import zipfile
import cv2
import numpy

import requests
from loguru import logger

logger.remove()
handler_id = logger.add(sys.stderr, level="INFO")


def get_project_path():
    """得到项目路径"""
    project_path = os.path.join(
        os.path.dirname(__file__),
    )
    return project_path


def zip_file(path):
    logger.debug(f'zip file from:{path}')
    start_dir = path  # 要压缩的文件夹路径
    file_news = start_dir + 'zips' + '.zip'  # 压缩后文件夹的名字

    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(start_dir):
        f_path = dir_path.replace(start_dir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        f_path = f_path and f_path + os.sep or ''  # 实现当前文件夹以及包含的所有文件的压缩
        for filename in file_names:
            z.write(os.path.join(dir_path, filename), f_path + filename)
    z.close()
    return file_news


def unzip_file(zip_src, dst_dir):
    logger.debug(f'unzip file to:{dst_dir}')

    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
        return True
    else:
        logger.error('this is not zip')
        return False


def save_to_seaweed(img):
    """
    先保存到临时文件夹，上传完成之后删除
    :param img:
    :return:
    """
    img_uuid = str(uuid.uuid1()).replace('-', '')
    img_url = f"http://192.168.200.71:8888/hamster/{img_uuid}.png"
    img_path = f'{get_project_path()}/temp/{img_uuid}.png'
    # if type(img) == numpy.ndarray:
    if isinstance(img, numpy.ndarray):  # cv2的格式与PIL.image的格式的save方式不一样
        cv2.imwrite(os.path.join(img_path), img)
    else:
        img.save(img_path)

    files = [
        ('', (f'{img_uuid}.png', open(img_path, 'rb'), 'image/png'))
    ]
    try:
        response = requests.request("POST", img_url, headers={}, data={}, files=files)
        if response.status_code == 201:
            logger.info(f"生成图片:{img_url}")
            return [200, img_url]
    except:
        return [500, 'save to seaweed failed']
    finally:
        os.remove(img_path)
