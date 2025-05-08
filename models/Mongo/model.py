import models.conection as conection

db = conection.connect_mongodb()

db.create_collection('agentes')