# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#
# @author: Five
# Created on 2013-8-28
#

import unittest
from ifanhao_tests import BasicTestCase


class Test(BasicTestCase):


    def test_many2many(self):

        with self.app.test_request_context():
            from ifanhao.models import Av, Tag
            av = Av.query.first()
            print av.tags
            print av

            tag = Tag.query.first()
            print tag
            print tag.avs
            print tag.avs[0].title



if __name__ == "__main__":
    unittest.main()
