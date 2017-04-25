from openedoo_project import db

# NOTE: if you can't import raw module in Openedoo 1.1.0.17,
#       see https://github.com/openedoo/openedoo/issues/80
#
# TODO: change it to the correct way Openedoo handle query
from openedoo_project.db.raw import query
from openedoo_project import config


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

    def get_all(self):
        """Get all records"""
        result = query('SELECT * FROM {}'.format(self.__tablename__))
        print result
        return result
