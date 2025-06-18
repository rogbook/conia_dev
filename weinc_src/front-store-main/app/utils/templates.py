import typing
from pathlib import Path
from fastapi.templating import Jinja2Templates

from app.utils.common_utils import phone_format, add_date_str, get_youtube_src, get_vimeo_src, component_item_visible, custom_round

try:
    import jinja2

    if hasattr(jinja2, "pass_context"):
        pass_context = jinja2.pass_context
    else:  # pragma: nocover
        pass_context = jinja2.contextfunction  # type: ignore[attr-defined]
except ImportError:  # pragma: nocover
    jinja2 = None  # type: ignore

current_file = Path(__file__)
current_file_dir = current_file.parent
project_root = current_file_dir.parent
project_root_absolute = project_root.resolve()
templates_root_absolute = project_root_absolute / "templates"


@pass_context  # noqa
def url_for(context: dict, name: str, **path_params: typing.Any) -> str:
    request = context["request"]
    http_url = request.url_for(name, **path_params)
    if request.url.scheme == 'https' or "x-forwarded-for" in request.headers.keys():
        return http_url.replace("http", "https", 1)
    else:
        return http_url


templates = Jinja2Templates(directory=templates_root_absolute, extensions=["jinja2.ext.loopcontrols"])
templates.env.globals["url_for"] = url_for
templates.env.filters["phone_format"] = phone_format
templates.env.filters["add_date_str"] = add_date_str
templates.env.filters["get_youtube_src"] = get_youtube_src
templates.env.filters["get_vimeo_src"] = get_vimeo_src
templates.env.filters["component_item_visible"] = component_item_visible
templates.env.filters["custom_round"] = custom_round
