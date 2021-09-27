import pymongo
import ssl

#Crear conexion a Mongodb
client = pymongo.MongoClient("mongodb+srv://doratt:Ludhe97@sandbox.sbzkp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mongoDb = client['cinemadataset']['attendancedata']

class MongoConnection:

    def insertMany(listCinema):
        if not listCinema is None:
            mongoDb.insert_many(listCinema)
        else:
            print('Error>InsertMany: Lista vacia')

    def insertOne(Cinema):
        if not Cinema is None:
           response = mongoDb.insert_one(Cinema)
           return response
        else:
            print('Error>InsertOne: objeto vacio')

    def find(queryFind,querySort,limit):

        if limit <=0 or not limit is None:
            limit = 10 
    
        if not queryFind is None and not querySort is None:
            response = mongoDb.find(queryFind).sort(querySort).limit(limit)
            return response
        elif not querySort is None:
            response = mongoDb.find().sort(querySort).limit(limit)
            return response
        else : 
            response = mongoDb.find().limit(limit)
            return response
    
    def aggregate(queryFind):

        if not queryFind is None :
            response = mongoDb.aggregate(queryFind)
            return response
        else : 
            response = mongoDb.find()
            return response