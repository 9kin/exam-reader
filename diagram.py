from os.path import dirname

from diagrams import Cluster, Diagram, Node
from diagrams.programming.framework import Flask
from diagrams.programming.language import Python


class Custom(Node):
    _provider = "telephony"
    _icon_dir = dirname(__file__) + "/resources/diagram"
    fontcolor = "#2d3436"


class Camelot(Custom):
    _icon = "camelot.png"


class MuPDF(Custom):
    _icon = "MuPDF.png"


class Peewee(Custom):
    _icon = "peewee.png"


from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS
from diagrams.aws.integration import SQS
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx

with Diagram("Web Service", show=True):
    with Cluster("Processing"):
        workers = [ECS("worker1"), ECS("worker2")]

    with Cluster("Extraction"):
        with Cluster("PDF"):
            pdf = Camelot("Table") - MuPDF("Text")

    with Cluster("database"):
        orm = Peewee("ORM")
        postgres = PostgreSQL("storage")

    queue = SQS("event queue")
    server = Flask()
    Nginx("Nginx") >> server >> queue >> workers >> pdf
    pdf >> orm >> postgres
