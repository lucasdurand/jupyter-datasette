import os, sys
import json
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import socket
import re
import subprocess

path = os.environ.get('DATASETTE_HOME',os.path.expanduser('~/'))

class DatasetteHolder():
    def __init__(self, home):
        self.path=home
        self.launch()

    def get_available_port(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind(('', 0))
        addr, port = tcp.getsockname()
        tcp.close()
        return port

    def reload(self):
        self.kill()
        self.launch()

    def launch(self):
        print("Launching")
        files = ' '.join([x for x in os.listdir(self.path) if x[-3:]=='.db'])
        self.port = self.get_available_port()
        cmd = f'datasette {files} --reload --port {self.port} --host 0.0.0.0'
        cmd = re.sub(' +', ' ', cmd)
        self.process = subprocess.Popen(cmd.split(' '))
        self.pid = self.process.pid

    def kill(self):
        self.process.kill()
        os.waitpid(self.pid,0)

class DatasetteHandler(IPythonHandler):
    def get(self):
        """
        Return location of running Datasette
        """           
        datasette = self.application.datasette

        if self.get_arguments('reload'):
            datasette.reload()

        port = datasette.port
        self.write(json.dumps({'port':port,'localurl':f'http://localhost:{port}'}))

def _jupyter_server_extension_paths():
    """
    Set up the server extension for collecting metrics
    """
    return [{
        'module': 'jupyter-datasette',
    }]

def _jupyter_nbextension_paths():
    """
    Set up the notebook extension for displaying metrics
    """
    return [{
        "section": "tree",
        "dest": "jupyter-datasette",
        "src": "static",
        "require": "jupyter-datasette/main"
    }]

def load_jupyter_server_extension(nbapp):
    """
    Called during notebook start
    """
    datasette = DatasetteHolder(path)
    nbapp.web_app.datasette = datasette
    route_pattern = url_path_join(nbapp.web_app.settings['base_url'], '/datasette')
    nbapp.web_app.add_handlers('.*', [(route_pattern, DatasetteHandler)])