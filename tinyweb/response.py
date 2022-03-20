import enum
from typing import Dict

from tinyweb.constants import DEFAULT_HEADERS, HTTP_VERSION, LINE_END, ENCODING


class StatusCode(enum.Enum):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406

    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504

    def get_name(self):
        return self.name.replace("_", " ")


class DefaultResponses:
    NOT_FOUND = f"HTTP/1.1 {StatusCode.NOT_FOUND.value} " \
                f"{StatusCode.NOT_FOUND.get_name()}{2 * LINE_END}" \
                f"NOT FOUND!".encode(ENCODING)


class Response:
    def __init__(self, status_code: StatusCode, headers: Dict[str, str], body: str):
        self._status_code = status_code
        self._headers = headers
        self._body = body

    def generate(self):
        headers = {**DEFAULT_HEADERS, **self._headers, "Content-Length": len(self._body)}

        response_code_line = (
            f"{HTTP_VERSION} {self._status_code.value} {self._status_code.get_name()}"
        )
        header_list = [f"{key}: {value}" for key, value in headers.items()]
        raw_headers = LINE_END.join(header_list)

        raw_response = LINE_END.join([response_code_line, raw_headers, "", self._body])

        return raw_response.encode(ENCODING)

    @staticmethod
    def from_result(result):
        if isinstance(result, tuple):
            response, status_code = result
        else:
            response, status_code = result, 200

        return Response(status_code=StatusCode(status_code), headers={}, body=response)
