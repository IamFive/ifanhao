# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-9-8
#
from ifanhao.av.models import Av
from flask.blueprints import Blueprint
from flask.helpers import url_for, make_response
from flask.templating import render_template


bp_sitemap = Blueprint('sitemap', __name__)

domain = 'http://www.mailoop.com'

@bp_sitemap.route('/sitemap/', methods=['GET'])
@bp_sitemap.route('/sitemap.xml', methods=['GET'])
@bp_sitemap.route('/sitemap_baidu.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    # user model pages
    avs = Av.query.order_by(Av.published_on).all()

    pages = []
    for av in avs:
        url = url_for('avs.get_av', code=av.code)
        modified_time = av.published_on.date().isoformat()
        pages.append([domain + url, modified_time])

    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response
