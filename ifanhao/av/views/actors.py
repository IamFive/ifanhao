# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-5
#

from flask.blueprints import Blueprint
from ifanhao.common.web.renderer import smart_render
from ifanhao.av.models import Actor

bp_actors = Blueprint('actors', __name__)


@bp_actors.route('/', methods=['GET'])
@bp_actors.route('/<int:page>', methods=['GET'])
@smart_render()
def get_actor_list(page=1):
    pagination = Actor.query.paginate(page, per_page=24)
    return dict(pagination=pagination)

