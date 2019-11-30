from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mtg
from bson.json_util import dumps
import json

app = Flask(__name__)

# app.config["MONGO_URI"] = f"mongodb://{keys['userName']}:{keys['password']}@ds011268.mlab.com:11268/heroku_p589mnvp"

app.config["MONGO_URI"] = "mongodb://localhost:27017/mtg_app"
mongo = PyMongo(app)

@app.route('/')
def home():
    data = mongo.db.cards.find()
    # print(data)
    return jsonify(json.loads(dumps(data)))

@app.route('/scrape')
def scrape():
    old_data = mongo.db.cards.find()
    new_data = scrape_mtg.scrape_magic()
    print(json.loads(dumps(old_data)))
    
    for card1 in new_data:
        if card1 in old_data:
            for card2 in old_data:
                if card1['card_name'] == card2['card_name']:
                    # if card1['edition'].keys()[0] in card2['edition'].keys():
                    to_db = card2
                    edition = card1['edition'].keys()[0]
                    edition_dict = card1['edition'][edition]
                    date = edition_dict.keys()[0]
                    price = edition_dict[date]
                    to_db['edition'][edition][date]= price
                    mongo.db.cards.update({
                        "card_name": to_db['card_name']
                    }, to_db, upsert=True)
                    print('update')
        else:#needs work!!!!
             for card2 in new_data:
                if card1['card_name'] == card2['card_name']:
                    # if card1['edition'].keys()[0] in card2['edition'].keys():
                    to_db = card2
                    edition = card1['edition'].keys()[0]
                    edition_dict = card1['edition'][edition]
                    date = edition_dict.keys()[0]
                    price = edition_dict[date]
                    to_db['edition'][edition][date]= price
                    mongo.db.cards.update({
                        "card_name": to_db['card_name']
                    }, to_db, upsert=True)
                    print('update')
            print('new_card')
            mongo.db.cards.insert_one(card1)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)