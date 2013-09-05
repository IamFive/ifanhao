# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-20
#
from ifanhao.common.app import db
from ifanhao.common.sa_orm_ext import BaseModelMixin
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import Integer, String, Date
from sqlalchemy.orm import relationship


class Tag(db.Model, BaseModelMixin):

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    category = Column(String(32), nullable=False)

    def __repr__(self):
        return '<Tags name::{}>'.format(self.name.encode('utf-8'))


class Actor(db.Model, BaseModelMixin):

    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    cn_name = Column(String(64), nullable=False)
    avatar = Column(String(64))
    birth = Column(Date)
    height = Column(Integer)
    weight = Column(Integer)
    cup = Column(String(1))
    chest = Column(Integer)
    waist = Column(Integer)
    hip = Column(Integer)

    def __repr__(self):
        return '<Actor name::{}>'.format(self.name.encode('utf-8'))


class Publisher(db.Model, BaseModelMixin):

    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)

    def __repr__(self):
        return '<Publisher name::{}>'.format(self.name.encode('utf-8'))


av_2_tag = Table('av_2_tag', db.metadata,
    Column('av_id', Integer, ForeignKey('avs.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

av_2_actor = Table('av_2_actor', db.metadata,
    Column('av_id', Integer, ForeignKey('avs.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)


class Av(db.Model, BaseModelMixin):

    __tablename__ = 'avs'

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    code = Column(String(16), nullable=False)
    published_on = Column(Date, nullable=False)
    length = Column(Integer, nullable=False)
    director = Column(String(64))
    maker = Column(String(64))
    publisher = Column(String(256))

    tags = relationship('Tag', secondary=av_2_tag,
                        order_by=Tag.id,
                        backref='avs')
    actors = relationship('Actor', secondary=av_2_actor,
                        backref='avs')


    def __repr__(self):
        return '<Av code::{}>'.format(self.code.encode('utf-8'))

