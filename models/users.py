# Poblado de usuarios

import conection

users_types = {
    "name": str,
    "email": str,
    "phone": str,
    "account_status": str,
    "tickets_history": list
}

users_data = [
    {
        "name": "Jaime",
        "edad": "20"
    }
]
conection.mongo_db["users"].insert_many(users_data)
print("Datos insertados en MongoDB!uwu")
