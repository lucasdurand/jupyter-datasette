# Some useful tools now that we have Datasette integrated with Jupyter
import subprocess
import sys
import pandas as pd
import socket
from IPython.display import display, HTML

import sqlite3
from contextlib import closing

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

# Let's keep this simple for now, unfortunately can't use csvs-to-sqlite to do more intricate setup (cli only)
def pandas_to_sqlite(df, name, table_name, db_root, if_exists, **kwargs):
    '''
        DataFrame -> SQLite db

        note, we set df.name and df.table_name on our pandas df instead of specifying as args
    '''
    table_name = df.table_name if 'table_name' in vars(df) else table_name
    name = df.name if 'name' in vars(df) else name
    db_name = os.path.join(db_root,name)

    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists=if_exists)
    return db_name

def start_datasette(db_path, show_errors=True, **kwargs):
    '''
        Pass in cmdline flags as kwargs: port=8080, reload=True
    '''
    port = kwargs.get('port',kwargs.get('p',None))
    port = find_free_port() if not port else port

    host = socket.gethostbyname(socket.gethostname())

    # keep the kwargs alive
    flags = [f'--{key}' if value is True else f'--{key} {value}' for key,value in kwargs.items()]
    flags = ' '.join(flags)
    cmd = f'datasette {db_path} {flags}'
    display(HTML(f'''<b>Datasette Launching at <a href="{host}:{port}">{host}:{port}</a></b>'''))
    try:
        process = subprocess.Popen(cmd.split(' '), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if show_errors:
            for line in iter(process.stderr.readline, b''):
                sys.stdout.write(line)
                f.write(line)
        else:
            return process.pid, process, port
    except: #catch KeyboardInterrupt and whatever other calamity might befall our process
        process.kill()

# Pandas DataFrame to Datasette
def pandas_to_datasette(df, name='this', table_name='table', db_root='./', if_exists='replace', **kwargs):
    db_name = pandas_to_sqlite(*args, **kwargs) 
    # now to launch it ...


# TODO: register Jupyter Magic