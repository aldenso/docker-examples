from flask import render_template, jsonify, abort, make_response, request
from app import app, db

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Avoid html response for errors
@app.errorhandler(404)
def not_found(error):
    """Return json response for not found."""
    return make_response(jsonify({'error': 'Not found'}), 404)


# Avoid html response for errors
@app.errorhandler(400)
def bad_request(error):
    """Return json response for bad request."""
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/')
@app.route('/index')
def index():
    title = "Flask Voting App"
    paragraph = ["Simple app to query a redis db."]

    candidates = db.keys(pattern="*")
    alldata = {}
    if not candidates:
        return jsonify({'message': 'No candidates!'})
    else:
        candidates = [item.decode('utf-8') for item in candidates]
        for i in candidates:
            values = db.hmget(i, "votes")
            if values != [None]:
                values = [val.decode('utf-8') for val in values]
                alldata[i] = int("".join(values))
    print(alldata)
    return render_template("index.html", title=title, paragraph=paragraph, candidates=alldata)


@app.route('/voting/api/v1/candidates', methods=['POST'])
def create_candidate():
    """Create new candidate."""
    if not request.json or 'name' not in request.json:
        abort(400)
    candidate = {'votes': 0}  # 0 votes
    check = db.keys(pattern=request.json['name'])
    if check:
        return jsonify({'error': 'candidate already exists.'}), 400
    else:
        db.hmset(request.json['name'], candidate)
        return jsonify({'message': "created."}), 201


@app.route('/voting/api/v1/candidates', methods=['GET'])
def get_candidates():
    """Get Candidates."""
    candidates = db.keys(pattern="*")
    if not candidates:
        return jsonify({'message': 'No candidates!'})
    else:
        candidates = [item.decode('utf-8') for item in candidates]
        alldata = {}
        for i in candidates:
            values = db.hmget(i, "votes")
            if values != [None]:
                # convert from byte list to dict with int
                alldata[i] = dict([("votes", int(key.decode('utf-8'))) for key in values])
        return jsonify({'candidates': alldata})

@app.route('/voting/api/v1/candidates/name/<string:name>', methods=['GET'])
def get_candidate(name):
    """Get Candidates."""
    candidate = db.hmget(name, "votes")
    if candidate == [None]:
        return jsonify({'error': 'No Candidate!'}), 400
    else:
        # convert from byte list to int
        candidate = int("".join([key.decode('utf-8') for key in candidate]))
        return jsonify({'votes': candidate})


@app.route('/voting/api/v1/candidates/name/<string:name>', methods=['DELETE'])
def delete_candidate(name):
    """Create new candidate."""
    if not db.keys(name):
        return jsonify({'error': 'candidate does not exists.'}), 404
    db.delete(name)
    return "", 204

@app.route('/voting/api/v1/candidates/name/<string:name>', methods=['PUT'])
def vote_candidate(name):
    """Create new candidate."""
    if not db.keys(name):
        return jsonify({'error': 'candidate does not exists.'}), 404
    db.hincrby(name, "votes", amount=1)
    return "", 204