from os import environ
from pandas import DataFrame, read_sql
from sqlalchemy import create_engine
from sqlalchemy.inspection import inspect


class DBConnector(object):

    def __init__(self, table, data_base, env=None):

        if env is None:
            env = environ['DATABASE_LOGIN'] + '/' + data_base

        self._env = env
        self._table = table
        self._data_base = data_base
        self.set_columns_names()

    @property
    def columns(self):
        """
        Return colums names
        """
        return self._columns

    @property
    def data_base(self):
        """
        Return data base name
        """
        return self._data_base

    @property
    def table(self):
        """
        Return table name
        """
        return self._table

    def count_rows(self):
        """
        Count the number of rows in the table

        Returns
        -------
        rows_number: int
            number of rows
        """

        # Create query
        query = """
        SELECT COUNT(*)
        FROM {table}
        """.format(table=self._table)

        # Query DB and extract rows number
        query_result = self.query_DB(query, add_keys=False)
        rows_number = query_result[0][0]

        return int(rows_number)

    @staticmethod
    def format_information(input):
        """
        Format information to be added on a SQL query or if already a str return the same result

        Parameters
        ----------
        input: list, str
            Input information

        Returns
        -------
        str
        """

        if isinstance(input, list):
            str_input = map(str, input)
            output = ', '.join(str_input)
        else:
            output = input

        return output

    def get_db_values(self, columns=None, id_filter=None):
        """
        Run query to extract table values

        Parameters
        ----------
        columns: str, list[str]
            columns names to query the table
        id_filter: str, list[str], list[int]
            id numbers to filter the SQL query with

        Returns
        -------
        db_info: pandas.DF
            resulting query from the table
        """
        # Define columns name
        columns = self._columns_str if columns is None else self.format_information(columns)

        # Create query
        query = """
        SELECT {columns}
        FROM {table}
        """.format(columns=columns, table=self._table)

        # Add id_filtering if needed
        if id_filter is not None:
            id_filter_format = self.format_information(id_filter)
            query += '\n WHERE id in ({id})'.format(id=id_filter_format)

        # Query DB
        db_info = self.query_DB(query)
        return db_info

    def query_DB(self, query):
        """
        Run input query into the DB

        Parameters
        ----------
        query: str
            SQL query

        Returns
        -------
        db_info: pandas.DF
            resulting query from the table
        """

        Engine = create_engine(self._env)
        db_info = read_sql(query, con=Engine)
        Engine.dispose()

        return db_info

    def set_columns_names(self):
        """
        Check DB table and sets columns names
        """

        Engine = create_engine(self._env)

        inspector = inspect(Engine)
        column_info = inspector.get_columns(self._table)
        column_names = map(lambda x: x['name'], column_info)

        Engine.dispose()

        self._columns = column_names
        self._columns_str = ', '.join(column_names)

    def store_values(self, data, if_exists='append'):
        """
        Store values in the DB table

        Parameters
        ----------
        data: pandas.DF
            data to be stored
        if_exists: str
            How to behave if the table already exists.
        """

        Engine = create_engine(self._env)
        data.to_sql(name=self._table, con=Engine, if_exists=if_exists, chunksize=500, index=False)
        Engine.dispose()
