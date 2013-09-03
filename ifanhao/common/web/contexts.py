# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-24
#
from flask.globals import request, current_app

def current_bp_processor():
    if request.endpoint:
        bp = request.endpoint.split('.')[0]
        current_app.logger.debug('current bp is: {}'.format(bp))
        return dict(bp=bp)
    return dict()
