#!/usr/bin/python

"""sqlitedatastore.py: Class implementing the object to interact with the persistent SQLite database"""

import re
import sqlite3

__author__ = "Ashvin Domah"
__copyright__ = "Copyright 2017"
__maintainer__ = "Ashvin Domah"
__email__ = "ashvindomah@gmail.com"
__status__ = "Production"
__version__ = "1.0"


class SQLiteDataStore(object):
    _db_conn = None

    def __init__(self, path_to_db_file):
        self._db_conn = sqlite3.connect(path_to_db_file)

    def execute_reader(self, query):
        data_set = []

        with self._db_conn:
            cursor = self._db_conn.execute(query)

            column_names = [description[0]
                            for description in cursor.description]

            for row in cursor:
                r = {}

                for index, value in enumerate(column_names):
                    r[value] = row[index]

                data_set.append(r)

        return data_set

    def execute_scalar(self, query):
        scalar = None

        with self._db_conn:
            cursor = self._db_conn.execute(query)

            scalar = cursor.fetchone()[0]

        return scalar

    def execute_non_query(self, query):
        info = None

        insert_pattern_regex = re.compile("INSERT*", re.IGNORECASE)

        with self._db_conn:
            cursor = self._db_conn.execute(query)

            if insert_pattern_regex.match(query):
                info = self.execute_scalar("SELECT last_insert_rowid()")
            else:
                info = self._db_conn.total_changes

            self._db_conn.commit()

        return info
