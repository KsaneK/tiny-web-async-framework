import asyncio
from typing import List

import tinyweb.constants as C
from tinyweb.exceptions import PageNotFoundException
from tinyweb.logger import log, RequestLogger
from tinyweb.request import Request, RequestMethod
from tinyweb.response import Response, StatusCode
from tinyweb.routes import Routes
from tinyweb.utils import generate_error_message


@log(RequestLogger)
class TinyWeb:
    READ_CHUNK_SIZE = 16 * 1024

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

        self._server = None

        self._routes = Routes()

    def run(self):
        self.logger.info(f"Starting webserver on {self._host}:{self._port}...")
        asyncio.run(self._run_server())

    async def _run_server(self):
        self._server = await asyncio.start_server(self._handle_request, self._host, self._port)
        async with self._server:
            await self._server.serve_forever()

    async def _handle_request(self, reader, writer):
        raw_request = await self._read_http_request_from_stream(reader)

        try:
            request = Request.parse(raw_request=raw_request)
        except Exception:
            self.logger.error("Couldn't parse request")
            writer.close()
            return

        try:
            func = self._routes.get_route(request.path, request.method)
            response_obj = Response.from_result(func(request))
            response = response_obj.generate()
            status = response_obj.status_code
        except PageNotFoundException:
            response = generate_error_message(StatusCode.NOT_FOUND)
            status = StatusCode.NOT_FOUND
        except Exception:
            response = generate_error_message(StatusCode.INTERNAL_SERVER_ERROR)
            status = StatusCode.INTERNAL_SERVER_ERROR

        self.logger.log(request=request, status_code=status.value)

        writer.write(response)
        writer.close()

    @staticmethod
    async def _read_http_request_from_stream(stream) -> str:
        raw_request = ""
        while not raw_request.endswith(2 * C.LINE_END):
            raw_request += (await stream.read(TinyWeb.READ_CHUNK_SIZE)).decode(C.ENCODING)

        return raw_request

    def route(self, path: str, methods: List[str]):
        def decorator(func):
            for method in methods:
                self._routes.add_route(path, RequestMethod(method), func)
            return func

        return decorator
