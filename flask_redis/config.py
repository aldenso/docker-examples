import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "my-very-long-super-secret-key"
REDISHOST = os.getenv("REDISHOST")
REDISPORT = os.getenv("REDISPORT")
