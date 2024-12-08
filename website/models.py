from website._init_ import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    data = db.Column(db.String(1000))
    date =db.Column(db.DateTime(timezone = True),default = func.now())
    # one user for many note
    user_id = db.Column(db.Integer ,db.ForeignKey('user.id'))


# user类继承
class User (db.Model,UserMixin):
    id = db.Column(db.Integer ,primary_key = True)
    email = db.Column(db.String(150),unique = True)
    password =  db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # 关联此user的note，以list存储
    notes = db.relationship('Note')