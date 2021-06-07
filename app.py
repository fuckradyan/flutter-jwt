from flask import Flask, jsonify, request, make_response
import jwt
import datetime
import base64
from functools import wraps
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message' : 'TOKEN IS MISSING'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'INVALID TOKEN'}), 403
        return f(*args, **kwargs)
    return decorated


@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Каждый видит это сообщение'})




@app.route('/protected')
@token_required
def protected():
    with open("obama.jpg", "rb") as image_file:
        message_string = base64.b64encode(image_file.read())
    return jsonify({'message' : 'Только аутентифицированные пользователи видят это сообщение.','time' : datetime.datetime.now(), 'img' :  str(message_string.decode('utf-8'))})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    # auth = request.authorization
    print(data.username)
    if auth and auth.password == 'admin':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=40)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})    
    return make_response('Could not verify!',401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

    return jsonify({data})


if __name__ == '__main__':
    app.run(debug=True)
