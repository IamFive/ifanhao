# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-20
#
from datetime import datetime
from ifanhao.common.app import db
from ifanhao.common.sa_orm_ext import BaseModelMixin
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime, Unicode


class Comic(db.Model, BaseModelMixin):

    __tablename__ = 'comics'

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    artist_name = Column(String(64))
    cover_url = Column(String(256))
    brief_intrd = Column(String(512))
    external_id = Column(Integer)
    lated_seqno = Column(Integer)

    type_name = Column(String(16)) # 类型：故事
    theme = Column(String(16)) # 题材：魔幻 动作 冒险
    sole_state = Column(Integer) # 1:连载中? 2:独家

    # don't know what does those two means
    grade_count = Column(Integer)
    total_grade = Column(Integer)

    def __repr__(self):
        return '<Comic title::{}>'.format(self.title.encode('utf-8'))


class Chapter(db.Model, BaseModelMixin):

    __tablename__ = 'chapters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    comic_id = Column(Integer, ForeignKey('comics.id'), nullable=False)
    title = Column(Unicode(128), nullable=False)
    seq = Column(Integer, nullable=False)
    updated_on = Column(DateTime, default=datetime.now(), nullable=False)


    def __init__(self, comic_id, title, seq):
        self.comic_id = comic_id
        self.title = title
        self.seq = seq

    def __repr__(self):
        return '<Chapter title::{}>'.format(self.title.encode('utf-8'))
