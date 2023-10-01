import pathlib
from jinja2 import Environment, FileSystemLoader, select_autoescape


template_env = Environment(loader=FileSystemLoader(
        pathlib.Path.cwd() / 'templates'
    ),
    autoescape=select_autoescape(['html'])
)


async def render_template(template_name: str, **context) -> str:

    template = template_env.get_template(template_name)
    html = template.render(context)

    return html
