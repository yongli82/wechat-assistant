#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask

import album
import config
from ext import db


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

    album.register_api(app)

    return app


__all__ = ['create_app']
