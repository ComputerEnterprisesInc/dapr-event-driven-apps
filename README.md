# Dapr Event Driven Apps

![](https://docs.dapr.io/images/pubsub-overview-publish-API.png)

## Prerequisites
1. Install Dapr CLI locally
2. Docker - to build containers
3. Setup a running Kubernetes Cluster (AKS, Minikube or whatever)
4. Redis - Running locally (for development purpose)

## Demo - Getting Started

### Local Development

* Install the pip requirements in each project
  
* Make sure the dapr redis state and pubsub is configured with your redis instance credentials. For simplicity, I've run redis without password. You can configure redis with password and configure in dapr component.yaml (using secret stores). 
  
* Run the below command in root directory
   ```bash
   ./run-all.sh
   ```
   or
   ```
   dapr run -d ./components --app-id detection --app-port 5001 -- python detection/app.py
   dapr run -d ./components --app-id recognition --app-port 5002 -- python recognition/app.py 
   dapr run -d ./components --app-id http-api --app-port 5000 -- python http-api/app.py
   ```
  
* Trigger the workflow from 
   ```
   curl http://localhost:5000/trigger
   ```

* See the output
    ```
    http-api [2021-12-06 19:14:00 +0000] [6] [INFO] Triggering detection
    http-api [2021-12-06 19:14:00 +0000] [6] [INFO] Publishing into detect topic: {'data': 'some data'}
    detection [2021-12-06 19:14:00 +0000] [6] [INFO] Detecting default
    recognition [2021-12-06 19:14:00 +0000] [6] [INFO] recognizing default
    detection [2021-12-06 19:14:00 +0000] [6] [INFO] Publishing into recognize topic: {'result': 'default'}
    ```

### Kubernetes

* Install Dapr in Kubernetes
  ```
  dapr init -k
  ```
* Install KEDA in kubernetes
  ```
  kubectl apply -f https://github.com/kedacore/keda/releases/download/v2.4.0/keda-2.4.0.yaml
  ```
* Install all our applications. (push it to registry and update the url deploy/app/kustomization.yaml)  
  ```
  kubectl apply -k deploy/app
  ```
* Get the ingress endpoint and trigger
  ```
  curl https://<ingressip or lb name>/trigger
  ```
* Check the logs from pods
  ```
    http-api-79fdf68945-67jnf http-api [2021-12-06 19:14:00 +0000] [6] [INFO] Publishing into detect topic: {'data': 'some data'}
    recognition-6485f9b969-8lns7 recognition [2021-12-06 19:14:00 +0000] [6] [INFO] recognizing default
    detection-f5ddd568f-wscqj detection [2021-12-06 19:14:00 +0000] [6] [INFO] Detecting default
    detection-f5ddd568f-wscqj detection [2021-12-06 19:14:00 +0000] [6] [INFO] Publishing into recognize topic: {'result': 'default'}
    recognition-6485f9b969-8lns7 recognition [2021-12-06 19:14:00 +0000] [6] [INFO] recognizing default
  ``` 
 ### KEDA Autoscaling
 * Apply the KEDA scaled objects
   ```
   kubectl apply -f deploy/app/keda/keda.yaml
   ```
 * Check the hpa
   ```
   kubectl get hpa
   ```   
 * Set the load test on the ingress endpoint
   ```
   hey -z 15m -c 1000 https://<ingressip or lb>/trigger
   ```
 * Check whether scaling up when it runs and down once you stop
   ```
    -➜  dapr-event-driven-apps git:(main) ✗  k get hpa -w
    NAME                                REFERENCE                TARGETS     MINPODS   MAXPODS   REPLICAS   AGE
    keda-hpa-detection-scaledobject     Deployment/detection     0/2 (avg)   1         10        10         43m
    keda-hpa-recognition-scaledobject   Deployment/recognition   0/2 (avg)   1         10        2          43m
    keda-hpa-detection-scaledobject     Deployment/detection     0/2 (avg)   1         10        10         46m
    keda-hpa-detection-scaledobject     Deployment/detection     0/2 (avg)   1         10        4          46m
    keda-hpa-recognition-scaledobject   Deployment/recognition   0/2 (avg)   1         10        2          46m
    keda-hpa-detection-scaledobject     Deployment/detection     0/2 (avg)   1         10        2          46m
    keda-hpa-recognition-scaledobject   Deployment/recognition   0/2 (avg)   1         10        1          46m
    keda-hpa-detection-scaledobject     Deployment/detection     0/2 (avg)   1         10        1          47m
    keda-hpa-recognition-scaledobject   Deployment/recognition   0/2 (avg)   1         10        1          47m
    ```
## References
* [Dapr](https://dapr.io/)
* [KEDA](https://keda.sh)
