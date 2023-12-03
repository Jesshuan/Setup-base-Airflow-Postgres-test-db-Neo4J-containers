import os
import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.neo4j.operators.neo4j import Neo4jOperator



DAG_ID = "test_connection_neo4j_dag"



with DAG(
    dag_id=DAG_ID,
    start_date=datetime.datetime(2020, 2, 2),
    schedule_interval="@weekly",
    catchup=False,
) as dag:
    
    start_dag = BashOperator(task_id="start_dag", bash_command="echo 'Start!'")
    
    neo4j_test = Neo4jOperator(
        neo4j_conn_id="neo4j_conn_id",
        task_id="neo4j_operator_task",
        sql='Create(m:Student{Name:"Test"})'
    )

    start_dag >> neo4j_test

    

