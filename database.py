from openedoo_project import db
from openedoo_project import config


class EclassSchema(db.Model):
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


class EclassPostsSchema(db.Model):
    """Eclass posts database schema.

    :id integer: The Post id
    :class_id integer: The Eclass id
    :description text: The post's description
    :reply text: The post's reply
    :attachment text: The post's file attachment
    :created datetime: Time when The post is created
    :edited datetime: Time when The post is edited
    """

    __tablename__ = 'icampus_eclass_post'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    class_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    reply = db.Column(db.UnicodeText())
    attachment = db.Column(db.Text)
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)
