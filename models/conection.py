from pymongo import MongoClient 

def connect_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['customer_support']
    return db

# if __name__ == "__main__":
#     # cassandra_session = connect_cassandra()
#     mongo_db = connect_mongodb()
#     print("Conexión establecida con Cassandra y MongoDB")

