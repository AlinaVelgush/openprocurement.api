# -*- coding: utf-8 -*-
from openprocurement.api.roles import RolesFromCsv
from schematics.exceptions import ValidationError
from schematics.types.compound import ModelType
from schematics.types import StringType
from openprocurement.tender.core.models import ContractValue
from openprocurement.api.utils import get_now
from openprocurement.api.models import Model, ListType, Contract as BaseContract, Document


class Contract(BaseContract):
    class Options:
        roles = RolesFromCsv("Contract.csv", relative_to=__file__)

    value = ModelType(ContractValue)
    awardID = StringType(required=True)
    documents = ListType(ModelType(Document, required=True), default=list())

    def validate_awardID(self, data, awardID):
        parent = data["__parent__"]
        if awardID and isinstance(parent, Model) and awardID not in [i.id for i in parent.awards]:
            raise ValidationError(u"awardID should be one of awards")

    def validate_dateSigned(self, data, value):
        parent = data["__parent__"]
        if value and isinstance(parent, Model) and value > get_now():
            raise ValidationError(u"Contract signature date can't be in the future")
