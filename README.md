# Airflow Stress Test in GKE
Stress testing Airflow with long running task, CPU heavy task, and memory heavy task.

## Setup
### 1. Create DAGs
Use generate_dag.py

### 2. Mount DAGs to PVC
If PVC not exists yet, create it using script in start.cmd

### 3. Run all
Use run_all.py to run all DAGs at once.

## Clean up
- Delete all containers in GKE
- Delete cluster
- Make sure disks are also deleted