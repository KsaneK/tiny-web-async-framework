from typing import Dict

from jinja2 import Template


def render(template_path: str, context: Dict = None) -> str:
    with open(template_path) as template_file:
        template = Template(template_file.read())
    return template.render(**context or {})
