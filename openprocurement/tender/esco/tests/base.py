# -*- coding: utf-8 -*-
import os
from copy import deepcopy
from datetime import datetime, timedelta
from openprocurement.api.models import get_now, SANDBOX_MODE
from openprocurement.api.tests.base import (
    BaseTenderWebTest, BaseWebTest, now
)

from openprocurement.api.utils import apply_data_patch
from openprocurement.api.tests.base import test_organization as base_test_organization
from openprocurement.tender.openua.tests.base import test_bids as base_test_bids
from openprocurement.tender.openua.tests.base import test_tender_data as base_ua_test_data
from openprocurement.tender.openeu.models import (
    TENDERING_DURATION as TENDERING_DURATION_EU,
    QUESTIONS_STAND_STILL as QUESTIONS_STAND_STILL_EU,
    COMPLAINT_STAND_STILL as COMPLAINT_STAND_STILL_EU
)
from openprocurement.tender.openeu.tests.base import test_tender_data as base_eu_test_data
from openprocurement.tender.limited.tests.base import test_tender_data as base_reporting_test_data


test_tender_ua_data = deepcopy(base_ua_test_data)
test_tender_ua_data['procurementMethodType'] = "esco.UA"

test_tender_eu_data = deepcopy(base_eu_test_data)
test_tender_eu_data['procurementMethodType'] = "esco.EU"

test_tender_reporting_data = deepcopy(base_reporting_test_data)
test_tender_reporting_data['procurementMethodType'] = "esco.reporting"

test_bids = deepcopy(base_test_bids)
test_organization = deepcopy(base_test_organization)




class BaseESCOWebTest(BaseWebTest):
    relative_to = os.path.dirname(__file__)
    initial_data = None
    initial_status = None
    initial_bids = None
    initial_lots = None
    initial_auth = ('Basic', ('broker', ''))
    docservice = None

    def setUp(self):
        super(BaseESCOWebTest, self).setUp()
        self.app.authorization = self.initial_auth
        self.couchdb_server = self.app.app.registry.couchdb_server
        self.db = self.app.app.registry.db
        if self.docservice:
            self.setUpDS()

    def tearDown(self):
        if self.docservice:
            self.tearDownDS()
        del self.couchdb_server[self.db.name]



class BaseESCOContentWebTest(BaseESCOWebTest):
    """ ESCO Content Test """
    initialize_initial_data = True

    def setUp(self):
        super(BaseESCOContentWebTest, self).setUp()
        if self.initial_data and self.initialize_initial_data:
            self.create_tender()

    def create_tender(self):
        cur_auth = self.app.authorization
        self.app.authorization = self.initial_auth

        data = deepcopy(self.initial_data)
        if self.initial_lots:
            lots = []
            for i in self.initial_lots:
                lot = deepcopy(i)
                lot['id'] = uuid4().hex
                lots.append(lot)
            data['lots'] = self.initial_lots = lots
            for i, item in enumerate(data['items']):
                item['relatedLot'] = lots[i % len(lots)]['id']
        response = self.app.post_json('/tenders', {'data': data})
        tender = response.json['data']
        self.tender_token = response.json['access']['token']
        self.tender_id = tender['id']
        status = tender['status']
        if self.initial_bids:
            self.initial_bids_tokens = {}
            response = self.set_status('active.tendering')
            status = response.json['data']['status']
            bids = []
            for i in self.initial_bids:
                if self.initial_lots:
                    i = i.copy()
                    value = i.pop('value')
                    i['lotValues'] = [
                        {
                            'value': value,
                            'relatedLot': l['id'],
                        }
                        for l in self.initial_lots
                    ]
                response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), {'data': i})
                self.assertEqual(response.status, '201 Created')
                bids.append(response.json['data'])
                self.initial_bids_tokens[response.json['data']['id']] = response.json['access']['token']
            self.initial_bids = bids
        if self.initial_status != status:
            self.set_status(self.initial_status)

        self.app.authorization = cur_auth


