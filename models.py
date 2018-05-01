#!/usr/bin/env python
# -*- coding:utf-8 -*-


from datetime import datetime
from werkzeug import cached_property
from ext import db


class PhotoGroup(db.Model):
    """
    媒介: 照片或视频
    """
    __tablename__ = "photo_groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255))
    desc = db.Column(db.Unicode(255))
    url = db.Column(db.Unicode(255))
    album_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)

    __mapper_args__ = {'order_by': [id]}

    def __repr__(self):
        return '<MediaGroup %s>' % (self.name or self.url)

    def __unicode__(self):
        return self.name
    
class Photo(db.Model):
    """
    媒介: 照片或视频
    """
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255))
    desc = db.Column(db.Unicode(255))
    url = db.Column(db.Unicode(255))
    album_id = db.Column(db.Integer)
    group_id = db.Column(db.Unicode(32))
    media_type = db.Column(db.Unicode(32))
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)

    __mapper_args__ = {'order_by': [id]}

    def __repr__(self):
        return '<Media %s>' % (self.name or self.url)

    def __unicode__(self):
        return self.name


class Album(db.Model):
    """相册"""

    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64), nullable=False)
    desc = db.Column(db.Unicode(255))
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.now)

    __mapper_args__ = {'order_by': [id]}

    def __repr__(self):
        return '<Album %r>' % self.name

    def __unicode__(self):
        return self.name

    @cached_property
    def formated_updated_time(self):
        return self.updated_at.strftime("%Y-%m-%d")

    # 相册相片数
    @cached_property
    def photo_count(self):
        return Photo.query.filter_by(album_id=self.id).count()
