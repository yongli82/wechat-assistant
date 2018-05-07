#!/usr/bin/env python
# -*- coding:utf-8 -*-


import logging
from datetime import datetime

from flask import Blueprint, request, make_response
from flask import jsonify

from ext import db
from marshmallow import Schema, fields, pprint

##### MODELS #####

class TaskItem(db.Model):
    """
    任务
    """
    __tablename__ = "task_item"
    TODO = 1
    DONE = 2

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Unicode(255))
    name = db.Column(db.Unicode(255))
    status = db.Column(db.Integer, default=TODO)
    desc = db.Column(db.Unicode(255))
    note = db.Column(db.UnicodeText)
    list_id = db.Column(db.Integer)
    due_date = db.Column(db.DateTime, index=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)
    update_at = db.Column(db.DateTime, index=True, default=datetime.now)

    __mapper_args__ = {'order_by': [id]}

    def __repr__(self):
        return '<TaskItem %s>' % self.name

    def __unicode__(self):
        return self.name

class TaskList(db.Model):
    __tablename__ = "task_list"

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Unicode(255))
    name = db.Column(db.Unicode(255))
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)
    update_at = db.Column(db.DateTime, index=True, default=datetime.now)

    __mapper_args__ = {'order_by': [id]}

    def __repr__(self):
        return '<TaskList %s>' % self.name

    def __unicode__(self):
        return self.name


class TaskItemSchema(Schema):
    id = fields.Int()
    owner = fields.Str()
    name = fields.Str(required=True)
    status = fields.Integer()
    desc = fields.Str()
    note = fields.Str()
    list_id = fields.Integer()
    due_date = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)
    update_at = fields.DateTime(dump_only=True)
    
class TaskListSchema(Schema):
    id = fields.Int()
    owner = fields.Str()
    name = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    update_at = fields.DateTime(dump_only=True)

taskItemSchema = TaskItemSchema()
taskListSchema = TaskListSchema()

logger = logging.getLogger(__name__)

bp = Blueprint('task', __name__)

PER_PAGE = 10


def register_api(app):
    app.register_blueprint(bp, url_prefix='/task')


@bp.route('/')
def hello_world():
    return 'Hello Task!'


@bp.route('/api/task/lists', methods=['GET'])
def list_task_lists():
    task_lists = TaskList.query.all()
    data = taskListSchema.dump(task_lists, many=True).data
    response = make_response(jsonify(data))
    return response


@bp.route('/api/task/lists', methods=['POST', 'PUT'])
def save_task_list():
    data = request.json
    task_list = TaskList(**data)
    task_list.update_at = datetime.now()
    db.session.add(task_list)
    db.session.commit()
    data = taskListSchema.dump(task_list, many=False).data
    response = make_response(jsonify(data))
    return response


@bp.route('/api/task/lists/<id>', methods=['GET'])
def get_task_list(id):
    list_id = int(id)
    task_list = TaskList.query.filter(TaskList.id == list_id).first()
    data = taskListSchema.dump(task_list, many=False).data
    response = make_response(jsonify(data))
    return response


@bp.route('/api/task/lists/<id>', methods=['DELETE'])
def delete_task_list(id):
    list_id = int(id)
    task_list = TaskList.query.filter(TaskList.id == list_id).first()
    db.session.delete(task_list)
    db.session.commit()
    data = taskListSchema.dump(task_list, many=False).data
    response = make_response(jsonify(data))
    return response


@bp.route('/api/task/items', methods=['GET'])
def list_tasks():
    if request.values.get("list_id"):
        list_id = int(request.values.get("list_id") or 1)
        task_items = TaskItem.query.filter(TaskItem.list_id == list_id).all()
    else:
        task_items = TaskItem.query.all()
    data = taskItemSchema.dump(task_items, many=True).data
    response = make_response(jsonify(data))
    return response


@bp.route('/api/task/items', methods=['POST', 'PUT'])
def save_task():
    data = request.json
    data = taskItemSchema.load(data).data
    task_item = TaskItem(**data)
    task_item.update_at = datetime.now()
    db.session.add(task_item)
    db.session.commit()
    data = taskItemSchema.dump(task_item, many=False).data
    response = make_response(jsonify(data))
    return response


@bp.route('/api/task/items/<id>', methods=['GET'])
def get_task(id):
    item_id = int(id)
    task_item = TaskItem.query.filter(TaskItem.id == item_id).first()
    data = taskItemSchema.dump(task_item, many=False).data
    response = make_response(jsonify(data))
    return response


@bp.route('/api/task/items/<id>', methods=['DELETE'])
def delete_task(id):
    item_id = int(id)
    task_item = TaskItem.query.filter(TaskItem.id == item_id).first()
    db.session.delete(task_item)
    db.session.commit()
    data = taskItemSchema.dump(task_item, many=False).data
    response = make_response(jsonify(data))
    return response
