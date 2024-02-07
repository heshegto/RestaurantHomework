from fastapi.routing import APIRoute

from app.main import app


def take_url_base() -> dict[str, str]:
    url_base = {}
    for route in app.routes:
        if route is APIRoute:
            url_base[route.name] = route.path
    return url_base


def reverse(name: str) -> str:
    return take_url_base()[name]
