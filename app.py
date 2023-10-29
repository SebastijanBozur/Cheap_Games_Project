from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request
from flask import redirect
from database import load_database
from database import save_database
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
import os
import requests
import time as tm
import click
from flask.cli import with_appcontext
from sqlalchemy import func


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'games.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

alembic = Alembic()
alembic.init_app(app)


class UserGame(db.Model):
    gameid = db.Column(db.Integer)
    userid = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)

class Gamedeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    internalName = db.Column(db.String(120), unique=True)
    title = db.Column(db.String(200), unique=False)
    metacriticLink = db.Column(db.String(1024), unique=False)
    dealID = db.Column(db.String(200), unique=False)
    storeID = db.Column(db.Integer, unique=False)
    gameID = db.Column(db.Integer, unique=False)
    salePrice = db.Column(db.Double, unique=False)
    normalPrice = db.Column(db.Double, unique=False)
    isOnSale = db.Column(db.Integer, unique=False)
    savings = db.Column(db.Double, unique=False)
    metacriticScore = db.Column(db.Integer, unique=False)
    steamRatingText = db.Column(db.String(200), unique=False)
    steamRatingPercent = db.Column(db.Integer, unique=False)
    steamRatingCount = db.Column(db.Integer, unique=False)
    steamAppID = db.Column(db.Integer, unique=False)
    releaseDate = db.Column(db.Integer, unique=False)
    lastChange = db.Column(db.Integer, unique=False)
    dealRating = db.Column(db.Double, unique=False)
    thumb = db.Column(db.String(1024), unique=False)


# https://www.cheapgames.com/
@app.route('/')
def main_page():
    return render_template('index.html')


def game_deals(store, page):
    url = f"https://www.cheapshark.com/api/1.0/deals?storeID={store}&upperPrice=15&pageNumber={page}"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json(),int(response.headers['X-Total-Page-Count'])

@click.command(name='download_games')
@with_appcontext
def download_games():
    store = [1, 2, 3, 7, 11, 15, 21, 23, 25, 27]

    for storeid in store:
        page = 0
        max_pages = 1
        while page < max_pages:
            print(storeid, page, max_pages)
            deals, max_pages = game_deals(store[storeid], page)
            for deal in deals:
                gamedeal = db.session.query(Gamedeal).filter(Gamedeal.internalName==deal['internalName']).first()
                if not gamedeal:
                    gamedeal = Gamedeal(**deal)
                else:
                    for k,v in deal.items():
                        setattr(gamedeal, k, v)
                db.session.add(gamedeal)
            db.session.commit()
            page += 1
            tm.sleep(5)


app.cli.add_command(download_games)


@click.command(name='recommendation')
@with_appcontext
def recommendation():
     recommendations = db.session.query(UserGame.gameid,
                  func.count(UserGame.gameid).label('total')).group_by(UserGame.gameid).order_by('total').all()[::-1]
     print(recommendations)

app.cli.add_command(recommendation)


def game_deal_update(gamedeal):
    pass


@app.route("/media/<path:name>")
def download_file(name):
    return send_from_directory(
      'media', name, as_attachment=False
    )


@app.route('/add-user', methods=['GET','POST'])
def add_user():
    name = request.args.get['name']
    height = int(request.args.get['height'])
    city = request.args.get['city']

    data = load_database()
    data[name] = {
        'height': height,
        'city': city
    }
    save_database(data)
    return redirect('/users')
    # data = load_database()
    # return render_template('add-user.html', users=data)


# https://www.cheapgames.com/users
@app.route('/users')
def users():
    data = load_database()
    return render_template('test.html', users=data)


# https://www.cheapgames.com/dynamic-value/
@app.route('/user-info/<name>')
def dynamic_func(name):
    data = load_database()
    user_data = data.get(name)
    return render_template(
        'user-info.html',
        user_name=name,
        user_data=user_data
    )

