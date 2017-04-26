from openedoo_project import db
from openedoo_project import config


try:
    # NOTE: if you can't import raw module in Openedoo 1.1.0.17,
    #       see https://github.com/openedoo/openedoo/issues/80
    #
    # TODO: change it to the correct way Openedoo handle query

    from openedoo_project.db.raw import query

except ImportError:
    from .lib.raw import query

from .error_handler import InvalidUsage


class Eclass(db.Model):
    """Eclass database schema

    :id integer: The Eclass id
    :name varchar: The Eclass name
    :course varchar: The course where Eclass belongs to
    :university varchar: The university where Eclass belongs to
    :member text: The Eclass member
    :admin text: The Eclass administrator
    :privilege varchar: The Eclass privilege, public or private
    :unique_code text: The Eclass unique code
    """

    __tablename__ = 'icampus_eclass'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.VARCHAR(50), nullable=False)
    course = db.Column(db.VARCHAR(50))
    university = db.Column(db.VARCHAR(50))
    member = db.Column(db.UnicodeText())
    admin = db.Column(db.UnicodeText())
    privilege = db.Column(db.VARCHAR(8), default="private")
    unique_code = db.Column(db.Text)

    def insert(self, data=None):
        """Insert a record"""

        try:
            sql = "INSERT INTO {} VALUES (DEFAULT, '{}', '{}', '{}', '{}', \
            '{}', '{}', '{}')"
            sql = sql.format(self.__tablename__, data['name'], data['course'],
                             data['university'], data['member'], data['admin'],
                             data['privilege'], data['unique_code'])
            query(sql)
            result = {'message': 'success'}
            return result

        except Exception as e:
            raise InvalidUsage('Something bad happened', repr(e),
                               status_code=410)

    def get_all(self):
        """Get all records"""

        try:
            result = query('SELECT * FROM {}'.format(self.__tablename__))
            return result

        except Exception as e:
            raise InvalidUsage('Something bad happened', repr(e),
                               status_code=410)

    def get(self, eclass_id=None):
        """Get record by id"""

        try:
            sql = 'SELECT * FROM {} WHERE id={}'
            sql = sql.format(self.__tablename__, eclass_id)
            result = query(sql)
            return result

        except Exception as e:
            raise InvalidUsage('Something bad happened', repr(e),
                               status_code=410)

    def update(self, data=None):
        """Update a record by id"""

        try:
            # Sql column construction from dict
            column = ', '.join("{key}='{value}'".format(key=key, value=value)
                               for key, value in data.iteritems()
                               if key not in ('id'))
            sql = 'UPDATE {} SET {} WHERE id={}'
            sql = sql.format(self.__tablename__, column, data['id'])
            # The query execution doesn't return any value
            query(sql)
            result = {'message': 'success'}
            return result

        except Exception as e:
            raise InvalidUsage('Something bad happened', repr(e),
                               status_code=410)
