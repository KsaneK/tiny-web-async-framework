import asyncio


class TinyWeb:
    READ_CHUNK_SIZE = 16 * 1024

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

        self._server = None
        self._loop = None

    def run(self):
        asyncio.run(self._run_server())

    async def _run_server(self):
        self._server = await asyncio.start_server(self._handle_request, self._host, self._port)
        async with self._server:
            await self._server.serve_forever()

    async def _handle_request(self, reader, writer):
        request = ""
        while not request.endswith("\r\n\r\n"):
            request += (await reader.read(TinyWeb.READ_CHUNK_SIZE)).decode("utf-8")

        writer.write("HTTP/1.1 200 OK\r\n\r\n<h1>Hello World!</h1>".encode("utf-8"))
        writer.close()
