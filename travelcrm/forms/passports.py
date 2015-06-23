# -*-coding: utf-8 -*-

import colander

from . import(
    Date,
    ResourceSchema, 
    BaseForm,
    BaseSearchForm,
)
from ..resources.passports import PassportsResource
from ..models.passport import Passport
from ..lib.qb.passports import PassportsQueryBuilder
from ..lib.utils.common_utils import translate as _


@colander.deferred
def date_validator(node, kw):
    request = kw.get('request')

    def validator(node, value):
        if not value and request.params.get('passport_type') == 'foreign':
            raise colander.Invalid(
                node,
                _(u"You must set end date for foreign passport")
            )
    return validator


class _PassportSchema(ResourceSchema):
    country_id = colander.SchemaNode(
        colander.Integer()
    )
    passport_type = colander.SchemaNode(
        colander.String(),
    )
    num = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=2, max=24)
    )
    end_date = colander.SchemaNode(
        Date(),
        missing=None,
        validator=date_validator
    )
    descr = colander.SchemaNode(
        colander.String(),
        missing=None,
        validator=colander.Length(min=2, max=255)
    )

class PassportForm(BaseForm):
    _schema = _PassportSchema

    def submit(self, passport=None):
        context = PassportsResource(self.request)
        if not passport:
            passport = Passport(
                resource=context.create_resource()
            )
        else:
            passport.resource.notes = []
            passport.resource.tasks = []
        passport.num = self._controls.get('num')
        passport.country_id = self._controls.get('country_id')
        passport.passport_type = self._controls.get('passport_type')
        passport.end_date = self._controls.get('end_date')
        passport.descr = self._controls.get('descr')
        return passport


class PassportSearchForm(BaseSearchForm):
    _qb = PassportsQueryBuilder