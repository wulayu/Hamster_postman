from tornado import web, ioloop

from handler.remove_background_handler import RemoveBackgroundHandler

from utils import logger, get_project_path

root_path = get_project_path()

urlpatterns = [
    web.url(r'/remove_bg', RemoveBackgroundHandler),
]
settings = dict(
    debug=False,
)


def start_server():
    app = web.Application(urlpatterns, **settings)
    app.listen(9998)
    logger.info('Start forward proxy server on port {}'.format(9998))
    ioloop.IOLoop.current().start()


start_server()
