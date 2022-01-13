import uuid
import pika
from hms_workflow_platform.settings import settings
from hms_workflow_platform.core.common.utils.rabbitMQ_manager import RabbitMQ


class SendToRabbit:
    def __init__(self):
        self._type_definition = {
            "patient": {
                "domain": "Patient",
                "method": "find_patient_by_hn",
                "key": lambda data: data.split(',')[0],
                "adapter_name": "adapter_2",
                "length": 2,
            },
            "encounter": {
                "domain": "Encounter",
                "method": "find_encounter_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_2",
                "length": 50,
            },
            "allergy": {
                "domain": "AllergyIntolerance",
                "method": "find_allergy_by_hn",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_2",
                "length": 50,
            },
            "procedure": {
                "domain": "Procedure",
                "method": "find_procedure_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_2",
                "length": 50,
            },
            "diagnostic": {
                "domain": "Diagnostic",
                "method": "find_diagnosis_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_3",
                "length": 20,
            },
            "cc": {
                "domain": "CC",
                "method": "find_cc_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_3",
                "length": 50,
            },
            "pi": {
                "domain": "PI",
                "method": "find_pi_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_3",
                "length": 50,
            },
            "appointment": {
                "domain": "Appointment",
                "method": "find_appointment_by_hn",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_3",
                "length": 1,
            },
            "medicalhistory": {
                "domain": "MedicalHistory",
                "method": "find_medicalhistory_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_3",
                "length": 50,
            },
            "vitalsigns": {
                "domain": "VitalSign",
                "method": "find_vitalsign_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_4",
                "length": 50,
            },
            "lab": {
                "domain": "Laboratory",
                "method": "find_laboratory_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_4",
                "length": 10,
            },
            "lab_trak": {
                "domain": "Labtrak",
                "method": "find_labtrak_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_4",
                "length": 1,
            },
            "radiology": {
                "domain": "Radiology",
                "method": "find_radiology_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_4",
                "length": 50,
            },
            "physicalexam": {
                "domain": "PhysicalExam",
                "method": "find_physicalexam_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_4",
                "length": 50,
            },
            "medicationdispense": {
                "domain": "MedicationDispense",
                "method": "find_medication_dispense_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_3",
                "length": 10,
            },
            "patientimage": {
                "domain": "PatientImage",
                "method": "find_patient_image_by_hn",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_1",
                "length": 1,
            },
            "request": {
                "domain": "Request",
                "method": "find_request_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_1",
                "length": 10,
            },
            "claim": {
                "domain": "Claim",
                "method": "find_claim_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_1",
                "length": 10,
            },
            "billing": {
                "domain": "Billing",
                "method": "find_billing_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_1",
                "length": 10,
            },
            "triage": {
                "domain": "Triage",
                "method": "find_triage_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_2",
                "length": 10,
            },
            "careplan": {
                "domain": "CarePlan",
                "method": "find_care_plan_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_4",
                "length": 10,
            },
            "servicerequest": {
                "domain": "ServiceRequest",
                "method": "find_service_request_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_4",
                "length": 10,
            },
            "coverage": {
                "domain": "Coverage",
                "method": "find_coverage_by_en",
                "key": (lambda data: data.split(',')[0]),
                "adapter_name": "adapter_4",
                "length": 10,
            },
            "billing_inprogress": {
                "domain": "Billing",
                "method": "find_unbilled_by_en",
                "key": lambda data: data.split(',')[0],
                "adapter_name": "adapter_2",
                "length": 10,
            }
        }
        self._data_template_msg = {
                "payload": None,
                "req_id": None,
                "trigger_start": None,
                "trigger_end": None,
                "trigger_duration": None,
                "trigger_raw_size": None,
                "redis_duration": None,
                "query_duration": None,
                "offset": None,
                "page_size": None,
                "total": None,
                "mq_persist_time": None,
                "his_source": None
            }
        self._log_template_msg = {
            "env": None,
            "site": None,
            "req_id": None,
            "timestamp": None,
            "micro_service_name": "HMS-DELTAHUB",
            "source_service": "HMS-DELTAHUB",
            "source_ip": None,
            "destination_service": "HMS-PARSER",
            "event_name": "call_parser",
            "library_type": "hms_parser_tracker",
            "parent_event": "call_hms-deltahub",
            "promise": "ASYNC",
            "state": "REQUEST",
            "channel": "OUTBOUND",
            "level": "DEBUG"
        }
        self._env = settings.get("env", "DEV")
        self._site = settings.get("site", "Local")
        self._rmq = RabbitMQ(settings.get('rabbitmq_settings'), auto_connect=False)

    def send_to_rabbit(self, domain, data_list):
        new_value = list(set(map(self._type_definition[domain]['key'], data_list)))
        total = len(new_value)
        req_id = str(uuid.uuid1())
        self._data_template_msg['total'] = total
        queue_name = f"{self._site}.{domain}.{self._env}"
        # queue_name = f"{self._site}.TEST_SEND.{self._env}"
        round = 0
        try:
            print("data to send:: ", new_value)
            self._rmq.connect()
            self._rmq.queue_declare(queue_name)
            domain_detail = self._type_definition[domain]

            while new_value and len(new_value) > 0:
                round = round+1
                value_list = new_value[0:domain_detail['length']]
                del new_value[0:domain_detail['length']]
                payload = f"{domain_detail['domain']} {domain_detail['method']} {domain_detail['adapter_name']} {' '.join(value_list)}"
                self._data_template_msg['payload'] = payload
                self._data_template_msg['req_id'] = f'{req_id}-{str(round).zfill(4)}'
                self._data_template_msg['page_size'] = len(value_list)
                self._log_template_msg['env'] = self._env
                self._log_template_msg['site'] = self._site
                self._log_template_msg['req_id'] = f'{req_id}-{str(round).zfill(4)}'
                data = {"data": self._data_template_msg, "log": self._log_template_msg}
                self._rmq.publish_data(data, queue_name)
        except pika.exceptions.ConnectionClosedByBroker:
            print(f"ERROR: ConnectionClosedByBroker")
        except pika.exceptions.AMQPChannelError:
            print(f"ERROR: AMQPChannelError")
        except pika.exceptions.AMQPConnectionError:
            print(f"ERROR: AMQPConnectionError")
        except Exception as e:
            print(e)
