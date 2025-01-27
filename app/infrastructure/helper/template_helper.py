from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader

base_path = Path(__file__).parent.parent.parent
env = Environment(loader=PackageLoader('app.infrastructure', 'template'))


def render_template(template: str, context: dict[str, Any] | None = None) -> str:
    if context is None:
        context = {}
    return str(env.get_template(template).render(**context))
