"""
@References
https://blog.quiltdata.com/repeatable-nlp-of-news-headlines-using-apache-airflow-newspaper3k-quilt-t4-vega-a0447af57032
https://github.com/robnewman/etl-airflow-s3/blob/master/dags/headlines.py
"""

import airflow
from airflow import DAG
# from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from airflow.utils import timezone
from datetime import datetime, timedelta

# Helpers
from time import time
import json

# Newspaper3k
import newspaper
from newspaper import Article

default_args = {
    'owner': 'superoutput',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email': ['superoutput@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'provide_context':True
}

dag = DAG(
    'headlines',
    default_args=default_args,
    schedule_interval=timedelta(days=1)
)


def scrape_articles(**kwargs):
    sources = kwargs['source_urls']
    category = kwargs['category']
    sources_keywords = dict() # Placeholder for results
    for s in sources:
        paper = newspaper.build(
            s,
            memoize_articles=False # Don't cache articles
        )
        keywords_list = list()
        for article in paper.articles:
            if category in article.url:
                single_article = Article(article.url)
                single_article.download()
                count = 0
                while single_article.download_state != 2:
                    # ArticleDownloadState.SUCCESS is 2 
                    count = count+1
                    time.sleep(count)
                single_article.parse()
                single_article.nlp()
                keywords_list.extend(single_article.keywords)
        if len(keywords_list) == 0:
            keywords_list.append("Error: No keywords")
        sources_keywords[s] = keywords_list
    return sources_keywords

task1 = PythonOperator(
    task_id='scrape_articles',
    python_callable=scrape_articles,
    op_kwargs={
        'source_urls': [
            'https://theguardian.com',
            'https://nytimes.com',
            'https://cnn.com'
        ],
        'category': 'politics'
    },
    dag=dag
)

def write_to_json(**context):
    data_directory = context['directory']
    file_name = context['filename']
    keywords = context['task_instance'].xcom_pull(task_ids='scrape_articles')
    file_names = list()
    for k in keywords:
        # Strip leading 'https://' and trailing '.com'
        domain = k.replace("https://","")
        domain = domain.replace(".com", "")
        new_fname = f"{data_directory}/{domain}_{file_name}"
        file_names.append(new_fname)
        with open(new_fname, 'w') as f:
            json.dump(
                keywords[k],
                f,
                ensure_ascii=False,
                indent=2,
                sort_keys=True
            )
    return file_names

task2 = PythonOperator(
    task_id='write_to_json',
    python_callable=write_to_json,
    op_kwargs={
        'directory': 'data',
        'filename': 'keywords.json'
    },
    dag=dag
)

def add_to_package(**context):
    datafiles = context['task_instance'].xcom_pull(task_ids='write_to_json')
    p = t4.Package()
    # Add datafiles
    for df in datafiles:
        p = p.set(
            df,
            f"{os.getcwd()}/{df}",
            meta=f"Add source file from {datetime.today().strftime('%Y-%m-%d')}"
        )
    # Add summary
    p.set(
        "quilt_summarize.json",
        "quilt_summarize.json",
        meta="Add summarize file"
    )
    # Add description
    p.set(
        "description.md",
        "description.md",
        meta="Project outline"
    )
    # Add visualizations
    p.set_dir(
        "src/visualization/vega_specs/",
        "src/visualization/vega_specs/"
    )
    # Build package
    tophash = p.build("superoutput/sentiment-analysis-headlines")
    # Push package
    # s3://hms-s3-dev-01/headlines/
    # https://hms-s3-dev-01.s3.ap-southeast-1.amazonaws.com/headlines/
    p.push(
        "superoutput/sentiment-analysis-headlines",
        dest="s3://hms-s3-dev-01/headlines/",
        message=f"Source data from {datetime.today().strftime('%Y-%m-%d')}"
    )
    return True

task3 = PythonOperator(
    task_id='add_to_package',
    python_callable=add_to_package,
    dag=dag
)

# Set dependencies
task1 >> task2 >> task3
