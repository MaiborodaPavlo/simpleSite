from collections import defaultdict
import re

from controllers import ContentController
from response import BadResponse
from logger import logger


class Router:
    _routes = defaultdict(dict)
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(Router, cls).__new__(cls)
        return cls.instance

    @property
    def routes(self):
        return self._routes

    @classmethod
    def route(cls, url=None, method='GET', controller=None, action=None):
        cls._routes[url][method] = (controller, action)

    def routing(self, path, method, form_data=None):

        for pattern in self._routes.keys():
            match = re.fullmatch(pattern, path)
            if match is not None:
                path = pattern
                try:
                    param = match.group(1)
                except IndexError:
                    param = None
                break

        if match is None:
            return BadResponse()

        rules = self._routes[path]

        try:
            controller, action = rules[method]
        except KeyError:
            logger.warning(f'{method} for {path} not supported')
            return BadResponse(501, 'Not Implemented')

        cls = globals()[controller]
        func = cls.__dict__[action]
        obj = cls()

        if all([param, form_data]):
            response = func(obj, url_params=param, form_data=form_data)
        elif param is not None:
            response = func(obj, url_params=param)
        elif form_data is not None:
            response = func(obj, form_data=form_data)
        else:
            response = func(obj)

        return response



