import json
from concurrent.futures import ThreadPoolExecutor

import requests

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Basic YWlyZmxvdzphaXJmbG93",
}
session = requests.session()
session.headers.update(headers)

base_url = "http://localhost:8080/api/v1"


def run_all():
    dags = list_all_dag()
    all_dag_id = list(map(lambda d: d["dag_id"], dags["dags"]))

    for dag_id in all_dag_id:
        delete_all_dag_run_of_dag(dag_id)

    with ThreadPoolExecutor(max_workers=100) as tp:
        for result in tp.map(unpause_dag, all_dag_id):
            assert result["is_paused"] == False


def stop_all():
    dags = list_all_dag()
    all_dag_id = list(map(lambda d: d["dag_id"], dags["dags"]))

    with ThreadPoolExecutor(max_workers=100) as tp:
        for result in tp.map(pause_dag, all_dag_id):
            assert result["is_paused"] == True


def unpause_dag(dag_id: str):
    return toggle_pause_dag(dag_id, False)


def pause_dag(dag_id: str):
    return toggle_pause_dag(dag_id, True)


def toggle_pause_dag(dag_id: str, is_paused: bool):
    resp = session.patch(
        url=base_url + "/dags/" + dag_id,
        data=json.dumps(
            {
                "is_paused": is_paused,
            }
        ),
    )
    resp.raise_for_status()

    return resp.json()


def delete_all_dag_run_of_dag(dag_id: str):
    resp = session.get(
        url=base_url + "/dags/" + dag_id + "/dagRuns",
    )
    resp.raise_for_status()

    dagruns = resp.json()

    for dagrun in dagruns["dag_runs"]:
        delete_dag_run(dag_id, dagrun["dag_run_id"])


def delete_dag_run(dag_id, dag_run_id):
    resp = session.delete(
        url=base_url + "/dags/" + dag_id + "/dagRuns/" + dag_run_id,
        data=json.dumps({}),
    )
    resp.raise_for_status()


def list_all_dag():
    endpoint = "/dags"

    resp = session.get(
        url=base_url + endpoint,
    )
    resp.raise_for_status()

    return resp.json()


__all__ = ["run_all"]
