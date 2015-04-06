from app import app
import os

@app.route('/')
@app.route('/index')
def index():
	return "Hello from Docker container: %s" % os.environ['HOSTNAME']
