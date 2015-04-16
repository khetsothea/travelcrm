# -*-coding: utf-8 -*-
from zope.interface import implementer

from ..interfaces import (
    IResourceType,
)
from ..resources import (
    ResourceTypeBase,
)
from ..lib.utils.common_utils import translate as _


@implementer(IResourceType)
class CompanyResource(ResourceTypeBase):

    __name__ = 'company'

    @property
    def allowed_permisions(self):
        return [
            ('view', _(u'view')),
            ('edit', _(u'edit')),
        ]