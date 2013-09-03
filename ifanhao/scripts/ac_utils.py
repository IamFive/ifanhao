# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-21
#
from flask.globals import current_app
from ifanhao.schemes import schema_comic
from ifanhao.comics.models import Comic, Chapter


def pull(comic_id=505432):
    """
    pull a comic from MAC
    :param comic_id: 505432 for naruto
    """

    with current_app.app_context():

        ac_client = current_app.ac_client

        current_app.logger.info('Pull Comic<id::{}> from m.ac.qq.com'
                                .format(comic_id))

        summary = ac_client.Comic.summary(comic_id)
        summary['external_id'] = summary.pop('id')

        c = Comic()
        c.fromdict(schema_comic.deserialize(summary))
        current_app.db.session.add(c)
        current_app.db.session.commit()

        chapters = ac_client.Chapter.list(comic_id)

        for chapter in chapters:
            current_app.db.session.add(Chapter(c.id, chapter.get('t'),
                                               chapter.get('seq')))
        current_app.db.session.commit()




