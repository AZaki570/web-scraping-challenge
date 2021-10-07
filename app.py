from flask import Flask
from scrape_mars import scrape
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

#################################################
# PyMongo Connection Setup
#################################################
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# You need to create a database named mars_app and collection name mars using mongodb compass
mongo = PyMongo(app)


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
