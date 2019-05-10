# Some useful tools now that we have Datasette integrated with Jupyter
import subprocess as _subprocess
import sys as _sys
import os as _os
import socket as _socket
from IPython.display import display as _display
from IPython.display import HTML as _HTML
import re

import sqlite3 as _sqlite3
from contextlib import closing as _closing

def find_free_port():
    with _closing(_socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(_socket.SOL_SOCKET, _socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

# Let's keep this simple for now, unfortunately can't use csvs-to-sqlite to do more intricate setup (cli only)
def pandas_to_sqlite(df, name='this', table_name='table', db_root='./', if_exists='replace', **kwargs):
    '''
        DataFrame -> SQLite db

        note, we set df.name and df.table_name on our pandas df instead of specifying as args
    '''
    table_name = df.table_name if 'table_name' in vars(df) else table_name
    name = df.name if 'name' in vars(df) else name
    db_name = _os.path.join(db_root,name)
    db_name = f'{db_name}.db' if '.db' not in db_name else db_name

    conn = _sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists=if_exists)
    return db_name

def start_datasette(db_path, jupyter, **kwargs):
    '''
        Pass in cmdline flags as kwargs: port=8080, reload=True
    '''
    port = kwargs.get('port',kwargs.get('p',None))
    host = _socket.gethostbyname(_socket.gethostname())

    # keep the kwargs alive
    flags = [f'--{key}' if value is True else f'--{key} {value}' for key,value in kwargs.items()]
    flags = ' '.join(flags)
    cmd = f'datasette {db_path} {flags}'
    cmd = re.sub(' +', ' ', cmd)

    if jupyter:
        _display(_HTML(f'''<b>Datasette Launching at <a target="_blank" href="http://{host}:{port}">http://{host}:{port}</a></b><br/>
            <pre>{cmd}</pre>'''))
    try:
        process = _subprocess.Popen(cmd.split(' '), stderr=_subprocess.PIPE, stdout=_subprocess.PIPE)
        return process
    except: #catch KeyboardInterrupt and whatever other calamity might befall our process
        process.terminate()