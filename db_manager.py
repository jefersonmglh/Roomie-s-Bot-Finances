import pymongo
from var_config import DB_AUTH




class DataBaseManager:

	def __init__(self):
		self.db = pymongo.MongoClient(DB_AUTH).ozado_db

	def add_currently(self, data):
		return self.db.currently.insert_one(data)
		
	def add_fixas(self, data):
		return self.db.fixas.insert_one(data)

	def all_fixas(self):
		return self.db.fixas.find({})

	def docs_per_data(self, last_fechamento):
		return self.db.currently.find({"time": {"$gt": last_fechamento}})

	def fechamento_data(self):
		return self.db.currently.find({'desc': 'fechamento'}).sort('time', -1)

	def mod_fix(self, doc_id, value_data, user_data):
		return self.db.fixas.update_one({"_id": doc_id}, {"$set": {
                                                  "value": value_data,
                                                  "user": user_data}})












