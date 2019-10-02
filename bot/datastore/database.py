from peewee import *

db = SqliteDatabase("app.sqlite3")


class Quote(Model):
    content = CharField()
    author = CharField()
    author_id = IntegerField()
    invoker = CharField()
    invoker_id = IntegerField()
    guild_id = IntegerField()
    timestamp = DateTimeField()

    class Meta:
        database = db


def init_db():
    db.create_tables([Quote])
