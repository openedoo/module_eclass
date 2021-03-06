from .raw_query import query
from .security import sanitize
from .error_handler import InvalidUsage


def sql_column_builder(data=None):
    """SQL column builder.

    A helper for building column list in SQL syntax from python dict.
    Example:

        data = {'id': 1, 'name': 'example'}

        become:

        id='1', name='example'

    Then it can be used with existing SQL syntax by joining them.
    Example:

        sql = 'INSERT INTO table SET {}'.format(sql_column_builder(data))

    """
    tmp = []
    for key, value in data.iteritems():
        if isinstance(value, basestring):
            sanitized_value = sanitize(value)
            tmp.append("{key}='{value}'".format(key=key, value=sanitized_value))
        else:
            tmp.append("{key}={value}".format(key=key, value=value))

    column_string = ', '.join(tmp)
    return column_string


def sql_select_expr_builder(expr=None):
    """SQL select expression builder.

    A helper for building select expression in SQL syntax from python list.
    """
    return ', '.join('{}'.format(expr_item for expr_item in expr))


class DBQuery(object):
    def insert(self, table=None, col=None):
        try:
            sql = "INSERT INTO {} SET id=DEFAULT, {}"
            sql = sql.format(table, sql_column_builder(col))
            return query(sql)

        except Exception:
            raise InvalidUsage('Something bad happened in the server.', '',
                               status_code=500)

    def select(self,
               select_expr=None,
               table=None, where_clause=None, pagination=None):
        """Select query.

        You can pass the select expression with python list for many columns,
        string for one column, and none if you want to select all.

        Example:

            db_query.select(select_expr=['a_table.id','a_table.name'],
                            table='a_table')

        Equivalent to:

            'SELECT a_table.id, a_table.name FROM a_table'

        """
        try:
            if not select_expr:
                col = '*'
            elif len(select_expr) == 1:
                col = select_expr[0]
            elif isinstance(select_expr, basestring):
                col = select_expr
            else:
                col = sql_select_expr_builder(select_expr)

            start_page = pagination['start_page'] if pagination else 0
            limit = pagination['limit'] if pagination else 20
            sql = 'SELECT {} FROM {} LIMIT {}, {}'.format(col,
                                                          table,
                                                          start_page,
                                                          limit)
            if where_clause:
                sql_where = sql_column_builder(where_clause)
                sql = "SELECT {} FROM {} WHERE {} LIMIT {}, {}"
                sql = sql.format(col, table, sql_where, start_page, limit)

            result = query(sql)
            return result

        except Exception as e:
            raise InvalidUsage('Something bad happened in the server.', str(e),
                               status_code=500)

    def update(self, table=None, col=None, where_clause=None):
        try:
            sql_where = ''
            for key, value in where_clause.iteritems():
                if isinstance(value, basestring):
                    sql_where = "{key}='{value}'"
                    sql_where = sql_where.format(key=key, value=sanitize(value))
                else:
                    sql_where = "{key}={value}"
                    sql_where = sql_where.format(key=key, value=value)

            column = sql_column_builder(col)
            sql = 'UPDATE {} SET {} WHERE {}'
            sql = sql.format(table, column, sql_where)
            result = query(sql)
            return result

        except Exception:
            raise InvalidUsage('Something bad happened in the server.', '',
                               status_code=500)

    def delete(self, table=None, where_clause=None):
        try:
            tmp = []
            for key, value in where_clause.iteritems():
                if isinstance(value, basestring):
                    sql_where = "{key}='{value}'"
                    sql_where = sql_where.format(key=key, value=sanitize(value))
                    tmp.append(sql_where)
                else:
                    sql_where = "{key}={value}"
                    sql_where = sql_where.format(key=key, value=value)
                    tmp.append(sql_where)

            where = ' AND '.join(tmp)
            sql = 'DELETE FROM {} WHERE {}'.format(table, where)
            return query(sql)

        except Exception as e:
            raise InvalidUsage('Something bad happened in the server', str(e),
                               status_code=500)
