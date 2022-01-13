import json
import pathlib

import airflow
import requests
import requests.exceptions as requests_exceptions
from airflow import DAG
from airflow.decorators import dag, task
from airflow.operators.subdag_operator import SubDagOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.example_dags.subdags.subdag import subdag

from airflow.utils import timezone
from datetime import datetime, timedelta
from hms_workflow_platform.core.services import *
from hms_workflow_platform.settings import settings

from hms_workflow_platform.core.common.utils.send_messages import SendToRabbit
from hms_workflow_platform.core.services.query.encounter_query_service import EncounterQueryService
from hms_workflow_platform.core.services.query.patient_query_service import PatientQueryService
from hms_workflow_platform.core.services.query.allergy_query_service import AllergyQueryService
from hms_workflow_platform.core.services.query.practitioner_query_service import PractitionerQueryService
from hms_workflow_platform.core.services.query.appointment_query_service import AppointmentQueryService
from hms_workflow_platform.core.services.query.billing_query_service import BillingQueryService
from hms_workflow_platform.core.services.query.payor_query_service import PayorQueryService

from hms_workflow_platform.core.services.template.encounter_template_service import EncounterTemplateService
from hms_workflow_platform.core.services.template.allergy_template_service import AllergyTemplateService
from hms_workflow_platform.core.services.template.appointment_template_service import AppointmentTemplateService
from hms_workflow_platform.core.services.template.billing_template_service import BillingTemplateService
from hms_workflow_platform.core.services.template.patient_template_service import PatientTemplateService
from hms_workflow_platform.core.services.template.payor_template_service import PayorTemplateService
from hms_workflow_platform.core.services.template.practitioner_template_service import PractitionerTemplateService



events = {
    "encounter_create": [ None, EncounterQueryService, "fetchCreated" ],
    "encounter_update": [ None, EncounterQueryService, "fetchUpdate" ],
    "encounter_discharge": [ None, EncounterQueryService, "fetchDischarge" ],
    "patient_create": [ None, PatientQueryService, "fetchCreated" ],
    "patient_update": [ None, PatientQueryService, "fetchUpdate" ],
    "patient_registration": [ None, PatientQueryService, "fetchRegistration" ],
    "payor_create": [ None, PayorQueryService, "fetchCreated" ],
    "payor_update": [ None, PayorQueryService, "fetchUpdate" ],
    "practitioner_create": [ None, PractitionerQueryService, "fetchCreated" ],
    "practitioner_update": [ None, PayorQueryService, "fetchUpdate" ],
    "allergy_create": [ None, AllergyQueryService, "fetchCreated" ],
    "appointment_create": [ None, AppointmentQueryService, "fetchCreated" ],
    "billing_create": [ None, BillingQueryService, "fetchCreated" ],
    "billing_inprogress_create": [ None, BillingQueryService, "fetchInprogressCreated" ]
}

domains = {
    "patient": [ None, PatientTemplateService ],
    "encounter": [ None, EncounterTemplateService ],
    "payor": [ None, PayorTemplateService ],
    "practitioner": [ None, PractitionerTemplateService ],
    "allergy": [ None, AllergyTemplateService ],
    "appointment": [ None, AppointmentTemplateService ],
    "billing": [ None, BillingTemplateService ],
}

#Global parameter
project_name = settings.get("site", "")
default_args = {
    'owner': 'HMS-Gateway',
    # 'start_date': airflow.utils.dates.days_ago(0, hour=0, minute=0, second=0, microsecond=0),
    # 'schedule_interval':"* * * * *",
    # 'schedule_interval':None,
}

main_dag = DAG(
        dag_id=project_name,
        default_args=default_args,
        start_date=timezone.utcnow().replace(
            second=0,
            microsecond=0),
        schedule_interval=timedelta(seconds=30),
        # schedule_interval=None,
        concurrency=20,
    )

def _generate_event(**kwargs):
    event = kwargs['event']
    date_str_yesterday = timezone.utcnow() - timedelta(hours=20)
    service = events[event][1]()
    service.prepareQuery(settings.get('data_source', ''), settings.get('site', ''))
    try:
        data_list = getattr(service, events[event][2])(yesterday=date_str_yesterday)
    except AttributeError:
        return []
    return data_list

def generateEventTasks():
    for event in events.keys():
        operator = DummyOperator(
            task_id=f'create_{event}_event',
            dag=main_dag,
        )

        process_task = PythonOperator(
            task_id=f'query_{event}',
            python_callable=_generate_event,
            op_kwargs={'event':event},
            dag=main_dag,
        )
        operator >> process_task
        events[event][0] = process_task

def _create_data_template(**kwargs):
    task_instance = kwargs['task_instance']
    ti = kwargs['ti']
    domain = kwargs['domain']
    service = domains[domain][1]()
    print(f'service:{service}')
    service.prepareTemplate(settings.get('data_source', ''))
    for event in events.keys():
        if domain == event.split('_')[0]:
            data_list = ti.xcom_pull(task_ids=f'query_{event}')
            # print(f'data_list::{data_list}')
            keys = service.generateKey(data_list)
            print(f'keys:{keys}')
            task_instance.xcom_push(key=event, value=keys)
    # return keys

def _handle_data_message_queue(**kwargs):
    send_msg = SendToRabbit()
    ti = kwargs['ti']
    domain = kwargs['domain']
    for event in events.keys():
        if domain == event.split('_')[0]:
            keys = ti.xcom_pull(task_ids=f'create_{domain}_template',key=event)
            # print(data_list)
            send_msg.send_to_rabbit(domain, keys)
    

def generateDomainTasks():
    for domain in domains.keys():
        task_create_key = PythonOperator(
            task_id=f'create_{domain}_template',
            python_callable=_create_data_template,
            op_kwargs={'domain':domain, },
            dag=main_dag,
        )
        handle_message_queue = PythonOperator(
            task_id=f'handle_{domain}_message_queue',
            python_callable=_handle_data_message_queue,
            op_kwargs={'domain':domain},
            dag=main_dag,
        )
        task_create_key >> handle_message_queue
        domains[domain][0] = task_create_key

def mapDomainsToEvents():
    for key in events.keys():
        events[key][0] >> domains[key.split('_')[0]][0]

generateEventTasks()
generateDomainTasks()
mapDomainsToEvents()
