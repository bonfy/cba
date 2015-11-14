# coding : utf-8

from peewee import *
import datetime


# db = MySQLdb.connect(host='localhost',user='****'
#    ,passwd='****',port=3306,db='****',charset='utf8')
db = MySQLDatabase(
    'cba', user='root', passwd='', charset='utf8', host='localhost', port=3306)


class BaseModel(Model):

    class Meta:
        database = db


class BBS(BaseModel):
    title = TextField()
    href = TextField()
    website = TextField()
    model = TextField()
    author = TextField()
    published = DateTimeField()
    created_date = DateTimeField(default=datetime.datetime.now)

db.connect()
db.create_tables([BBS, ])
