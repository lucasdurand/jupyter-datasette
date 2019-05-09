
import pandas as pd
df = pd.DataFrame()

# Some useful tools now that we have Datasette integrated with Jupyter
import sqlite3

# Pandas DataFrame to Datasette

def pandas_to_datasette(df, table):


# Let's keep this simple for now, unfortunately can't use csvs-to-sqlite to do more intricate setup (cli only)
def pandas_to_sqlite(df, name='this', table_name='table', root='./', if_exists='replace', **kwargs):
	'''
		DataFrame -> SQLite db

		note, we set df.name and df.table_name on our pandas df instead of specifying as args
	'''
	table_name = df.table_name if 'table_name' in vars(df) else table_name
	name = df.name if 'name' in vars(df) else name
	db_name = os.path.join(root,name)

	

	conn = sqlite3.connect(db_name)
	df.to_sql(table_name, conn, if_exists=if_exists)
	return db_name