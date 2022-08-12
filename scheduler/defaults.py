import os

SQL_IMPORT_FILE = os.getenv('SQL_IMPORT_FILE', './sqlite/script/database.sql')
SQL_DATABASE = os.getenv('SQL_DATABASE', 'monitoring.sqlite')