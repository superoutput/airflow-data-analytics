import sys
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from airflow.utils import timezone
from datetime import datetime, timedelta

from google.cloud.language_v1.types import Document
from airflow.contrib.operators.gcp_natural_language_operator import *

main_dag = DAG(
        dag_id='GCP',
        start_date=timezone.utcnow().replace(
            second=0,
            microsecond=0),
        schedule_interval=timedelta(seconds=180),
        concurrency=20,
    )

TEXT = """Airflow is a platform to programmatically author, schedule and monitor workflows.

Use Airflow to author workflows as Directed Acyclic Graphs (DAGs) of tasks. The Airflow scheduler executes
 your tasks on an array of workers while following the specified dependencies. Rich command line utilities
 make performing complex surgeries on DAGs a snap. The rich user interface makes it easy to visualize
 pipelines running in production, monitor progress, and troubleshoot issues when needed.
"""
document = Document(content=TEXT, type="PLAIN_TEXT")

analyze_entities = CloudNaturalLanguageAnalyzeEntitiesOperator(
    document=document,
    task_id="analyze_entities",
    dag=main_dag,
)

analyze_entities_result = BashOperator(
    bash_command=f"echo {analyze_entities.output}",
    task_id="analyze_entities_result",
    dag=main_dag,
)
analyze_entities >> analyze_entities_result

analyze_entity_sentiment = CloudNaturalLanguageAnalyzeEntitySentimentOperator(
    document=document,
    task_id="analyze_entity_sentiment",
    dag=main_dag,
)

analyze_entity_sentiment_result = BashOperator(
    bash_command=f"echo {analyze_entity_sentiment.output}",
    task_id="analyze_entity_sentiment_result",
    dag=main_dag,
)
analyze_entity_sentiment >> analyze_entity_sentiment_result

analyze_sentiment = CloudNaturalLanguageAnalyzeSentimentOperator(
    document=document,
    task_id="analyze_sentiment",
    dag=main_dag,
)

analyze_sentiment_result = BashOperator(
    bash_command=f"echo {analyze_sentiment.output}",
    task_id="analyze_sentiment_result",
    dag=main_dag,
)
analyze_sentiment >> analyze_sentiment_result

analyze_classify_text = CloudNaturalLanguageClassifyTextOperator(
    document=document,
    task_id="analyze_classify_text",
    dag=main_dag,
)

analyze_classify_text_result = BashOperator(
    bash_command=f"echo {analyze_classify_text.output}",
    task_id="analyze_classify_text_result",
    dag=main_dag,
)
analyze_classify_text >> analyze_classify_text_result

def _log():
    print(sys.path)

log = PythonOperator(
    task_id="log",
    python_callable=_log,
    dag=main_dag,
)
