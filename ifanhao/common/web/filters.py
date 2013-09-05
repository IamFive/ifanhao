# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#
import urllib
from markdown import markdown
from flask import Markup

def setup_filters(app):

    def urlencode_filter(s):
        if type(s) == 'Markup':
            s = s.unescape()
        s = s.encode('utf8')
        s = urllib.quote_plus(s)
        return Markup(s)

    def markdown_filter(data):
        return Markup(markdown(data))

    app.add_template_filter(urlencode_filter, name='urlencode')
    app.add_template_filter(markdown_filter, name='markdown')

