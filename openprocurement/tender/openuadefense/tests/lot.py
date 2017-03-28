# -*- coding: utf-8 -*-
import unittest
from openprocurement.tender.belowthreshold.tests.base import test_lots
from openprocurement.api.tests.base import snitch
from openprocurement.tender.openuadefense.tests.base import BaseTenderUAContentWebTest
from openprocurement.tender.openua.tests.base import test_bids
from openprocurement.tender.openuadefense.tests.lot_blanks import (
    create_tender_lot_invalid,
    create_tender_lot,
    patch_tender_lot,
    patch_tender_currency,
    patch_tender_vat,
    get_tender_lot,
    get_tender_lots,
    delete_tender_lot,
    question_blocking,
    claim_blocking,
    next_check_value_with_unanswered_question,
    next_check_value_with_unanswered_claim,
    tender_value,
    tender_features_invalid,
    create_tender_bidder_invalid,
    patch_tender_bidder,
    create_tender_bidder_with_features_invalid,
    create_tender_bidder_with_features,
    one_lot_0bid,
    one_lot_1bid,
    one_lot_1bid_patch,
    one_lot_2bid,
    one_lot_3bid_1un,
    two_lot_0bid,
    two_lot_2can,
    two_lot_1bid_0com_1can,
    two_lot_1bid_2com_1win,
    two_lot_1bid_0com_0win,
    two_lot_1bid_1com_1win,
    two_lot_2bid_on_first_and_1_on_second_awarding,
    two_lot_2bid_2com_2win,
)


class TenderLotResourceTest(BaseTenderUAContentWebTest):

    test_create_tender_lot_invalid = snitch(create_tender_lot_invalid)

    test_create_tender_lot = snitch(create_tender_lot)

    test_patch_tender_lot = snitch(patch_tender_lot)

    test_patch_tender_currency = snitch(patch_tender_currency)

    test_patch_tender_vat = snitch(patch_tender_vat)

    test_get_tender_lot = snitch(get_tender_lot)

    test_get_tender_lots = snitch(get_tender_lots)

    test_delete_tender_lot = snitch(delete_tender_lot)


class TenderLotEdgeCasesTest(BaseTenderUAContentWebTest):
    initial_lots = test_lots * 2
    initial_bids = test_bids

    test_question_blocking = snitch(question_blocking)

    test_claim_blocking = snitch(claim_blocking)

    test_next_check_value_with_unanswered_question = snitch(next_check_value_with_unanswered_question)

    test_next_check_value_with_unanswered_claim = snitch(next_check_value_with_unanswered_claim)


class TenderLotFeatureResourceTest(BaseTenderUAContentWebTest):
    initial_lots = 2 * test_lots

    test_tender_value = snitch(tender_value)

    test_tender_features_invalid = snitch(tender_features_invalid)


class TenderLotBidderResourceTest(BaseTenderUAContentWebTest):
    # initial_status = 'active.tendering'
    initial_lots = test_lots

    test_create_tender_bidder_invalid = snitch(create_tender_bidder_invalid)

    test_patch_tender_bidder = snitch(patch_tender_bidder)


class TenderLotFeatureBidderResourceTest(BaseTenderUAContentWebTest):
    initial_lots = test_lots

    def setUp(self):
        super(TenderLotFeatureBidderResourceTest, self).setUp()
        self.lot_id = self.initial_lots[0]['id']
        response = self.app.patch_json('/tenders/{}'.format(self.tender_id), {"data": {
            "items": [
                {
                    'relatedLot': self.lot_id,
                    'id': '1'
                }
            ],
            "features": [
                {
                    "code": "code_item",
                    "featureOf": "item",
                    "relatedItem": "1",
                    "title": u"item feature",
                    "enum": [
                        {
                            "value": 0.01,
                            "title": u"good"
                        },
                        {
                            "value": 0.02,
                            "title": u"best"
                        }
                    ]
                },
                {
                    "code": "code_lot",
                    "featureOf": "lot",
                    "relatedItem": self.lot_id,
                    "title": u"lot feature",
                    "enum": [
                        {
                            "value": 0.01,
                            "title": u"good"
                        },
                        {
                            "value": 0.02,
                            "title": u"best"
                        }
                    ]
                },
                {
                    "code": "code_tenderer",
                    "featureOf": "tenderer",
                    "title": u"tenderer feature",
                    "enum": [
                        {
                            "value": 0.01,
                            "title": u"good"
                        },
                        {
                            "value": 0.02,
                            "title": u"best"
                        }
                    ]
                }
            ]
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['items'][0]['relatedLot'], self.lot_id)

    test_create_tender_bidder_invalid = snitch(create_tender_bidder_with_features_invalid)

    test_create_tender_bidder = snitch(create_tender_bidder_with_features)


class TenderLotProcessTest(BaseTenderUAContentWebTest):
    setUp = BaseTenderUAContentWebTest.setUp

    test_1lot_0bid = snitch(one_lot_0bid)

    test_1lot_1bid = snitch(one_lot_1bid)

    test_1lot_1bid_patch = snitch(one_lot_1bid_patch)

    test_1lot_2bid = snitch(one_lot_2bid)

    test_1lot_3bid_1un = snitch(one_lot_3bid_1un)

    test_2lot_0bid = snitch(two_lot_0bid)

    test_2lot_2can = snitch(two_lot_2can)

    test_2lot_1bid_0com_1can = snitch(two_lot_1bid_0com_1can)

    test_2lot_1bid_2com_1win = snitch(two_lot_1bid_2com_1win)

    test_2lot_1bid_0com_0win = snitch(two_lot_1bid_0com_0win)

    test_2lot_1bid_1com_1win = snitch(two_lot_1bid_1com_1win)

    test_2lot_2bid_on_first_and_1_on_second_awarding = snitch(two_lot_2bid_on_first_and_1_on_second_awarding)

    test_2lot_2bid_2com_2win = snitch(two_lot_2bid_2com_2win)


# def suite():
#     suite = unittest.TestSuite()
#     suite.addTest(unittest.makeSuite(TenderLotResourceTest))
#     suite.addTest(unittest.makeSuite(TenderLotBidderResourceTest))
#     suite.addTest(unittest.makeSuite(TenderLotFeatureBidderResourceTest))
#     suite.addTest(unittest.makeSuite(TenderLotProcessTest))
#     return suite


# if __name__ == '__main__':
#     unittest.main(defaultTest='suite')
