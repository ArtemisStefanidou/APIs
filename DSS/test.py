import pymongo

myclient = pymongo.MongoClient('localhost', 27017)
mydb = myclient["dock-mongo_mongodb_1"]

mycol = mydb["gap_events"]

gap_event = {
	"vessel_id": 000000000,
	"gap_start": 1689692459,
	"lon_start": 37.83,
	"lat_start": 37.83,
	"gap_end": 1689692469,
	"lon_end": 37.83,
	"lat_end": 37.84
}

myquery = { "vessel_id": 0 }

for x in mycol.find(myquery):
  print(x)
