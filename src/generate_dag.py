import os
from typing import Literal

from common import rand_id

dir_path = os.path.dirname(os.path.realpath(__file__))

from string import Template
from textwrap import dedent


COUNT = 10
DAG_TYPE: Literal["U", "R", "S"] = "R"


def generate_dag(seed):
    dag_id = rand_id(seed)

    if DAG_TYPE != "U":
        dag_id += f"_{DAG_TYPE.lower()}"

    with open(get_dag_path(dag_id), "w+") as f:
        f.write(
            get_dag_template().substitute(
                seed=seed,
                dag_id=dag_id,
                dag_type=DAG_TYPE,
            )
        )


def get_dag_path(dag_id):
    return os.path.join(dir_path, "../dags/", f"{dag_id}.py")


def get_dag_template():
    return Template(
        dedent(
            """    from datetime import datetime
    from airflow.models import DAG
    from task_generator import generate_task

    seed = ${seed}
    dag_type = "${dag_type}"

    dag = DAG(
        dag_id="${dag_id}",
        schedule="@once",
        start_date=datetime(2024, 8, 1),
    )

    generate_task(seed, dag, dag_type)
    """
        )
    )


for i in range(0, COUNT):
    generate_dag(i)
