import os
import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.neo4j.operators.neo4j import Neo4jOperator
from custom_operators.delete_neo4j_graph_operators import DeleteNeo4jGraphOperator

DAG_ID = "delete_all_neo4j_graph_dag"

with DAG(
    dag_id=DAG_ID,
    start_date=datetime.datetime(2020, 2, 2),
    schedule_interval="@weekly",
    catchup=False,
) as dag:
    
    neo4j_delete = DeleteNeo4jGraphOperator(task_id='delete_all_graph', 
                                          neo4j_conn_uri="neo4j_local")



    

