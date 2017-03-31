# -*- coding: utf-8 -*-
from openprocurement.api.utils import (
    json_view,
    context_unpack,
    get_now,
)
from openprocurement.tender.core.utils import (
    optendersresource,
    save_tender
)
from openprocurement.tender.core.validation import (
    validate_lot_data,
    validate_tender_period_extension,
    validate_lot_operation_not_in_allowed_status
)

from openprocurement.tender.openua.views.lot import (
    TenderUaLotResource as TenderLotResource
)


@optendersresource(name='aboveThresholdEU:Tender Lots',
                   collection_path='/tenders/{tender_id}/lots',
                   path='/tenders/{tender_id}/lots/{lot_id}',
                   procurementMethodType='aboveThresholdEU',
                   description="Tender EU lots")
class TenderEULotResource(TenderLotResource):

    @json_view(content_type="application/json", validators=(validate_lot_data, validate_lot_operation_not_in_allowed_status, validate_tender_period_extension), permission='edit_tender')
    def collection_post(self):
        """Add a lot
        """
        lot = self.request.validated['lot']
        lot.date = get_now()
        tender = self.request.validated['tender']
        tender.lots.append(lot)
        if self.request.authenticated_role == 'tender_owner':
            tender.invalidate_bids_data()
        if save_tender(self.request):
            self.LOGGER.info('Created tender lot {}'.format(lot.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'tender_lot_create'}, {'lot_id': lot.id}))
            self.request.response.status = 201
            self.request.response.headers['Location'] = self.request.route_url('{}:Tender Lots'.format(tender.procurementMethodType), tender_id=tender.id, lot_id=lot.id)
            return {'data': lot.serialize("view")}
