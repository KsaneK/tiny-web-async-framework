import enum
import json
from typing import Dict, Any

from tinyweb.constants import LINE_END


class RequestMethod(enum.Enum):
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"


class Request:
    def __init__(
        self,
        path: str,
        method: RequestMethod,
        headers: Dict[str, str],
        body: str,
        http_version: str,
    ):
        self._path = path
        self._method = method
        self._headers = headers
        self._body = body
        self._http_version = http_version

    @property
    def path(self) -> str:
        return self._path

    @property
    def method(self) -> RequestMethod:
        return self._method

    @property
    def headers(self) -> Dict[str, str]:
        return self._headers

    @property
    def http_version(self) -> str:
        return self._http_version

    def json(self) -> Dict[Any, Any]:
        return json.loads(self._body)

    @staticmethod
    def parse(raw_request: str):
        headers = {}
        first_line, rest = raw_request.split(LINE_END, maxsplit=1)
        method, path, http_version = first_line.split(" ")
        headers_raw, body = rest.split(2 * LINE_END)
        for header_line in headers_raw.split(LINE_END):
            header_key, header_value = header_line.split(": ", maxsplit=1)
            headers[header_key] = header_value

        return Request(
            path=path,
            method=RequestMethod(method.upper()),
            headers=headers,
            body=body,
            http_version=http_version,
        )

    def __str__(self):
        return f"Request({self._method} {self._path})"

    def __repr__(self):
        return f"Request(path={self._path}, method={self._method})"
