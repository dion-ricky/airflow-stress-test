from time import sleep

import numpy as np
from airflow.models.baseoperator import BaseOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

from common import rand_id, rand_num


def generate_task(seed, dag, dag_type):
    mapper = {
        "U": generate_union_task,
    }
    return mapper.get(
        dag_type,
        generate_splitted_task,
    )(seed, dag, dag_type)


def generate_union_task(seed, dag, **kwargs):
    base_task = generate_base_task(seed, dag)
    empty_task1 = generate_empty_task(seed, dag, "1")
    empty_task2 = generate_empty_task(seed, dag, "2")
    waiting_task = generate_waiting_task(seed, dag)
    empty_task3 = generate_empty_task(seed, dag, "3")

    base_task >> empty_task1 >> empty_task2 >> waiting_task >> empty_task3


def generate_splitted_task(seed, dag, dag_type):
    mapper = {
        "R": generate_splitted_task_r,
        "S": generate_splitted_task_s,
    }
    return mapper[dag_type](seed, dag)


def generate_splitted_task_r(seed, dag):
    base_task = generate_base_task(seed, dag)
    empty_task1 = generate_empty_task(seed, dag, "1")
    empty_task2 = generate_empty_task(seed, dag, "2")

    (base_task >> empty_task1 >> empty_task2)


def generate_splitted_task_s(seed, dag):
    sensor_task = generate_sensor_task(seed, dag)
    waiting_task = generate_waiting_task(seed, dag)
    empty_task3 = generate_empty_task(seed, dag, "3")

    sensor_task >> waiting_task >> empty_task3


def generate_base_task(seed, dag):
    base_task: BaseOperator

    if seed % 2 == 0:
        base_task = generate_cpu_task(seed, dag)
    else:
        base_task = generate_mem_task(seed, dag)

    return base_task


def generate_cpu_task(seed, dag) -> BaseOperator:
    return PythonOperator(
        task_id=rand_id(seed) + "_b",
        python_callable=fib,
        op_args=(rand_num(seed, 35, 45),),
        dag=dag,
    )


def generate_mem_task(seed, dag) -> BaseOperator:
    return PythonOperator(
        task_id=rand_id(seed) + "_m",
        python_callable=use_lots_of_memory,
        op_args=(rand_num(seed, 150000, 750000),),
        dag=dag,
    )


def generate_waiting_task(seed, dag) -> BaseOperator:
    return PythonOperator(
        task_id=rand_id(seed) + "_s",
        python_callable=wait,
        op_args=(rand_num(seed, 5, 45),),
        dag=dag,
    )


def generate_sensor_task(seed, dag) -> BaseOperator:
    return ExternalTaskSensor(
        task_id=rand_id(seed) + "_sr",
        external_dag_id=rand_id(seed) + "_r",
        external_task_id=rand_id(seed) + "_e2",
        allowed_states=["success"],
        dag=dag,
    )


def generate_empty_task(seed, dag, suffix="") -> BaseOperator:
    return EmptyOperator(
        task_id=rand_id(seed) + "_e" + suffix,
        dag=dag,
    )


def wait(seconds):
    sleep(seconds)


def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


def use_lots_of_memory(size_in_mb):
    num_elements = int((size_in_mb / 1000) * (1024**3) / 8)
    large_array = np.ones(num_elements, dtype=np.float64)
    return large_array