class BaseESCOUAContentWebTest(BaseESCOContentWebTest):
    """ ESCO UA Content Test """

    initial_data = test_tender_ua_data

    def set_status(self, status, extra=None):
        data = {'status': status}

        if status == 'active.tendering':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now).isoformat(),
                    "endDate": (now + timedelta(days=13)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now).isoformat(),
                    "endDate": (now + timedelta(days=16)).isoformat()
                }
            })
        elif status == 'active.auction':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=16)).isoformat(),
                    "endDate": (now - timedelta(days=3)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=16)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'active.qualification':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=17)).isoformat(),
                    "endDate": (now - timedelta(days=4)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=17)).isoformat(),
                    "endDate": (now - timedelta(days=1)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=1)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=1)).isoformat(),
                                "endDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'active.awarded':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=17)).isoformat(),
                    "endDate": (now - timedelta(days=4)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=17)).isoformat(),
                    "endDate": (now - timedelta(days=1)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=1)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now).isoformat(),
                    "endDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=1)).isoformat(),
                                "endDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'complete':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=25)).isoformat(),
                    "endDate": (now - timedelta(days=11)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=25)).isoformat(),
                    "endDate": (now - timedelta(days=8)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=8)).isoformat(),
                    "endDate": (now - timedelta(days=7)).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now - timedelta(days=7)).isoformat(),
                    "endDate": (now - timedelta(days=7)).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=8)).isoformat(),
                                "endDate": (now - timedelta(days=7)).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        if extra:
            data.update(extra)

        tender = self.db.get(self.tender_id)
        tender.update(apply_data_patch(tender, data))
        self.db.save(tender)

        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.get('/tenders/{}'.format(self.tender_id))
        self.app.authorization = authorization
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        return response


    def go_to_enquiryPeriod_end(self):
        now = get_now()
        self.set_status('active.tendering', {
            "enquiryPeriod": {
                "startDate": (now - timedelta(days=13)).isoformat(),
                "endDate": (now - (timedelta(minutes=1) if SANDBOX_MODE else timedelta(days=1))).isoformat()
            },
            "tenderPeriod": {
                "startDate": (now - timedelta(days=13)).isoformat(),
                "endDate": (now + (timedelta(minutes=2) if SANDBOX_MODE else timedelta(days=2))).isoformat()
            },
            "auctionPeriod": {
                "startDate": (now + timedelta(days=2)).isoformat()
            }
        })

