from handler.base_handler import BaseRequestHandler
from tool.convert import convert
from tool.convert import convert_return_image
from tool.convert import transparence2white
from io import BytesIO


class RemoveBackgroundHandler(BaseRequestHandler):

    async def post(self):
        # try:
        flag = self.request.body_arguments['flag'][0].decode(encoding='utf-8')  # 透明图的flag为true
        print('flag =', flag)
        image = self.request.files['image'][0]['body']

        if flag == 'false':
            result = convert(image)
            self.write({'code': 200, 'url': result[1]})
        else:
            image_result = convert_return_image(image)
            img_bytes = BytesIO()
            image_result.save(img_bytes, format='png')
            img_bytes = img_bytes.getvalue()
            result_white = transparence2white(img_bytes)
            self.write({'code': 200, 'url': result_white[1]})

    # except:
    #     self.write({'code': 500, 'msg': '服务器异常'})
