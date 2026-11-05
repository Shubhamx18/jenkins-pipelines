# End-to-End Flask Application CI/CD Pipeline via Jenkins & Kind Kubernetes

This project demonstrates an automated CI/CD pipeline built using **Jenkins**, **Docker**, and **Kubernetes (Kind)** on a native Ubuntu host (`PG-ITISS23`). The pipeline automatically pulls code, builds a Docker image, pushes it to Docker Hub, and deploys the application to a local Kind Kubernetes cluster.

---

## 🏗 Architecture & Overview

* **Host Environment:** Native Ubuntu Installation (`PG-ITISS23`)
* **CI/CD Automation:** Declarative Jenkins Pipeline
* **Containerization:** Docker (`shubhamm18/jenkins-k8s`)
* **Orchestration:** Local Kind Cluster (`kind-my-cluster` listening on `127.0.0.1:36401`)
* **Kubernetes Target Namespace:** `myspace`

---

## 🚀 Setup & Prerequisites

### 1. Host Authentication for Jenkins User
Since Jenkins runs under its own system user (`jenkins`), it requires explicit read access to the local Kubernetes cluster configuration and client certificates. Run the following commands on your Ubuntu host:

```bash
# Create dedicated .kube directory for Jenkins user
sudo mkdir -p /var/lib/jenkins/.kube

# Copy active root cluster configuration
sudo cp /root/.kube/config /var/lib/jenkins/.kube/config

# Assign ownership to the jenkins service user
sudo chown -R jenkins:jenkins /var/lib/jenkins/.kube
sudo chmod 600 /var/lib/jenkins/.kube/config
```

> **Note:** These steps resolve `permission denied` and `Couldn't get current server API group list` errors by granting the `jenkins` user direct authorization to communicate with `127.0.0.1:36401`.

### 2. Jenkins Credentials
Configure the following credential in Jenkins (**Manage Jenkins** > **Credentials**):
* **ID:** `dockerhub-creds`
* **Type:** Username with password (Docker Hub credentials)

---

## 📁 Repository Structure

```text
Working-W-Jenkins/Docker-Kubernetes-Jenkins/
├── Dockerfile              # Flask application container specification
├── deployment.yml          # Kubernetes Deployment & NodePort Service manifests
├── app.py                  # Main Flask application logic
└── README.md               # Project documentation
```

---

## 📄 Declarative Jenkinsfile Pipeline

The pipeline uses standard multi-line shell blocks and handles authentication seamlessly:

```groovy
pipeline {
    agent any

    triggers {
        pollSCM("H/5 * * * *")
    }

    environment {
        MY_LOGIN   = credentials("dockerhub-creds")
        IMAGE_NAME = "shubhamm18/jenkins-k8s"
    }

    stages {
        stage("code checkout") {
            steps {
                git branch: "main",
                    url: "https://github.com/Shubhamx18/jenkins-pipelines.git"
            }
        }

        stage("docker build to go !") {
            steps {
                dir("Working-W-Jenkins/Docker-Kubernetes-Jenkins") {
                    sh "docker build -t $IMAGE_NAME:latest ."
                }
            }
        }

        stage("docker login !") {
            steps {
                sh "echo $MY_LOGIN_PSW | docker login -u $MY_LOGIN_USR --password-stdin"
            }
        }

        stage("docker push now !") {
            steps {
                sh "docker push $IMAGE_NAME:latest"
            }
        }

        stage("applying k8s manifests !!") {
            steps {
                sh '''
                    kubectl apply --validate=false -f Working-W-Jenkins/Docker-Kubernetes-Jenkins/deployment.yml -n myspace
                    kubectl get all -n myspace
                '''
            }
        }

        stage("done !") {
            steps {
                sh 'echo "pipeline runs successfully !!"'
            }
        }
    }
}
```

---

## 🛠 Manifest Configuration (`deployment.yml`)

Ensure your deployment manifest uses current API versions compatible with Kubernetes v1.30+:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
  namespace: myspace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-app
        image: shubhamm18/jenkins-k8s:latest
        ports:
        - containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: flask-service
  namespace: myspace
spec:
  type: NodePort
  selector:
    app: flask-app
  ports:
    - port: 5000
      targetPort: 5000
      nodePort: 30050
```

---

## 🔍 Verification

Once the pipeline completes, verify the deployment directly from your host:

```bash
kubectl get all -n myspace
```

Expected Output:
```text
NAME                             READY   STATUS    RESTARTS   AGE
pod/flask-app-7d489f5596-sttp8   1/1     Running   0          2m

NAME                    TYPE       CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE
service/flask-service   NodePort   10.96.58.80   <none>        5000:30050/TCP   2m
```