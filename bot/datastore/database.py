from peewee import *

db = SqliteDatabase("app.sqlite3")


class Quote(Model):
    content = CharField()

    class Meta:
        database = db


def init_db():
    db.create_tables([Quote])
