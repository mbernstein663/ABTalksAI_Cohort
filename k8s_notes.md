# Kubernetes Minikube Demo Testing

Today we are deploying our Docker containers, testing scaling + rolling updates, and trying different Kubernetes rollout methods.

## Changing Image Tags

NAME                       READY   STATUS    RESTARTS   AGE
backend-5d6c768d4f-d4rkl   1/1     Running   0          9m55s
backend-5d6c768d4f-v246m   1/1     Running   0          10m
backend-5d6c768d4f-xth2m   1/1     Running   0          8m42s
frontend-dcf9d57f5-m84qr   1/1     Running   0          19m
backend-5d6c768d4f-xth2m   1/1     Terminating   0          9m3s
backend-5d6c768d4f-xth2m   1/1     Terminating   0          9m3s
backend-656fd749d6-xkk4r   0/1     Pending       0          0s
backend-656fd749d6-xkk4r   0/1     Pending       0          0s
backend-656fd749d6-xkk4r   0/1     ContainerCreating   0          0s
backend-656fd749d6-xkk4r   0/1     Running             0          1s
backend-5d6c768d4f-xth2m   0/1     Completed           0          9m5s
backend-5d6c768d4f-xth2m   0/1     Completed           0          9m6s
backend-5d6c768d4f-xth2m   0/1     Completed           0          9m6s
backend-5d6c768d4f-xth2m   0/1     Completed           0          9m6s

## "kubectl delete -f k8s/"

deployment.apps "backend" deleted from default namespace
service "backend" deleted from default namespace
deployment.apps "frontend" deleted from default namespace
service "frontend" deleted from default namespace

## Results

Started a local Kubernetes cluster using Minikube with Docker images. I then successfully loaded the frontend and backend. Scaling results were successful from 2->3 replicas. Rolling updates worked successfully and full pod teardown also worked successfully. 
