from airflow.models.baseoperator import BaseOperator
from airflow.providers.neo4j.hooks.neo4j import Neo4jHook


import time

from datetime import datetime

import copy

import pandas as pd

# --- Batch function ---

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


# --- CLASS ---


class DeleteNeo4jGraphOperator(BaseOperator):

    def __init__(
            self,
            neo4j_conn_uri= "postgres_default",
            **kwargs
        ) -> None:

        super().__init__(**kwargs)
        self.neo4j_conn_uri: str = neo4j_conn_uri


    def execute(self, context):

        neo4j_hook = Neo4jHook(self.neo4j_conn_uri)

        driver = neo4j_hook.get_conn()

        with driver.session() as session:
            result = session.write_transaction(delete_all)
            count = result[0]['COUNT']
            print(f'Numbers of deleted nodes : {count}')







            

