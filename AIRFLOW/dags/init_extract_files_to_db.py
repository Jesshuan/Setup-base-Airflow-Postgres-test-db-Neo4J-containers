import os
import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator



DAG_ID = "init_extract_files_to_db_dag"


with DAG(
    dag_id=DAG_ID,
    start_date=datetime.datetime(2020, 2, 2),
    schedule_interval="@weekly",
    catchup=False,
) as dag:
    
    start_dag = BashOperator(task_id="start_dag", bash_command="echo 'Start!'")
    


    start_dag
    

