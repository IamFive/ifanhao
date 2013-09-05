# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#

import os
from ifanhao.constants import ROOT

#------------- Application setting here. ---------------------

DEBUG = True
CSRF_ENABLED = False
SECRET_KEY = 'i am really not a secret key'

MEDIA_URL_PATH = '/m'
MEDIA_FOLDER = os.path.join(ROOT, 'medias')

SQLALCHEMY_DATABASE_URI = 'mysql://root:!@#456@127.0.0.1:3306/ifanhao'
SQLALCHEMY_ECHO = False


LOGGER_ROOT_LEVEL = 'DEBUG'
FILE_LOG_HANDLER_FODLER = os.path.join(ROOT, 'logs')
FILE_LOG_HANDLER_LEVEL = 'DEBUG'
LOG_FORMAT = (
    '[%(asctime)s] %(levelname)s *%(pathname)s:%(lineno)d* : %(message)s'
)

UPLOADS_DEFAULT_DEST = MEDIA_FOLDER
UPLOADS_DEFAULT_URL = MEDIA_URL_PATH
