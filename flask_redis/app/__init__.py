from flask import Flask
import redis

app = Flask(__name__)
app.config.from_object('config')
db = redis.Redis(host=app.config['REDISHOST'],
                 port=app.config['REDISPORT'])  # connect to server

from app import views
