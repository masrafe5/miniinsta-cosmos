from mongo import db

collection = db["test"]

data = {
    "name": "Masrafe",
    "status": "CosmosDB Connected"
}

collection.insert_one(data)

print("SUCCESS")