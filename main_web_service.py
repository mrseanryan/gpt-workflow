from http.server import BaseHTTPRequestHandler, HTTPServer
from random import randint
from urllib.parse import urlparse, parse_qs
import threading, socket

from config__database_schema_creator import EXPERT_COMMANDS
import core
import config
import config_web

chain = core.create_command_messages(EXPERT_COMMANDS)

# Python web server with cookie-based session
# based on https://davidgorski.ca/posts/sessions/

# TODO add sessions like gpt-rpg
previous_messages = []

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/":        self.bot
        }
        try:
            response = 200
            path = self.parse_path()
            print(f"req path: '{path}'")
            content = routes[path]()
        except Exception as error:
            print("!! error: ", error)
            response = 404
            content = "{ 'error': 'Oops! Not Found' }"

        self.send_response(response)
        self.send_header('Content-type','text/plain')
        self.end_headers()

        self.write(content)
        return

    def bot(self):
        user_prompt = self.parse_query_param("p")
        command_messages = core.create_command_messages(EXPERT_COMMANDS)
        rsp = core.execute_prompt(user_prompt, previous_messages, command_messages)
        return rsp

    def parse_path(self):
        return urlparse(self.path).path

    def parse_query_params(self):
        return parse_qs(urlparse(self.path).query)

    def parse_query_param(self, param):
        params = self.parse_query_params()
        if param in params:
            value_array = params[param]
            if value_array is None:
                return ""
            return value_array[0]
        return ""

    def write(self, content):
        self.wfile.write(bytes(content, "utf-8"))

def start_single_threaded():
    # Single threaded so can debug!
    webServer = HTTPServer((config_web.HOSTNAME, config_web.PORT), MyServer)
    print("Server started http://%s:%s" % (config_web.HOSTNAME, config_web.PORT))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")

def start_multi_threaded():
    # Multi-threaded server, else performance is terrible
    # ref https://stackoverflow.com/questions/46210672/python-2-7-streaming-http-server-supporting-multiple-connections-on-one-port
    #
    # Create ONE socket.
    addr = (config_web.HOSTNAME, config_web.PORT)
    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(5)

    # Launch many listener threads.
    class Thread(threading.Thread):
        def __init__(self, i):
            threading.Thread.__init__(self)
            self.i = i
            self.daemon = True
            self.start()
        def run(self):
            httpd = HTTPServer(addr, MyServer, False)

            # Prevent the HTTP server from re-binding every handler.
            # https://stackoverflow.com/questions/46210672/
            httpd.socket = sock
            httpd.server_bind = self.server_close = lambda self: None

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass
            httpd.server_close()

    print(f"Server started at http://{config_web.HOSTNAME}:{config_web.PORT} - {config_web.WEB_SERVER_THREADS} threads")
    print("Please set the 'p' query parameter to be the user's prompt.")
    print("example: http://localhost:8083/?p=I%20need%20a%20make%20a%20Car%20Parts%20application")
    print("[press any key to stop]")
    [Thread(i) for i in range(config_web.WEB_SERVER_THREADS)]
    input("Press ENTER to kill server")

    print("Server stopped.")

if __name__ == "__main__":
    if config.is_debug:
        start_single_threaded()
    else:
        start_multi_threaded()
