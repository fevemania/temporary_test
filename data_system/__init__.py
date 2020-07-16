from flask import Flask, request, g
from flask_restful import Api

import os
import click
import base64
import json

from data_system.config import config
from data_system.extensions import jwt
#from data_system.models.user import User
from data_system.resources.token import TokenResource, RefreshResource
from data_system.utils import check_username_query

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)
#   register_command(app)
    register_resources(app)

    return app

def register_extensions(app):
    jwt.init_app(app)

#def register_command(app):
#    @app.cli.command()
#    @click.option('--drop', is_flag=True, help='Create after drop.')
#    def init(drop):
#        if drop:
#            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
#            db.drop_all()
#            click.echo('Drop tables.')
#        db.create_all()
#        click.echo('Initialized database and file upload folders.')
#
#    @app.cli.command()
#    @click.option('--username', prompt=True, help='The username used to login.')
#    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
#    def create_user(username, password):
#        click.echo('Creating the new user...')
#        user = User(username=username)
#        user.set_password(password)
#        db.session.add(user)
#        db.session.commit()

def register_resources(app):
    api = Api(app)

    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
