from aiohttp import web
import os

routes = web.RouteTableDef()

@routes.get("/")
async def root(request):
    return web.json_response({"status": "running"})

async def start_web_server():
    app = web.Application()
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", 8000))
    site = web.TCPSite(runner, "0.0.0.0", port)

    await site.start()
