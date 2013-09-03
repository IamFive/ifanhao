# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-5
#

from flask.blueprints import Blueprint
from ifanhao.common.web.renderer import smart_render
from ifanhao.av.models import Av, Tag, Actor
from flask.globals import g, current_app
from sqlalchemy.sql.expression import func, desc

bp_avs = Blueprint('avs', __name__)


@bp_avs.route('/', methods=['GET', 'POST'])
@bp_avs.route('/<int:page>', methods=['GET', 'POST'])
@smart_render()
def get_av_list(page=1):

    categories = Tag.query.order_by(Tag.id).all()

    # filter conditions
    k = g.formdata.get('k', '')
    tags = g.formdata.getlist('tags', int)

    q = Av.query
    if len(tags):
        grouped_tags = current_app.db.session.query(func.group_concat(Tag.id))\
                        .filter(Tag.id.in_(tags)).group_by(Tag.category).all()

        for grouped in grouped_tags:
            splitted = grouped[0].split(',')
            q = q.filter(Av.tags.any(Tag.id.in_(splitted)))

    if k:
        like_str = '%' + k + '%'
        q = q.filter(Av.code.like(like_str) | Av.title.like(like_str) |
                     Av.actors.any(Actor.name.like(like_str)))


    pagination = q.order_by(desc(Av.published_on)).paginate(page)
    return dict(pagination=pagination, categories=categories,
                k=k, tags=tags)


@bp_avs.route('/<code>', methods=['GET'])
@smart_render()
def get_av(code):
    av = Av.query.filter_by(code=code).one()
    return dict(av=av)

