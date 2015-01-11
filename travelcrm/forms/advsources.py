# -*-coding: utf-8 -*-

import colander

from . import (
    ResourceSchema,
    ResourceSearchSchema
)
from ..models.advsource import Advsource
from ..lib.utils.common_utils import translate as _


@colander.deferred
def name_validator(node, kw):
    request = kw.get('request')

    def validator(node, value):
        advsource = Advsource.by_name(value)
        if (
            advsource
            and str(advsource.id) != request.params.get('id')
        ):
            raise colander.Invalid(
                node,
                _(u'Advertise source with the same name exists'),
            )
    return colander.All(colander.Length(max=32), validator,)


class AdvsourceSchema(ResourceSchema):
    name = colander.SchemaNode(
        colander.String(),
        validator=name_validator,
    )


class AdvsourceSearchSchema(ResourceSearchSchema):
    pass
