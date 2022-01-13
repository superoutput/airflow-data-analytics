import sys
import os

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base)

from datetime import datetime, timedelta
from pytz import timezone
from hms_workflow_platform.core.services.template.encounter_template_service import EncounterTemplateService
from hms_workflow_platform.core.services.template.allergy_template_service import AllergyTemplateService
from hms_workflow_platform.core.services.template.appointment_template_service import AppointmentTemplateService
from hms_workflow_platform.core.services.template.billing_template_service import BillingTemplateService
from hms_workflow_platform.core.services.template.patient_template_service import PatientTemplateService
from hms_workflow_platform.core.services.template.payor_template_service import PayorTemplateService
from hms_workflow_platform.core.services.template.practitioner_template_service import PractitionerTemplateService

from hms_workflow_platform.core.services.query.encounter_query_service import EncounterQueryService
from hms_workflow_platform.core.services.query.patient_query_service import PatientQueryService
from hms_workflow_platform.core.services.query.allergy_query_service import AllergyQueryService
from hms_workflow_platform.core.services.query.practitioner_query_service import PractitionerQueryService
from hms_workflow_platform.core.services.query.appointment_query_service import AppointmentQueryService
from hms_workflow_platform.core.services.query.billing_query_service import BillingQueryService
from hms_workflow_platform.core.services.query.payor_query_service import PayorQueryService
from core.common.utils.send_messages import SendToRabbit


def main():
    function_class = {
        "allergy_create": [AllergyQueryService, AllergyTemplateService, "fetchCreated"],
        "appointment_create": [AppointmentQueryService, AppointmentTemplateService, "fetchCreated"],
        "billing_create": [BillingQueryService, BillingTemplateService, "fetchCreated"],
        "billing_inprogress_create": [BillingQueryService, BillingTemplateService, "fetchInprogressCreated"],
        "encounter_create": [EncounterQueryService, EncounterTemplateService, "fetchCreated"],
        "encounter_update": [EncounterQueryService, EncounterTemplateService, "fetchUpdate"],
        "encounter_discharge": [EncounterQueryService, EncounterTemplateService, "fetchDischarge"],
        "patient_create": [PatientQueryService, PatientTemplateService, "fetchCreated"],
        "patient_update": [PatientQueryService, PatientTemplateService, "fetchUpdate"],
        "patient_registration": [PatientQueryService, PatientTemplateService, "fetchRegistration"],
        "payor_create": [PayorQueryService, PayorTemplateService, "fetchCreated"],
        "payor_update": [PayorQueryService, PayorTemplateService, "fetchUpdate"],
        "practitioner_create": [PractitionerQueryService, PractitionerTemplateService, "fetchCreated"],
        "practitioner_update": [PayorQueryService, PractitionerTemplateService, "fetchUpdate"],
    }
    today = datetime.now(timezone('Asia/Bangkok'))
    date_str_yesterday = today - timedelta(hours=20)
    # date_str_yesterday = today - timedelta(days=20)
    tomorrow = today + timedelta(days=1)
    service_query = function_class[sys.argv[1]][0]()

    service_query.prepareQuery('im', '')
    data_list = getattr(service_query, function_class[sys.argv[1]][2])(yesterday=date_str_yesterday)
    service_template = function_class[sys.argv[1]][1]()
    service_template.prepareTemplate('im')
    keys = service_template.generateKey(data_list)
    # print(f'keys_fetchCreated::{keys}')

    send_msg = SendToRabbit()
    send_msg.send_to_rabbit(sys.argv[1].split('_')[0], keys)

if __name__ == "__main__":
    main()
