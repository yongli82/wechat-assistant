#!/usr/bin/env python
# -*- coding:utf-8 -*-


import logging
import os

from flask import Blueprint, request, make_response
from flask import jsonify
from werkzeug import secure_filename

import config
from ext import db
from models import Album, Photo, PhotoGroup

logger = logging.getLogger(__name__)

bp = Blueprint('api', __name__)

PER_PAGE = 10


def register_api(app):
    app.register_blueprint(bp, url_prefix='')


@bp.route('/')
def hello_world():
    return 'Hello World!'


@bp.route("/api/albums", methods=['GET'])
def query_albums():
    albums = []
    page = int(request.values.get("page") or 1)
    album_paginate = Album.query.paginate(page, PER_PAGE, False)
    album_models = album_paginate.items
    for album_model in album_models:
        an_album = {
            "id": album_model.id,
            "name": album_model.name,
            "photoTotal": album_model.photo_count,
            "formatUpdateTime": album_model.formated_updated_time,
        }
        albums.append(an_album)
    response = make_response(jsonify(albums))
    response.headers["X-Pagination-Page-Count"] = album_paginate.pages
    response.headers["X-Pagination-Current-Page"] = album_paginate.page
    return response


@bp.route("/api/albums", methods=['POST'])
def add_album():
    name = request.json.get("name")
    desc = request.json.get("description")

    album_model = Album(name=name, desc=desc)
    db.session.add(album_model)
    db.session.commit()
    an_album = {
        "id": album_model.id,
        "name": album_model.name,
        "photoTotal": album_model.photo_count,
        "formatUpdateTime": album_model.formated_updated_time,
    }

    return make_response(jsonify(an_album))


@bp.route("/api/photos", methods=['POST'])
def add_photos():
    album_id = request.values.get("album_id")
    description = request.values.get("description")
    photo_group = PhotoGroup(album_id=album_id, desc=description)
    db.session.add(photo_group)
    db.session.commit()
    data = {"id": photo_group.id, "album_id": album_id, "description": description}
    response = make_response(jsonify(data), 201)
    return response


@bp.route("/api/photo-items", methods=['POST'])
def add_photo_item():
    return add_media_item('photo')


@bp.route("/api/video-items", methods=['POST'])
def add_video_item():
    return add_media_item('video')


def add_media_item(media_type):
    logger.info("add_media_item %s" % media_type)
    file = request.files['file']
    filename = file.filename
    group_id = request.values.get("group_id")
    album_id = request.values.get("album_id")
    secured_filename = secure_filename(filename)
    file_path = os.path.join(config.UPLOAD_FOLDER, secured_filename)
    file.save(file_path)
    logger.info("save file %s to file path %s" % (filename, file_path))
    # file_url = url_for('uploaded_file', filename=filename)
    file_url = "/static/upload/" + secured_filename
    photo = Photo(album_id=album_id, group_id=group_id, url=file_url, media_type=media_type, name=filename)
    db.session.add(photo)
    db.session.commit()
    data = {
        "photo_id": photo.id,
        "album_id": album_id,
        "group_id": group_id,
        "file_url": file_url
    }
    return make_response(jsonify(data))


@bp.route("/api/photo-items", methods=['GET'])
def query_photo_items():
    album_id = request.values.get("album_id")
    page = int(request.values.get("page") or 1)
    data = []
    logger.info("query_photo_items in album %s and page %s" % (album_id, page))
    photo_groups_paginate = PhotoGroup.query.filter(PhotoGroup.album_id == album_id).paginate(page, PER_PAGE, False)
    photo_groups = photo_groups_paginate.items
    for photo_group in photo_groups:
        photos = Photo.query.filter(Photo.group_id == photo_group.id).all()
        group_items = [{"path": photo.url} for photo in photos]
        data.append({
            "description": photo_group.desc,
            "photos": group_items
        })

    response = make_response(jsonify(data))
    response.headers["X-Pagination-Page-Count"] = photo_groups_paginate.pages
    response.headers["X-Pagination-Current-Page"] = photo_groups_paginate.page
    return response
