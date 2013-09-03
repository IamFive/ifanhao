# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-5
#

from flask.blueprints import Blueprint
from ifanhao.common.web.renderer import smart_render

bp_torrents = Blueprint('torrents', __name__)

@bp_torrents.route('/', methods=['GET'])
@smart_render()
def index():
    pass