class BaseESCOEUContentWebTest(BaseESCOContentWebTest):
    """ ESCO EU Content Test """

    initial_data = test_tender_eu_data

    def set_status(self, status, extra=None):
        data = {'status': status}
        if status == 'active.tendering':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - timedelta(days=1)).isoformat(),
                    "endDate": (now + TENDERING_DURATION_EU - QUESTIONS_STAND_STILL_EU).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - timedelta(days=1)).isoformat(),
                    "endDate": (now + TENDERING_DURATION_EU).isoformat()
                }
            })
        elif status == 'active.pre-qualification':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - TENDERING_DURATION_EU - timedelta(days=1)).isoformat(),
                    "endDate": (now - QUESTIONS_STAND_STILL_EU).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - TENDERING_DURATION_EU - timedelta(days=1)).isoformat(),
                    "endDate": (now).isoformat(),
                },
                "qualificationPeriod": {
                    "startDate": (now).isoformat(),
                }
            })
        elif status == 'active.pre-qualification.stand-still':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - TENDERING_DURATION_EU - timedelta(days=1)).isoformat(),
                    "endDate": (now - QUESTIONS_STAND_STILL_EU).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - TENDERING_DURATION_EU - timedelta(days=1)).isoformat(),
                    "endDate": (now).isoformat(),
                },
                "qualificationPeriod": {
                    "startDate": (now).isoformat(),
                },
                "auctionPeriod": {
                    "startDate": (now + COMPLAINT_STAND_STILL_EU).isoformat()
                }
            })
        elif status == 'active.auction':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - TENDERING_DURATION_EU - COMPLAINT_STAND_STILL_EU - timedelta(days=1)).isoformat(),
                    "endDate": (now - COMPLAINT_STAND_STILL_EU - TENDERING_DURATION_EU + QUESTIONS_STAND_STILL_EU).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - TENDERING_DURATION_EU - COMPLAINT_STAND_STILL_EU - timedelta(days=1)).isoformat(),
                    "endDate": (now - COMPLAINT_STAND_STILL_EU).isoformat()
                },
                "qualificationPeriod": {
                    "startDate": (now - COMPLAINT_STAND_STILL_EU).isoformat(),
                    "endDate": (now).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'active.qualification':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - TENDERING_DURATION_EU - COMPLAINT_STAND_STILL_EU - timedelta(days=2)).isoformat(),
                    "endDate": (now - QUESTIONS_STAND_STILL_EU - COMPLAINT_STAND_STILL_EU - timedelta(days=1)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - TENDERING_DURATION_EU - COMPLAINT_STAND_STILL_EU - timedelta(days=2)).isoformat(),
                    "endDate": (now - COMPLAINT_STAND_STILL_EU - timedelta(days=1)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=1)).isoformat(),
                    "endDate": (now).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=1)).isoformat(),
                                "endDate": (now).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'active.awarded':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - TENDERING_DURATION_EU - COMPLAINT_STAND_STILL_EU - timedelta(days=3)).isoformat(),
                    "endDate": (now - QUESTIONS_STAND_STILL_EU - COMPLAINT_STAND_STILL_EU - timedelta(days=2)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - TENDERING_DURATION_EU - COMPLAINT_STAND_STILL_EU - timedelta(days=3)).isoformat(),
                    "endDate": (now - COMPLAINT_STAND_STILL_EU - timedelta(days=2)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=2)).isoformat(),
                    "endDate": (now - timedelta(days=1)).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now - timedelta(days=1)).isoformat(),
                    "endDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=2)).isoformat(),
                                "endDate": (now - timedelta(days=1)).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        elif status == 'complete':
            data.update({
                "enquiryPeriod": {
                    "startDate": (now - TENDERING_DURATION_EU - COMPLAINT_STAND_STILL_EU - timedelta(days=4)).isoformat(),
                    "endDate": (now - QUESTIONS_STAND_STILL_EU - COMPLAINT_STAND_STILL_EU - timedelta(days=3)).isoformat()
                },
                "tenderPeriod": {
                    "startDate": (now - TENDERING_DURATION_EU - COMPLAINT_STAND_STILL_EU - timedelta(days=4)).isoformat(),
                    "endDate": (now - COMPLAINT_STAND_STILL_EU - timedelta(days=3)).isoformat()
                },
                "auctionPeriod": {
                    "startDate": (now - timedelta(days=3)).isoformat(),
                    "endDate": (now - timedelta(days=2)).isoformat()
                },
                "awardPeriod": {
                    "startDate": (now - timedelta(days=1)).isoformat(),
                    "endDate": (now).isoformat()
                }
            })
            if self.initial_lots:
                data.update({
                    'lots': [
                        {
                            "auctionPeriod": {
                                "startDate": (now - timedelta(days=3)).isoformat(),
                                "endDate": (now - timedelta(days=2)).isoformat()
                            }
                        }
                        for i in self.initial_lots
                    ]
                })
        if extra:
            data.update(extra)

        tender = self.db.get(self.tender_id)
        tender.update(apply_data_patch(tender, data))
        self.db.save(tender)

        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('chronograph', ''))
        #response = self.app.patch_json('/tenders/{}'.format(self.tender_id), {'data': {'id': self.tender_id}})
        response = self.app.get('/tenders/{}'.format(self.tender_id))
        self.app.authorization = authorization
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        return response


class BaseESCOReportingContentWebTest(BaseESCOContentWebTest):
    """ ESCO Reporting Content Test """

    initial_data = test_tender_reporting_data
