""" TODO: add tests """
import datetime
from functools import wraps

import jwt
from flask import jsonify, request


def encode_auth_token(string_id, secret_key):
    try:
        payload = {
            'iat': datetime.datetime.utcnow(),
            'sub': string_id,
        }
        return jwt.encode(payload, secret_key, algorithm='HS256')
    except Exception as e:
        return e


def decode_auth_token(auth_token, secret_key):
    try:
        payload = jwt.decode(auth_token, secret_key, algorithms=["HS256"])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


# decorator for flask views verifying the JWT
def token_required_fact(token_key, token_secret):
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split('Bearer ')[1]
            if not token:
                return jsonify({'message': 'Token is missing !!'}), 401
            try:
                decoded = decode_auth_token(token, token_secret)
            except:
                return jsonify({'message': 'Token is invalid !!'}), 401
            if decoded != token_key:
                return jsonify({'message': 'Token is invalid !!'}), 401

            return f(*args, **kwargs)

        return decorated

    return token_required
