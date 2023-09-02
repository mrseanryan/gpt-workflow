from http.server import BaseHTTPRequestHandler, HTTPServer
import traceback
from urllib.parse import urlparse, parse_qs
import urllib
import threading, socket

from prompts_dot_graph_creator import EXPERT_COMMANDS, GetPromptToDescribeWorkflow, getExpertCommandToCreateDot, getExpertCommandToDescribeDot
import core
import config
import config_web

# Python web server with cookie-based session
# based on https://davidgorski.ca/posts/sessions/

# TODO add sessions like gpt-rpg
previous_messages = []

prompt_id = 1

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/generate-dot":        self.bot_generate_dot,
            "/describe-dot":        self.bot_describe_dot,
        }
        try:
            response = 200
            path = self.parse_path()
            print(f"req path: '{path}'")
            content = routes[path]()
        except Exception as error:
            print("!! error: ", error)
            traceback.print_exc() # print stack trace
            response = 404
            content = "{ 'error': 'Oops! Not Found' }"

        self.send_response(response)
        self.send_header('Content-type','text/plain')
        self.end_headers()

        self.write(content)
        return

    def bot_describe_dot(self):
        global prompt_id
        user_prompt = self.parse_query_param("p")
        print(f"  {user_prompt}")
        user_prompt_wrapped = GetPromptToDescribeWorkflow(user_prompt)
        command_messages = core.create_command_messages([getExpertCommandToDescribeDot()])
        if config_web.discard_previous_messages:
            previous_messages = []
        rsp = core.execute_prompt(user_prompt_wrapped, previous_messages, command_messages, prompt_id)
        prompt_id += 1
        return rsp

    def bot_generate_dot(self):
        global prompt_id
        DELIMITER = "======"
        EMPTY_DOT = "digraph G{}"
        user_prompt = self.parse_query_param("p")
        print(f"  {user_prompt}")
        command_messages = core.create_command_messages([getExpertCommandToCreateDot()])
        if config_web.discard_previous_messages:
            previous_messages = []
        rsp = core.execute_prompt(user_prompt, previous_messages, command_messages, prompt_id)
        prompt_id += 1
        if "human_output" in rsp:
            return rsp["human_output"] + f"\n\n{DELIMITER}\n\n" + rsp["dot"]
        else:
            print("!! error rsp? - cannot parse")
            print(rsp)
            return f"{rsp}\n\n{DELIMITER}\n\n{EMPTY_DOT}"

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

def quotify(text):
    return urllib.parse.quote(text)

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

    escaped_create_dot = quotify("Create a flow that makes a series of decisions about whether to approve a mortgage application")
    escaped_dot = quotify('digraph G { Start_Start_1[shape=ellipse, label="Start_1" ];  Decision_Experience[shape=Mdiamond, label="Experience" ];  Decision_Education[shape=Mdiamond, label="Education" ];  Decision_Skills[shape=Mdiamond, label="Skills" ];  End_Recommend[shape=rectangle, label="Recommend" ];  End_Not_Recommend[shape=rectangle, label="Not_Recommend" ];  Start_Start_1 -> Decision_Experience;  Decision_Experience -> Decision_Education [label="true"];  Decision_Experience -> End_Not_Recommend [label="false"];  Decision_Education -> Decision_Skills [label="true"];  Decision_Education -> End_Not_Recommend [label="false"];  Decision_Skills -> End_Recommend [label="true"];  Decision_Skills -> End_Not_Recommend [label="false"];}")}')

    print(f"Server started at http://{config_web.HOSTNAME}:{config_web.PORT} - {config_web.WEB_SERVER_THREADS} threads")
    print("Please set the 'p' query parameter to be the user's prompt.")
    print(f"- generate DOT example: http://{config_web.HOSTNAME}:{config_web.PORT}/generate-dot?p={escaped_create_dot}")
    print(f"- describe DOT example: http://{config_web.HOSTNAME}:{config_web.PORT}/describe-dot?p={escaped_dot}");
    print("[press any key to stop]")
    [Thread(i) for i in range(config_web.WEB_SERVER_THREADS)]
    input("Press ENTER to kill server\n")

    print("Server stopped.")

if __name__ == "__main__":
    if config.is_debug:
        start_single_threaded()
    else:
        start_multi_threaded()
