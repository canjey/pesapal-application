from ast import Pass
from http.server import HTTPServer, BaseHTTPRequestHandler
from sys import path
import cgi
import socket, ssl
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from importlib.machinery import SourceFileLoader

from jinja2 import Environment, select_autoescape, FileSystemLoader


class RequestHandler(BaseHTTPRequestHandler):
    """Class that handles HTTPRequests

    In this class I have implemented a dynamic and static server.
    The dynamic server generates html using python in the same way Apache uses PHP
    The static server, serves content as is the file system in the server

    Attributes: 
        root_directory (str): This is the path from where or files are served from

    """
    root_directory = '/'


    def get_jinja_env(self):
        """Gets jinja environment based on the root directory

        Return:
            Environment: The jinja environment that will be used to load the templates
        """
        return Environment(
            loader=FileSystemLoader(
                os.path.join(self.root_directory, 'templates')
            ),
            autoescape=select_autoescape()
        )
    def process_request(self, method):
        """Dynamically generates html based on content of the python file
        Get file path based on the url path.
        Fetch and load a python file using this path run the main function on the python file
        Example main method
            def main(env, request_handler, method):
                return 'generated HTML'
        Args:
            method(str): GET or POST
        
        """
        # get file path from request combine with root directory to get
        # full path
        if self.path.endswith('/'):
            self.path += '__init__.py'
        file_path = os.path.join(self.root_directory, self.path[1:])

        try:
            # get python file using path above
            python_file = SourceFileLoader("python_file", file_path).load_module()
            # call main function to return generated html
            generated_html = python_file.main(
                env=self.get_jinja_env(),
                request_handler=self,
                method=method
            )
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(generated_html.encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write("ERROR".encode())
            raise e

    def static_get(self):
        """Get static files
        Get file path from url path, get content of the file and then display the file

        """
        file_path = os.path.join(self.root_directory, self.path[1:])
        try :
            f = open(file_path, "r")
        except FileNotFoundError:
            return 
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(f.read().encode())

    def dynamic_get(self):
        self.process_request("GET")

    def dynamic_post(self):
        self.process_request("POST")

    def do_GET(self):
        """If file ends with .py or / generate dynamic files
        else, generate static files
        """
        if self.path.endswith('/') or self.path.endswith('.py'):
            return self.process_request('GET')
        else:
            return self.static_get()
        

    def do_POST(self):
        return self.process_request('POST')


    
def main(root_directory, port):
    # set root directory
    RequestHandler.root_directory = root_directory
    print("run")
    server = HTTPServer(('', port), RequestHandler)
    print('Server running on port %s' % port)
    server.serve_forever()


if __name__ == '__main__':
    # take arguments from main where the root directory is specified
    root_directory, port = sys.argv[1], sys.argv[2]
    main(root_directory, int(port))