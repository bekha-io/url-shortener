import datetime
import random
import string

from peewee import *
from playhouse.sqliteq import SqliteQueueDatabase


database = SqliteQueueDatabase('database.db')


def generate_id(length: int = 5):
    choices = string.digits + string.ascii_lowercase
    s = ''
    for i in range(0, length):
        s += random.choice(choices)
    return s


class BaseModel(Model):
    class Meta:
        database = database


class ShortUrl(BaseModel):
    id: str = CharField(max_length=6, default=generate_id, primary_key=True)
    url: str = CharField(unique=True)
    ip_requested: str = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def new(cls, url: str, ip_requested: str) -> 'ShortUrl':
        record = cls.get_or_none(url=url, ip_requested=ip_requested)
        if not record:
            return cls.create(url=url, ip_requested=ip_requested)
        return record

    @classmethod
    def get_by_ip(cls, ip_requested: str):
        return cls.select().where(cls.ip_requested == ip_requested).order_by(cls.created_at.desc())

    @property
    def redirects_count(self):
        return self.redirects.count()


class UrlRedirect(BaseModel):
    short_url: ShortUrl = ForeignKeyField(ShortUrl, backref='redirects')
    ip_requested: str = CharField()
    requested_at: datetime.datetime = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def new(cls, short_url: ShortUrl, ip_requested: str) -> 'UrlRedirect':
        return cls.create(short_url=short_url, ip_requested=ip_requested)


database.create_tables(
    [ShortUrl, UrlRedirect]
)