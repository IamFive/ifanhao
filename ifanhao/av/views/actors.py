# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-5
#

from flask.blueprints import Blueprint
from ifanhao.common.web.renderer import smart_render

bp_actors = Blueprint('actors', __name__)


@bp_actors.route('/', methods=['GET'])
@smart_render()
def get_av_list(page=1):
    return dict()

