#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/upload")
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(BASE_DIR, 'data_dev_sqlite.db')
