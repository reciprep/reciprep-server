from flask import Blueprint, request, make_response, jsonify, g
from flask.views import MethodView
from flask_restful import Api, Resource, url_for

from api import bcrypt, db
from api.models.user import User
from api.decorators import is_logged_in

auth_blueprint = Blueprint('auth', __name__)
auth_api = Api(auth_blueprint)


class RegisterAPI(Resource):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter(
            (User.email == post_data.get('email')) | \
            (User.username == post_data.get('username'))
        ).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    username=post_data.get('username'),
                    password=post_data.get('password')
                )
                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject), 201)
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject), 401)
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please log in.',
            }
            return make_response(jsonify(responseObject), 202)


class LoginAPI(Resource):
    """
    User Login Resource
    """
    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(
                username=post_data.get('username')
            ).first()
            if user and bcrypt.check_password_hash(
                user.password, post_data.get('password')
            ):
                auth_token = user.encode_auth_token()
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(responseObject), 200)
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject), 404)
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject), 500)


class UserAPI(Resource):
    """
    User Resource
    """

    # Apply auth / user checks
    decorators = [is_logged_in]

    def get(self):
        user_id = g.user_id
        user = User.query.filter_by(id=user_id).first()
        responseObject = {
            'status': 'success',
            'data': {
                'user_id': user.id,
                'email': user.email,
                'username': user.username,
                'registered_on': user.registered_on
            }
        }
        return make_response(jsonify(responseObject), 200)


auth_api.add_resource(RegisterAPI, '/api/auth/register')
auth_api.add_resource(LoginAPI, '/api/auth/login')
auth_api.add_resource(UserAPI, '/api/auth/status')
