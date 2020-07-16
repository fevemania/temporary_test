from http import HTTPStatus
from flask import request, current_app, g
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    jwt_refresh_token_required
)
import pyotp
from marshmallow import ValidationError
from werkzeug.security import check_password_hash

import pdb
import datetime
import os
from pprint import pprint

#from data_system.models.user import User
from data_system.schemas.user import UserSchema 
from data_system.utils import check_username_query, check_jwt_payload, upload_blob

user_schema = UserSchema()

class TokenResource(Resource):

    def post(self):
        json_data = request.get_json()
        try:
            data = user_schema.load(data=json_data)
        except ValidationError as err:
            if json_data is None:
                return ({'message': 'Validation errors', 'errors': 'input should not be None'}, 
                        HTTPStatus.BAD_REQUEST)
            return {'message': 'Validation errors', 'errors': err.messages}, HTTPStatus.BAD_REQUEST
        
        # check if the username exists 
        query_job = check_username_query(data.get('unique_id'))

        UNIQUE_ID_CHECK = False
        PASSWORD_CHECK = False
        for row in query_job:
            UNIQUE_ID_CHECK = True
            # check if the password match and totp_code match
            totp = pyotp.TOTP(row.totp_key)
            for totp_code in data.get('totp_codes'):
                if totp.verify(totp_code) and check_password_hash(row.password_hash, data.get('password')):
                    PASSWORD_CHECK = True
                    current_app.config['JWT_PRIVATE_KEY'] = row.jwt_private_key
                    access_token = create_access_token(identity=row.unique_id, fresh=True)
                    refresh_token = create_refresh_token(identity=row.unique_id)
                    return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK

        if not UNIQUE_ID_CHECK or not PASSWORD_CHECK:
            return {'message': 'invalid_request'}, HTTPStatus.UNAUTHORIZED


class RefreshResource(Resource):

    @jwt_refresh_token_required
    def post(self):
        pdb.set_trace()
        current_user = get_jwt_identity()

        token = create_access_token(identity=current_user, fresh=False)

        return {'token': token}, HTTPStatus.OK

# only for development
class CsvUploadResource(Resource):
    @check_jwt_payload
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()

        upload_blob('project-name', request.files['data'], os.path.join('transport', current_user + '_' + request.files['data'].filename))
        return {}, HTTPStatus.CREATED
