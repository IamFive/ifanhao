# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-9-3
#
from ifanhao.common.app import startup_app

app = startup_app()
app.run('0.0.0.0', 5000, True)
