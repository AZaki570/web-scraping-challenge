from flask import Flask
from scrape_mars import scrape
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo

import certifi
ca = certifi.where()
app = Flask(__name__)

#################################################
# PyMongo Connection Setup
#################################################
app.config["MONGO_URI"] = "mongodb+srv://user1:pr3HdpivD9iaPsBQ@cluster0.h9yuk.mongodb.net/database?retryWrites=true&w=majority"

mongo = PyMongo(app, tlsCAFile=ca)


@app.route("/")
def index():
    mars = mongo.db['mars'].find_one()['data']
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape_route():
    mars = mongo.db['mars']
    data = scrape()
    mars.update({}, data, upsert=True)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
