# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-22
#

class BaseModelMixin():

    def fromdict(self, _dict):
        """ Merge in items in the dict into our object
            if it's one of our columns
        """
        for c in self.__table__.columns:
            if c.name in _dict:
                setattr(self, c.name, _dict[c.name])
