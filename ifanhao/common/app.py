# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-20
#

from ac_client.client import AcClient
from flask import Flask, render_template, request
from flask.globals import g, current_app
from flask.helpers import url_for
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from ifanhao.common import error_code
from ifanhao.common.exceptions import FriendlyException
from ifanhao.common.interceptors import setup_formdata_interceptor, \
    setup_render_as_interceptor
from ifanhao.common.tools.env import ResourceLoader
from ifanhao.common.tools.utils import mkdirs
from ifanhao.common.web.renderer import smart_render, JsonResp, RenderFormat, \
    ContentType
from ifanhao.constants import ROOT, STATIC_URL_PATH
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
from werkzeug.utils import redirect
import json
import os
from flaskext.uploads import configure_uploads
from werkzeug.wsgi import SharedDataMiddleware


app = None
db = None


def init_logger():

    log_format = app.config.get('LOG_FORMAT')
    if app.config.get('LOG_FORMAT'):
        app.debug_log_format = log_format;

    # setup root log format - global filter.
    app.logger.setLevel(app.config.get('LOGGER_ROOT_LEVEL'))
    log_file_folder = app.config.get('FILE_LOG_HANDLER_FODLER')
    mkdirs(log_file_folder, is_folder=True)

    filename = os.path.join(log_file_folder, app.import_name + '.log')
    file_handler = TimedRotatingFileHandler(filename=filename, when="midnight",
                                            backupCount=10)
    file_handler.suffix = "%Y%m%d"
    file_handler.setLevel(app.config.get('FILE_LOG_HANDLER_LEVEL'))
    file_handler.setFormatter(Formatter(log_format))
    app.logger.addHandler(file_handler)


def init_bp_modules():
    """add blueprint modules.
    """
    global app

    from ifanhao.comics.views import bp_comics
    app.register_blueprint(bp_comics, url_prefix='/comics')

    from ifanhao.av.views.avs import bp_avs
    app.register_blueprint(bp_avs, url_prefix='/a')

    from ifanhao.av.views.actors import bp_actors
    app.register_blueprint(bp_actors, url_prefix='/b')

    #    server media folder
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        app.config.get('MEDIA_URL_PATH') :  app.config.get('MEDIA_FOLDER')
    })

    @app.route('/api/version', methods=['GET'])
    @smart_render()
    def version_handler():
        from ifanhao import version
        return version()

    @app.route('/')
    @app.route('/index')
    @smart_render()
    def index():
        pass

    @app.route('/favicon.ico')
    def favicon():
        return redirect(url_for('static', filename='favicon.ico'))


def init_error_handler():

    global app

    def handler_ex(ex, status=400):

        status = ex.code if ex.code >= 400 and ex.code < 500 else 400

        if g.rformat == RenderFormat.HTML:
            return render_template('{0}.html'.format(status), error=ex), status

        if isinstance(ex, FriendlyException) and len(ex.msg_list) == 1:
            message = ex.msg_list[0]
        else:
            message = ex.msg_list
        resp = json.dumps(JsonResp.make_failed_resp(ex.code, message))

        if g.rformat == RenderFormat.JSON:
            return Response(resp, mimetype=ContentType.JSON), status
        elif g.rformat == RenderFormat.JSONP:
            callback = request.args.get('callback', False)
            if callback:
                content = "{}({})".format(callback, resp)
                return Response(content, mimetype=ContentType.JSONP,
                                status=200)
            return Response(resp, mimetype=ContentType.JSON, status=200)


    @app.errorhandler(404)
    def page_not_found(error):
        ex = FriendlyException.fec(error_code.RESOURCE_NOT_EXIST)
        return handler_ex(ex, 404)

    @app.errorhandler(FriendlyException)
    def friendly_ex_handler(ex):
        app.logger.exception(ex)
        status = ex.code if ex.code >= 400 and ex.code < 500 else 400
        return handler_ex(ex, status=status)

    @app.errorhandler(Exception)
    def exception_handler(error, status=400):
        app.logger.exception(error)
        ex = FriendlyException(400, str(error))
        return handler_ex(ex, status)


def init_interceptors():
    setup_render_as_interceptor(app)
    setup_formdata_interceptor(app)

    from ifanhao.common.web.contexts import (current_bp_processor,
                                             pro_version_processor)
    app.context_processor(current_bp_processor)
    app.context_processor(pro_version_processor)

    from ifanhao.common.web.filters import setup_filters
    setup_filters(app)


def setup_flask_initial_options():

    static_folder = ResourceLoader.get().configs.get('STATIC_FOLDER')
    template_folder = ResourceLoader.get().configs.get('TEMPLATE_FOLDER')
    if not static_folder:
        static_folder = os.path.join(ROOT, 'static')

    if not template_folder:
        template_folder = os.path.join(ROOT, 'templates')

    options = dict(static_url_path=STATIC_URL_PATH)
    options['static_folder'] = static_folder
    options['template_folder'] = template_folder
    return options



def init_db_engine():

    global db
    global app

    def remove_db_session(exception=None):
        db.session.remove()

    db = SQLAlchemy(app)
    app.db = db
    app.teardown_request(remove_db_session)

    # register models
    #    import icomic.comics.models
    import ifanhao.av.models


def init_uploads():
    from ifanhao.uploads import upload_list
    configure_uploads(app, upload_list)


# def init_ac_client():
#    app.ac_client = AcClient('http://m.ac.qq.com/')


def startup_app():

    global app

    if not app:
        args = setup_flask_initial_options()
        app = Flask('ifanhao', **args)

        app.config.update(ResourceLoader.get().configs)
        app.debug = app.config.get('DEBUG', True)
        init_logger()

        try:
            init_db_engine()
            init_error_handler()
            init_interceptors()
            init_bp_modules()
            init_uploads()
            app.logger.info('Start success from ROOT [%s] .', ROOT)
        except Exception, e:
            app.logger.error('Start Ifanhao faild!')
            app.logger.exception(e)
            raise e

    return app


def init_db():
    with current_app.app_context():

        db.create_all()

        folder_path = ResourceLoader.get().get_resoure('init-sql').path
        if folder_path and os.path.isdir(folder_path):
            for data_file in os.listdir(folder_path):
                with open(folder_path + os.path.sep + data_file, 'r') as mqls:
                    db.engine.execute(mqls.read())

def clear_db():
    with current_app.app_context():
        db.drop_all()
