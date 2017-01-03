# -*- coding: utf-8 -*-
from openprocurement.tender.openua.views.contract import TenderUaAwardContractResource as TenderUaContractResource
from openprocurement.tender.openeu.views.contract import TenderAwardContractResource as TenderEUContractResource
from openprocurement.tender.limited.views.contract import TenderAwardContractResource as TenderReportingContractResource
from openprocurement.api.utils import opresource


@opresource(name='Tender ESCO UA Contracts',
            collection_path='/tenders/{tender_id}/contracts',
            path='/tenders/{tender_id}/contracts/{contract_id}',
            procurementMethodType='esco.UA',
            description="Tender ESCO UA contracts")
class TenderESCOUAContractResource(TenderUaContractResource):
    """ Tender ESCO UA Contract Resource """


@opresource(name='Tender ESCO EU Contracts',
            collection_path='/tenders/{tender_id}/contracts',
            path='/tenders/{tender_id}/contracts/{contract_id}',
            procurementMethodType='esco.EU',
            description="Tender ESCO EU contracts")
class TenderESCOEUContractResource(TenderEUContractResource):
    """ Tender ESCO EU Contract Resource """


@opresource(name='Tender ESCO Reporting Contracts',
            collection_path='/tenders/{tender_id}/contracts',
            path='/tenders/{tender_id}/contracts/{contract_id}',
            procurementMethodType='esco.reporting',
            description="Tender ESCO Reporting contracts")
class TenderESCOReportingContractResource(TenderReportingContractResource):
    """ Tender ESCO Reporting Contract Resource """
