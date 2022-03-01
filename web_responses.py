import os

from aiohttp import web

ROOT = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(ROOT, "frontend")


async def index(request):
    content = open(os.path.join(FRONTEND_DIR, "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def javascript(request):
    content = open(os.path.join(FRONTEND_DIR, "client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)


async def style(request):
    content = open(os.path.join(FRONTEND_DIR, "style.css"), "r").read()
    return web.Response(content_type="text/css", text=content)
