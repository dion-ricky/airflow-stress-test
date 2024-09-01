gcloud container clusters create-auto airflow-cluster --region us-central1
kubectl create namespace airflow
kubectl apply -f helm/airflow-dags-pvc.yaml
helm install --namespace airflow -f helm/values.yaml airflow apache-airflow/airflow
@REM helm upgrade airflow apache-airflow/airflow --namespace airflow -f helm/values.yaml
@REM kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow