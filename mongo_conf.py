from mongoengine import *
from datetime import datetime
import inflect
import pymongo
from pushbullet.pushbullet import PushBullet

def get_var_value(filename="varstore.dat"):
    with open(filename, "r") as f:
        val = int(f.read() or 0)
        return val

def increase_var_value(filename="varstore.dat"):
    with open(filename, "r+") as f:
        val = int(f.read() or 0) + 1
        f.seek(0)
        f.truncate()
        f.write(str(val))
        return val

next_day = get_var_value()
p = inflect.engine()
initial_day = next_day-1
initial_day = p.number_to_words(initial_day)
next_day = p.number_to_words(next_day)

print(" Next day {}".format(next_day))
print(" Initial day {}".format(initial_day))


try:
    connect(
        db='Takealot_DB',
        host="mongodb://localhost:27017/"
    )
    print("Connection successful")
    

except:
    print("Unable to connnect")

class GraphicsCards(Document):
    item_name = StringField(max_length=200, required=True)
    item_price = IntField(default=0)
    meta = {'collection': 'graphics_cards_day_{}'.format(next_day)}

def compare_collections():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient["Takealot_DB"]
    collectionA = "graphics_cards_day_{}".format(initial_day)
    collectionB="graphics_cards_day_{}".format(next_day) 
    print(collectionA, collectionB)
    apiKey = "GET YOUR OWN API KEY"
    p = PushBullet(apiKey)
    # Get a list of devices
    devices = p.getDevices()

    x = get_var_value()
    print("THIS IS THE VARSTORE VALUE: {}".format(x))
    y = x-1
    print("THIS IS THE VARSTORE VALUE MINUS 1: {}".format(y))
    if x<2:
        print("Nothing to compare. Program must run at least twice.")
    else:
        for item in db.get_collection(collectionA).find():
            item_name = item['item_name']
            item2 = db.get_collection(collectionB).find_one({'item_name':item_name})

            result= "\n Price change is {} for item {} with original price being {} in collection A,\n and item {} with original price being {} in collection B.\n The difference is {}".format(
            item['item_price'] > item2['item_price'], item['item_name'], item['item_price'], item2['item_name'], 
            item2['item_price'], item['item_price'] - item2['item_price'])

            p.pushNote(devices[0]["iden"], 'Scraping completed', result)
