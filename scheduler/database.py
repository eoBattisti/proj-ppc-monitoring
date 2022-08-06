import os
import sqlite3

from singleton import Singleton

class Database(metaclass=Singleton):
    """
    Database Class.
    """
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = self.get_connection()

    def __str__(self):
        return f'Database name: {self.db_name}'

    @property
    def changes(self):
        """ Verify the number of affected rows by the last
            sql query. 

        Returns:
            tuple(int): number of affected rows.
        """        
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = """SELECT changes();"""
            cursor.execute(query)
            changes =  cursor.fetchone()
            return changes
        except sqlite3.Error as error:
            print("Error while getting database information")

    @property
    def total_changes(self):
        """
        Verify the amount of affected rows since the connection
        was opened.

        Returns:
            tuple(int): number of affected rows.
        """
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = """SELECT total_changes();"""
            cursor.execute(query)
            changes =  cursor.fetchone()
            return changes
        except sqlite3.Error as error:
            print("Error while getting database information")

    def __connect(self):
        """ Try to establish a connection to the database.

        Returns:
            Connection: the database connection
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
        except sqlite3.Error as error:
            print(f'Error while connecting to the database: {self.db_name}')
        finally:
            if conn:
                print(f'Connection to the database established!')
                return conn

    def __disconnect(self):
        """
        Disconnect from the database.
        """
        try:
            if self.connection:
                self.connection.close()
                print(f'The connection is closed')
        except sqlite3.Error as error:
            print(f'Error while disconnecting to the database: {self.db_name}')

    def __get_num_columns(self, table: str) -> int:
        """ Return the amount of rows of a given table

        Args:
            table (str): table name

        Returns:
            int: number of rows
        """
        cursor = None
        columns_info = None
        try:
            cursor = self.connection.cursor()
            query = f"""PRAGMA table_info({table})"""
            cursor.execute(query)
            columns_info = cursor.fetchall()
        except sqlite3.Error as error:
            print(f'Error while getting amount of rows: {error}')
        finally:
            if columns_info:
                return len(columns_info)
            else:
                return None

    def __normalize_insert_query_string(self, table: str, query: str) -> str:
        """ Normalize a insert query string to match the database
        the exact number of columns that must be inserted.
        
        Args:
            table (str): the table name

        
        Returns:
            str: SQL Query
        """
        num_columns = self.__get_num_columns(table=table)
        values = ""
        for _ in range(num_columns):
            values += ",".join("? ")
        values = " (" + values + ")"
        query = query + values
        return query

    def close_connection(self):
        """Close database connection."""
        self.__disconnect()

    def get_connection(self):
        """Return a database connection."""
        return self.__connect()

    def import_tables(self, file: str):
        """ Import and execute a given sql into the database.
        This method is used to init all the tables.

        Args:
            file (str): filepath
        """               
        cursor = self.connection.cursor()
        try:
            if not os.path.exists(file):
                raise FileNotFoundError
            sql_file = open(file, 'r')
            query = sql_file.read()
            cursor.executescript(query)
        except sqlite3.Error as error:
            print(f'Error while importing tables: {error}')
        except FileNotFoundError:
            print(f'The given database file to import does not exist!')

    def insert_data(self, table: str, data: tuple):
        """Try to insert the given data into the given table. 

        Args:
            table (str): table name

            data (tuple): the data to be inserted. ex: (foo, bar, xpto)
        """        
        cursor = self.connection.cursor()
        try:
            query = f"INSERT INTO {table} VALUES"
            query = self.__normalize_insert_query_string(table=table, query=query)
            cursor.execute(query, data)
            self.connection.commit()
            print(f'Successfuly insert the data into disk_table')
        except sqlite3.Error as error:
            print(f'Erro while inserting data into disk_table: {error}')
        finally:
            cursor.close()


if __name__ == "__main__":
    db = Database('test.sqlite')
    db.import_tables('./sqlite/script/database.sql')
    print(db.changes)
    print(db.total_changes)
    db.drop_table('test.db')
