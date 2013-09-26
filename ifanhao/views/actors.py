# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-5
#

from flask.blueprints import Blueprint
from ifanhao.common.web.renderer import smart_render
from ifanhao.models import Actor
from flask.globals import g
from sqlalchemy.sql.expression import desc

bp_actors = Blueprint('actors', __name__)


@bp_actors.route('/', methods=['GET'])
@bp_actors.route('/<int:page>', methods=['GET'])
@smart_render()
def get_actor_list(page=1):

    # filter conditions
    k = g.formdata.get('k', '')

    q = Actor.query
    if k:
        like_str = '%' + k + '%'
        q = q.filter(Actor.name.like(like_str) | Actor.cn_name.like(like_str))

    pagination = q.order_by(desc(Actor.cup)).paginate(page, per_page=12)

    return dict(pagination=pagination, k=k)

