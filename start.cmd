docker build -t dion-ricky/airflow-stress-test .

gcloud auth configure-docker us-central1-docker.pkg.dev
docker tag dion-ricky/airflow-stress-test us-central1-docker.pkg.dev/dionricky-personal/airflow/airflow-stress-test

gcloud container clusters create-auto airflow-cluster --region us-central1
kubectl create namespace airflow
@REM kubectl apply -f helm/airflow-dags-pvc.yaml
helm install --namespace airflow -f helm/values.yaml airflow apache-airflow/airflow
@REM helm upgrade airflow apache-airflow/airflow --namespace airflow -f helm/values.yaml
kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow

airflow users create \
    --username airflow \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password airflow