from io import BytesIO

from handler.base_handler import BaseRequestHandler
from tool.convert import convert_url, convert_image, add_white_bg
from utils import logger


class RemoveBackgroundHandler(BaseRequestHandler):

    async def post(self):
        # try:
        transparent = self.request.body_arguments['transparent'][0].decode(encoding='utf-8')
        logger.info(f'是否为透明图 {transparent}')
        image = self.request.files['image'][0]['body']
        if transparent == 'true':
            result = convert_url(image)
            self.write({'code': 200, 'url': result[1]})
        else:
            transparent_image = convert_image(image)
            img_bytes = BytesIO()
            transparent_image.save(img_bytes, format='png')
            img_bytes = img_bytes.getvalue()
            white_bg_image = add_white_bg(img_bytes)
            self.write({'code': 200, 'url': white_bg_image[1]})

    # except:
    #     self.write({'code': 500, 'msg': '服务器异常'})
