# -*-coding: utf-8-*-

import colander
import phonenumbers
from colander import (
    Date as ColanderDate,
    Invalid,
    null,
    _
)
from babel.dates import parse_date

from ..lib.utils.common_utils import get_locale_name


class ResourceSchema(colander.Schema):
    status = colander.SchemaNode(
        colander.Integer(),
    )


class Date(ColanderDate):

    def deserialize(self, node, cstruct):
        if not cstruct:
            return null
        try:
            result = parse_date(cstruct, locale=get_locale_name())
        except:
            raise Invalid(
                node,
                _(
                    self.err_template,
                    mapping={'val': cstruct}
                )
            )
        return result


class PhoneNumber(object):

    def __call__(self, node, value):
        try:
            phone = phonenumbers.parse(value)
        except phonenumbers.NumberParseException:
            raise Invalid(
                node,
                _(
                    u"Phone must be in format +XXXXXXXXXXX "
                    u"and contains country code",
                    mapping={'val': value}
                )
            )
        if not phonenumbers.is_valid_number(phone):
            raise Invalid(
                node,
                _(
                    u"Phone is not valid",
                    mapping={'val': value}
                )
            )
