import sqlite3

connection = sqlite3.connect('organizations.db')

# Allowable filters:
# id, name, city, state, postal, category

class Query:
    def __init__(self, filters={}, orderBy=None, isAscending = True):
        self._filters = filters
        self._orderBy = orderBy
        if isAscending:
            self._direction = ''
        else:
            self._direction = ' DESC'

    def build_query(self):
        # Basic query string
        query_string = "select id,name,city,state,postal,category from organizations"
        bind_params = []

        # Optionally add WHERE clause
        if self._filters:
            keys = self._filters.keys()
            query_string += ' WHERE ' + ' AND '.join(map(lambda key: "%s == ?" % (key), keys))
            bind_params += map(lambda key: self._filters[key], keys)

        # Optionally add ORDER BY clause
        if self._orderBy:
            query_string += ' ORDER BY ' + self._orderBy + self._direction

        return (query_string, bind_params)

    def cursor(self):
        cursor = connection.cursor()
        (query_string, bind_params) = self.build_query()
        cursor.execute(query_string, bind_params)
        return cursor

