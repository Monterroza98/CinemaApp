from Models.MongoConnection import *

class CinemaController:

    def __init__():

    def uploadToDatabase(filename, content):

        if not filename is None and not content is None:
            jsonRequest = {"_id": filename, "content": content}

            MongoConnection.insert_many(jsonRequest)
            
        else :
            print('Error>InsertMany: filename o content vacio') 
            
