# -*- coding: utf-8 -*-
from openprocurement.api.utils import opresource

from openprocurement.tender.openua.views.bid import TenderUABidResource
from openprocurement.tender.openeu.views.bid import TenderBidResource as TenderEUBidResource


@opresource(name='Tender ESCO UA Bids',
            collection_path='/tenders/{tender_id}/bids',
            path='/tenders/{tender_id}/bids/{bid_id}',
            procurementMethodType='esco.UA',
            description="Tender ESCO UA bids")
class TenderESCOUABidResource(TenderUABidResource):
    """ Tender ESCO UA Bid Resource """


@opresource(name='Tender ESCO EU Bids',
            collection_path='/tenders/{tender_id}/bids',
            path='/tenders/{tender_id}/bids/{bid_id}',
            procurementMethodType='esco.EU',
            description="Tender ESCO EU bids")
class TenderESCOEUBidResource(TenderEUBidResource):
    """ Tender ESCO EU Bid Resource """
