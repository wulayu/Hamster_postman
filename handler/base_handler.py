from typing import Optional, Awaitable

from tornado import web

from utils import get_project_path
from loguru import logger


class BaseRequestHandler(web.RequestHandler):
    root_path = get_project_path()

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def err(self, status_code, msg):
        logger.error({'code': status_code, 'msg': msg})
        self.set_status(status_code)
        self.finish({'code': status_code, 'msg': msg})
