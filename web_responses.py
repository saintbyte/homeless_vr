import os

from aiohttp import web

ROOT = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(ROOT, "frontend")


def _get_frontend_file_path(file: str) -> str:
    return os.path.join(FRONTEND_DIR, file)


async def index(request):
    content = open(_get_frontend_file_path("index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def javascript(request):
    content = open(_get_frontend_file_path("client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)


async def style(request):
    content = open(_get_frontend_file_path("style.css"), "r").read()
    return web.Response(content_type="text/css", text=content)
