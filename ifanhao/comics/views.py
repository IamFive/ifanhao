# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-5
#

from flask.blueprints import Blueprint
from ifanhao.common.web.renderer import smart_render
from ifanhao.comics.models import Comic, Chapter

bp_comics = Blueprint('comics', __name__)


@bp_comics.route('/', methods=['GET'])
@smart_render()
def get_all():
    comics = Comic.query.all()
    return dict(comics=comics)


@bp_comics.route('/<int:comic_id>', methods=['GET'])
@smart_render()
def get_one(comic_id):
    comic = Comic.query.filter_by(id=comic_id).one()
    chapters = Chapter.query.filter_by(comic_id=comic_id).all()
    return dict(comic=comic, chapters=chapters)
