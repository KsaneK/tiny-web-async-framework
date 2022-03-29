import enum
import json
from typing import Dict, Any, Tuple, Union

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
        endpoint: str,
        args: Dict[str, str],
        method: RequestMethod,
        headers: Dict[str, str],
        body: str,
        http_version: str,
    ):
        self._path = path
        self._endpoint = endpoint
        self._args = args
        self._method = method
        self._headers = headers
        self._body = body
        self._http_version = http_version

    @property
    def path(self) -> str:
        return self._path

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def args(self) -> Dict[str, str]:
        return self._args

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
    def from_wsgi(environ: Dict[str, Any]) -> "Request":

        method = RequestMethod(environ["REQUEST_METHOD"])
        path = environ["REQUEST_URI"]
        endpoint = environ["PATH_INFO"]
        args = Request.parse_args(environ["QUERY_STRING"])
        http_version = environ["SERVER_PROTOCOL"]
        content_type = environ["CONTENT_TYPE"]
        try:
            content_length = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            content_length = 0
        body = environ["wsgi.input"].read(content_length)

        headers = {}

        for key, value in environ.items():
            if key.startswith("HTTP_"):
                header_name = key.replace("_", " ")
                headers[header_name] = value

        return Request(
            path=path,
            endpoint=endpoint,
            args=args,
            method=method,
            headers=headers,
            body=body,
            http_version=http_version,
        )

    @staticmethod
    def from_raw_bytes(raw_request: str):
        headers = {}
        first_line, rest = raw_request.split(LINE_END, maxsplit=1)
        method, path, http_version = first_line.split(" ")
        endpoint, args = Request.parse_path_and_args(path)
        headers_raw, body = rest.split(2 * LINE_END)
        for header_line in headers_raw.split(LINE_END):
            header_key, header_value = header_line.split(": ", maxsplit=1)
            headers[header_key] = header_value

        return Request(
            path=path,
            endpoint=endpoint,
            args=args,
            method=RequestMethod(method.upper()),
            headers=headers,
            body=body,
            http_version=http_version,
        )

    @staticmethod
    def parse_path_and_args(path: str) -> Tuple[str, Dict[str, Union[str, int, float, bool]]]:
        if "?" not in path:
            return path, {}

        endpoint, query_string = path.split("?")
        args = Request.parse_args(query_string)

        return endpoint, args

    @staticmethod
    def parse_args(query_string: str) -> Dict[str, Union[str, int, float, bool]]:
        args = query_string.split("&")

        args_dict = {}
        for raw_arg in args:
            if "=" not in raw_arg:
                args_dict[raw_arg] = True
                continue
            key, value = raw_arg.split("=", maxsplit=1)
            if value.isdigit():
                value = int(value)
            elif value.replace(".", "").isdigit():
                try:
                    value = float(value)
                except ValueError:
                    pass
            args_dict[key] = value

        return args_dict

    def __str__(self):
        return f"Request({self._method} {self.path})"

    def __repr__(self):
        return f"Request(path={self.path}, method={self._method})"
