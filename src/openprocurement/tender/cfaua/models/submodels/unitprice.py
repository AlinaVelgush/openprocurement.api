# -*- coding: utf-8 -*-
from decimal import Decimal
from schematics.exceptions import ValidationError
from schematics.types import FloatType, StringType
from schematics.types.compound import ModelType
from openprocurement.api.models import Model, DecimalType
from openprocurement.tender.cfaua.models.submodels.value import Value as BaseValue


class Value(BaseValue):

    amount = DecimalType(precision=-2, min_value=Decimal("0.0"))

    def validate_amount(self, data, amount):
        pass


class UnitPrice(Model):
    relatedItem = StringType()
    value = ModelType(Value)

    def validate_relatedItem(self, data, relatedItem):
        pass
