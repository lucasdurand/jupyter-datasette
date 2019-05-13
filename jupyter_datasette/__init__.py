from notebook.utils import url_path_join as _url_path_join
from notebook.base.handlers import IPythonHandler
import sys as _sys
import os as _os
import socket as _socket
from IPython.display import display as _display
from IPython.display import HTML as _HTML

# TODO: real config class for this
datasette_path = _os.environ.get('DATASETTE_HOME',_os.path.expanduser('~/Datasette'))
datasette_host = _os.environ.get('DATASETTE_HOST',None) # provide a static hostname to keep users happy

from . import tools

# Pandas DataFrame to Datasette
def pandas_to_datasette(df, name='this', table_name='table', db_root='./', if_exists='replace', logging=True, **kwargs):
    # create the DB from csv
    db_name = tools.pandas_to_sqlite(df, name, table_name, db_root, if_exists) 
    # now to launch it ...
    return Datasette(db_name, jupyter=True, logging=logging, **kwargs)
    

# Publish Pandas DataFrame to Jupyter-Datasette Home


# TODO: register Jupyter Magic

class Datasette():
    '''
    I hold and manage a Datasette server. I pick up changes to existing databases, 
        but need to be reloaded to pick up new files
    '''
    def __init__(self, files=[], folder=None, logging=False, jupyter=True, **kwargs):
        self.files =  files
        self.path = folder
        self.logging = logging
        self.jupyter = jupyter
        self._launch()

    def reload(self):
        '''Terminate existing Datasette process and start on another available port'''

        # TODO: can we run this from a service that detects newly added files?
        self.kill()
        self._launch()
        return

    def _launch(self):
        '''Only to be called directly in __init__ for first launch'''
        if self.path:
            files = ' '.join([_os.path.join(self.path,x) for x in _os.listdir(self.path) if x[-3:]=='.db'])
        else:
            files = ' '.join(self.files) if type(self.files) is list else self.files
        self.port = tools.find_free_port()

        # TODO: use pexpect so we're sure that it's `Goin' Fast` before we try and load the page
        self.process = tools.start_datasette(files, jupyter=self.jupyter, port=self.port, host='0.0.0.0', reload=True)
        self.pid = self.process.pid
        
        if self.logging: # this is blocking
            try:
                for line in iter(self.process.stderr.readline, b''):
                    _sys.stdout.write(line)
            except: # KeyboardInterrupt or some other calamity
                self.process.terminate()     

    def kill(self):
        self.process.terminate()
        self.process.wait()
        return

    def __del__(self):
        self.kill()

class _DatasetteHandler(IPythonHandler):
    def get(self):
        """
        Return location of running Datasette
        """           
        datasette = self.application.datasette

        if self.get_arguments('reload'):
            datasette.reload()
            return
        else:
            port = datasette.port
            host = datasette_host if datasette_host else _socket.gethostbyname(_socket.gethostname())
            self.redirect(f'http://{host}:{port}')

def _jupyter_server_extension_paths():
    """
    Set up the server extension for managing Datasette
    """
    return [{
        'module': 'jupyter-datasette',
    }]

def _jupyter_nbextension_paths():
    """
    Set up the notebook extension for displaying Datasette
    """
    return [{
        "section": "tree",
        "dest": "jupyter-datasette",
        "src": "static",
        "require": "jupyter-datasette/main"
    }]

def load_jupyter_server_extension(nbapp):
    """
    Called during jupyter server start
    """
    datasette = Datasette(folder=datasette_path, jupyter=False)
    nbapp.web_app.datasette = datasette
    route_pattern = _url_path_join(nbapp.web_app.settings['base_url'], '/datasette')
    nbapp.web_app.add_handlers('.*', [(route_pattern, _DatasetteHandler)])
