from cassandra.cluster import Cluster # type: ignore
from pymongo import MongoClient # type: ignore
import models.model as model
import os

# Read env vars releated to Cassandra App
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'customer_support')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')

def connect_cassandra():
    cluster = Cluster(['127.0.0.1'])  # Dirección del contenedor
    session = cluster.connect()
    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)
    return session

def connect_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['customer_support']
    return db

if __name__ == "__main__":
    cassandra_session = connect_cassandra()
    mongo_db = connect_mongodb()
    print("Conexión establecida con Cassandra y MongoDB")

