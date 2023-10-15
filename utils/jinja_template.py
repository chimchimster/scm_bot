import pathlib

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .jinja_filters import round_float_value

template_env = Environment(loader=FileSystemLoader(
        pathlib.Path.cwd() / 'templates'
    ),
    autoescape=select_autoescape(['html']),
    enable_async=True,
)

template_env.filters['round_float_value'] = round_float_value


async def render_template(template_name: str, **context) -> str:

    template = template_env.get_template(template_name)
    html = await template.render_async(context)

    return html
