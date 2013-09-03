# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#
from flask_script import Manager
from ifanhao.common.app import startup_app

manager = Manager(startup_app)


@manager.command
def initdb():
    """ Initialize database . """
    from ifanhao.common.app import init_db
    init_db()


@manager.command
def cleardb():
    """Clear database ."""
    from ifanhao.common.app import clear_db
    clear_db()


@manager.command
def reinitdb():
    """ Initialize database . """
    from ifanhao.common.app import init_db, clear_db
    clear_db()
    init_db()


@manager.option("-c", "--cid", dest='cid',
                default=505432, help="comic id of ac.qq.com")
def acpull(cid):
    from ifanhao.scripts import ac_utils
    ac_utils.pull(cid)


@manager.command
def acinit():
    from ifanhao.scripts import ac_utils
    ac_utils.pull(505430)
    ac_utils.pull(505431)
    ac_utils.pull(505432)
    ac_utils.pull(505433)
    ac_utils.pull(505434)
    ac_utils.pull(505435)
    ac_utils.pull(505436)
    ac_utils.pull(505437)
    ac_utils.pull(505438)

if __name__ == '__main__':
    manager.run()
