class MongoConnection:

    #JsonStructure
    #{"__id": filename , content : [{nombreCine1: value1..... columna},{},{}] }

    #constructor 
    def __init__(self):
        mongoConnect = pymongo.MongoClient("mongodb://localhost:27017/")
        mongoDb = myclient["mydatabase"]
        mongoCol = mydb["customers"]

    def insertMany(listCinema):
        if not listCinema is None:
            mongoCol.insert_many(listCinema)
        else:
            print('Error>InsertMany: Lista vacia')

    def insertOne(Cinema):
        if not Cinema is None:
            mongoCol.insert_one(Cinema)
        else:
            print('Error>InsertOne: objeto vacio')

    def find(queryFind,querySort,limit):

        if limit <=0 or not limit is None:
            limit = 10 
    
        if not queryFind is None and not querySort is None:
            response = mongoCol.find(queryFind).sort(querySort).limit(limit)
            return response
        elif not querySort is None:
            response = mongoCol.find().sort(querySort).limit(limit)
            return response
        else : 
            response = mongoCol.find().limit(limit)
            return response
    
    def aggregate(queryFind,querySort,limit):

        if limit <=0 or not limit is None:
            limit = 10 
    
        if not queryFind is None and not querySort is None:
            response = mongoCol.aggregate(queryFind).sort(querySort).limit(limit)
            return response
        else : 
            response = mongoCol.find().limit(limit)
            return response