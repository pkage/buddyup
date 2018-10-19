#! /usr/bin/env python3

# for docs see:
# https://docs.aiohttp.org/en/stable/index.html

from aiohttp import web

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def redirect_to_index(req):
    raise web.HTTPFound('/index.html') 

app = web.Application()
app.add_routes([
    web.get('/{name}', handle),
    web.get('/', redirect_to_index),
    web.static('/static', './static')
])

web.run_app(app, debug=True)
