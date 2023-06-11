import threading

from extensions.CozyLauncher.http_server import CozyHttpServer
import extensions.CozyLauncher.socket_server as socket_server


def start_servers():
    stopper = threading.Event()
    socket_server.main(stopper)

    http_server = CozyHttpServer()

    http_server.run()


if __name__ == "__main__":
    start_servers()
