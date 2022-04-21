import os

from aiohttp import web

ROOT = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(ROOT, "frontend")


def _get_frontend_file_path(file: str) -> str:
    return os.path.join(FRONTEND_DIR, file)


async def index(request):
    content = open(_get_frontend_file_path("index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def data_channel_test(request):
    content = open(_get_frontend_file_path("data_channel_test.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def javascript(request):
    content = open(_get_frontend_file_path("client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)


async def style(request):
    content = open(_get_frontend_file_path("style.css"), "r").read()
    return web.Response(content_type="text/css", text=content)


async def fulltilt_min_js(request):
    content = open(_get_frontend_file_path("fulltilt.min.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)
