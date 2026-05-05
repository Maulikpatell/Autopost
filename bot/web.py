from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/", allow_head=True)
async def root(request):
    return web.json_response({"status": "running"})


@routes.get("/health")
async def health(request):
    return web.json_response({"ok": True})


async def start_web_server():
    app = web.Application(client_max_size=30000000)
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
