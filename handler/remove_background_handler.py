from handler.base_handler import BaseRequestHandler
from tool.convert import convert


class RemoveBackgroundHandler(BaseRequestHandler):

    async def post(self):
        try:
            image = self.request.files['image'][0]['body']
            result = convert(image)
            self.write({'code': 200, 'url': result[1]})
        except:
            self.write({'code': 500, 'msg': '服务器异常'})
