import asyncio
import os
import platform
import subprocess
import threading

from fastapi import FastAPI, Response, Request

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
start_script = os.path.join(base_dir, "webui-user.bat")
print(base_dir)


def start_webui():
    try:
        # check if os is windows
        if platform.system() == "Windows":
            os.chdir(base_dir)
            subprocess.Popen(start_script, shell=True)
        elif platform.system() == "Linux":
            os.chdir(base_dir)
            subprocess.Popen("sh webui.sh", shell=True)
    except KeyboardInterrupt:
        print("killing webui...")


class CozyHttpServer:
    def __init__(self):
        self.app = FastAPI()
        self.register_routes()

    def register_routes(self):
        @self.app.get("/cozy-launcher/start")
        async def start():

            start_webui()

            return Response(status_code=200, content="pass")

        @self.app.get("/cozy-launcher/stop")
        async def stop():
            return Response(status_code=200, content="pass")

        @self.app.get("/cozy-launcher/ping")
        async def ping():

            # check if 127.0.0.1:7860 is returning a response
            import requests
            url = "http://127.0.0.1:7860"
            try:
                requests.get(url)
            except:
                return Response(status_code=500, content=f"fail to connect to {url}")

            return Response(status_code=200, content=f"{url} is responding")

    def run(self, host: str = "127.0.0.1", port: int = 8000):
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)
