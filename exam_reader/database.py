from peewee import Model, CharField
from playhouse.postgres_ext import PostgresqlExtDatabase

# https://stackoverflow.com/a/26735105
# createuser -P -s -e exam
# sudo vim /etc/postgresql/13/main/pg_hba.conf
# local all   exam md5
# sudo service postgresql restart
# psql -U exam postgres

db = PostgresqlExtDatabase('postgres', user='exam', password='1234')

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = db

class Tmp(BaseModel):
    username = CharField()


db.connect()
db.create_tables([Tmp])
