# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-6-16
#

__test__ = False

from ifanhao.common.app import startup_app
from ifanhao.common.tools.env import ResourceLoader

# os.environ.setdefault(ResourceLoader.ENV_VAR_NAME,
#                     '/var/www/vhosts/icomic/resources/prod')
application = startup_app()
