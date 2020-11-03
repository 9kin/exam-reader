from peewee import CharField, Model, SmallIntegerField
from playhouse.postgres_ext import PostgresqlExtDatabase

# https://stackoverflow.com/a/26735105
# createuser -P -s -e exam
# sudo vim /etc/postgresql/13/main/pg_hba.conf
# local all   exam md5
# sudo service postgresql restart
# psql -U exam postgres

db = PostgresqlExtDatabase("postgres", user="exam", password="1234")


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = db


class PQueue(BaseModel):
    path = CharField()
    status = SmallIntegerField()
