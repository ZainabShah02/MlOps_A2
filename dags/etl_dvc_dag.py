from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from extract import extract_data
from transform import transform_data
from load import load_data

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 12, 15),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_dvc_dag',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)

extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load_data,
    dag=dag,
)

extract_task >> transform_task >> load_task
