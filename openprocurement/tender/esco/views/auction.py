# -*- coding: utf-8 -*-
from openprocurement.api.utils import opresource
from openprocurement.tender.openua.views.auction import TenderUaAuctionResource
from openprocurement.tender.openeu.views.auction import TenderAuctionResource as TenderEUAuctionResource


@opresource(name='Tender ESCO UA Auction',
            collection_path='/tenders/{tender_id}/auction',
            path='/tenders/{tender_id}/auction/{auction_lot_id}',
            procurementMethodType='esco.UA',
            description="Tender ESCO UA Auction data")
class TenderESCOUAAuctionResource(TenderUaAuctionResource):
    """ Tender ESCO UA Auction Resource """


@opresource(name='Tender ESCO EU Auction',
            collection_path='/tenders/{tender_id}/auction',
            path='/tenders/{tender_id}/auction/{auction_lot_id}',
            procurementMethodType='esco.EU',
            description="Tender ESCO EU Auction data")
class TenderESCOEUAuctionResource(TenderEUAuctionResource):
    """ Tender ESCO EU Auction Resource """
