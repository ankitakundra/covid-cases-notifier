from datetime import datetime,timedelta
from helper import find_no_of_cases
from helper import create_email_content
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),

}
dag = DAG(
    dag_id='coronavirus_cases_notifier',
    default_args=default_args,
    start_date = datetime(2020,9,27),
    schedule_interval='00 03 * * *'
)
task_1 = PythonOperator(
    task_id = "scrape_coronavirus_cases",
    python_callable = find_no_of_cases,
    dag = dag
)

task_2 = PythonOperator(
    task_id = "create_email_content",
    python_callable = create_email_content,
    provide_context = True,
    dag = dag
)
task_3 = EmailOperator(
    task_id='send_email',
    to='ankita.rkl12@gmail.com',
    subject='Coronavirus Cases - India',
    html_content="{{ task_instance.xcom_pull(task_ids='create_email_content', key='email_content') }}",
    dag=dag
)

task_1 >> task_2 >> task_3
