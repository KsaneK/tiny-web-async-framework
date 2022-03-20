from typing import Callable

from tinyweb.exceptions import PageNotFoundException
from tinyweb.request import RequestMethod


class Routes:
    def __init__(self):
        self._route_map = {}

    def add_route(self, path: str, method: RequestMethod, func: Callable):
        self._route_map[(path, method)] = func

    def get_route(self, path: str, method: RequestMethod):
        if (path, method) not in self._route_map:
            raise PageNotFoundException(f"Path {path} not found")
        return self._route_map[(path, method)]
