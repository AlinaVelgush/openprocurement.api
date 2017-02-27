# -*- coding: utf-8 -*-
from openprocurement.api.utils import (
    get_now
)
from openprocurement.tender.core.utils import (
    optendersresource
)
from openprocurement.tender.belowthreshold.views.question import TenderQuestionResource


@optendersresource(name='Tender UA Questions',
                   collection_path='/tenders/{tender_id}/questions',
                   path='/tenders/{tender_id}/questions/{question_id}',
                   procurementMethodType='aboveThresholdUA',
                   description="Tender questions")
class TenderUaQuestionResource(TenderQuestionResource):

    def validate_question(self, operation):
        tender = self.request.validated['tender']
        now = get_now()
        if operation == 'add' and (now < tender.enquiryPeriod.startDate or now > tender.enquiryPeriod.endDate):
            self.request.errors.add('body', 'data', 'Can add question only in enquiryPeriod')
            self.request.errors.status = 403
            return
        if operation == 'update' and tender.status != 'active.tendering':
            self.request.errors.add('body', 'data', 'Can\'t update question in current ({}) tender status'.format(tender.status))
            self.request.errors.status = 403
            return
        question = self.request.validated['question']
        items_dict = {i.id: i.relatedLot for i in tender.items}
        if any([
            i.status != 'active'
            for i in tender.lots
            if question.questionOf == 'lot' and i.id == question.relatedItem or question.questionOf == 'item' and i.id == items_dict[question.relatedItem]
        ]):
            self.request.errors.add('body', 'data', 'Can {} question only in active lot status'.format(operation))
            self.request.errors.status = 403
            return
        if operation == 'update' and now > tender.enquiryPeriod.clarificationsUntil:
            self.request.errors.add('body', 'data', 'Can update question only before enquiryPeriod.clarificationsUntil')
            self.request.errors.status = 403
            return
        return True
