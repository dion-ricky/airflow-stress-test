FROM apache/airflow:2.10.0

COPY src /opt/airflow/src
COPY dags /opt/airflow/dags