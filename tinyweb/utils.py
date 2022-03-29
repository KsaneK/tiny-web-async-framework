import os

import tinyweb.constants as C
from tinyweb.response import Response, StatusCode
from tinyweb.templates import render

ROOT_DIR = os.path.dirname(__file__)


def generate_error_response(status_code: StatusCode) -> Response:
    error_message = status_code.get_name().capitalize()
    response = Response.from_result(
        (
            render(
                template_path=os.path.join(
                    ROOT_DIR, C.TEMPLATES_DIR_NAME, C.ERROR_TEMPLATE_FILE_NAME
                ),
                context={"error_code": status_code.value, "error_message": error_message},
            ),
            status_code.value,
        )
    )
    return response
