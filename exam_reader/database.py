from os import getenv

from peewee import CharField, Model, SmallIntegerField
from playhouse.postgres_ext import PostgresqlExtDatabase

# https://stackoverflow.com/a/26735105
# createuser -P -s -e exam
# sudo vim /etc/postgresql/13/main/pg_hba.conf
# local all   exam md5
# sudo service postgresql restart
# psql -U exam postgres


db = PostgresqlExtDatabase(
    getenv("DB_NAME"),
    user=getenv("DB_USER"),
    password=getenv("DB_PASSWORD"),
    host=getenv("DB_HOST"),
    port=getenv("DB_PORT"),
)


class BaseModel(Model):
    """A base model that will use our Postgresql database."""

    class Meta:
        """Meta class."""

        database = db


class Job(BaseModel):
    """Job model for worker (like redis)"""

    path = CharField()
    status = SmallIntegerField()
