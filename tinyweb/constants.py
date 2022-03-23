LINE_END = "\r\n"
ENCODING = "utf-8"
HTTP_VERSION = "HTTP/1.1"
TEMPLATES_DIR_NAME = "templates"
ERROR_TEMPLATE_FILE_NAME = "error.html"
REQUEST_LOG_TEMPLATE = '"{method} {path} {http_version}" - {status_code}'

DEFAULT_HEADERS = {
    "Server": "TinyWeb",
    "Content-Type": "text/html",
}
