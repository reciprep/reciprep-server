from flask import Blueprint, request, make_response, jsonify, g
from functools import wraps

"""
Decorators for checking client auth status
"""

def is_logged_in(f):
    """
    Decorator for checking if a User is logged in
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # get the auth token
            auth_header = request.headers.get('Authorization')
            if auth_header:
                auth_token = auth_header.split(" ")[1]
            else:
                auth_token = ''
            if auth_token:
                resp = User.decode_auth_token(auth_token)
                if not isinstance(resp, str):
                    return f(*args, **kwargs)
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Provide a valid auth token.'
                }
                return make_response(jsonify(responseObject)), 401

        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Something went wrong.'
            }
            return make_response(jsonify(responseObject)), 401
    return decorated_function

def has_verified_email(f):
    """
    Decorator for checking if a User has verified their email
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            #### TODO perform verified email check here
            return f(*args, **kwargs)
        except Exception as e:
            print(e)
            return "Something went wrong."
    return decorated_function
