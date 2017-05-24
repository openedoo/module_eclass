from openedoo_project.db.raw import query
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
    column_string = ''
    for key, value in data.iteritems():
        if isinstance(value, basestring):
            column_string += ", {key}='{value}'".format(key=key,
                                                        value=sanitize(value))
        else:
            column_string += ", {key}={value}".format(key=key,
                                                      value=value)
    return column_string


def sql_select_expr_builder(expr=None):
    """SQL select expression builder.

    A helper for building select expression in SQL syntax from python list.
    """
    return ', '.join('{}'.format(expr_item for expr_item in expr))


class DBQuery(object):
    def insert(self, table=None, col=None):
        try:
            sql = "INSERT INTO {} SET id=DEFAULT{}"
            sql = sql.format(table, sql_column_builder(col))
            return query(sql)

        except Exception:
            raise InvalidUsage('Something bad happened in the server.', '',
                               status_code=500)

    def select(self, select_expr=None, table=None, where_clause=None):
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

            sql = 'SELECT {} FROM {}'.format(col, table)
            if where_clause:
                sql_where = "{key}='{value}'"
                for key, value in where_clause.iteritems():
                    sql_where = sql_where.format(key=key, value=sanitize(value))
                sql = 'SELECT {} FROM {} WHERE {}'.format(col,
                                                          table,
                                                          sql_where)

            result = query(sql)
            return result

        except Exception as e:
            raise
