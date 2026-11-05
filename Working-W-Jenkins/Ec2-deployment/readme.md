# Production-Grade Flask App CI/CD Pipeline (Jenkins + Kind on AWS)

An automated, two-tier AWS EC2 architecture for building, containerizing, pushing, and deploying a Python Flask application to a Kubernetes (Kind) cluster using Jenkins.

---

## 1. System Architecture

```text
  +-------------------------------------+             +---------------------------------------+
  |  EC2 Instance #1: Controller        |             |  EC2 Instance #2: Worker              |
  |  - Jenkins Master (Port 8080)       |             |  - Jenkins SSH Agent                  |
  |  - SCM Poller                       |-- SSH (22)->|  - Docker Engine                      |
  |  - Pipeline Orchestrator            |             |  - Kind K8s Cluster (Control-Plane)   |
  +-------------------------------------+             +---------------------------------------+
                     ^                                                    |
                     | Polls                                              v
           +-------------------+                              +-----------------------+
           | GitHub Repository |                              | Docker Hub Registry   |
           +-------------------+                              +-----------------------+
```

---

## 2. Infrastructure & Prerequisites

### EC2 Master (Controller Node)
* **OS:** Ubuntu 22.04 LTS / 24.04 LTS
* **Inbound Rules:** TCP `8080` (Jenkins Web UI), TCP `22` (SSH Access)
* **Required Packages:** `openjdk-17-jre`, `jenkins`

### EC2 Worker (Build Node)
* **OS:** Ubuntu 22.04 LTS / 24.04 LTS
* **Inbound Rules:** TCP `22` (From Controller Private IP)
* **Required Packages:** `docker.io`, `kubectl`, `kind`

---

## 3. Worker Node Pre-flight Setup

Run on **EC2 Instance #2 (Worker)**:

```bash
# Add user to Docker group
sudo usermod -aG docker ubuntu && newgrp docker

# Initialize Kind Cluster
kind create cluster --name my-cluster --wait 60s

# Verify Cluster and Context
kubectl cluster-info --context kind-my-cluster
kubectl get nodes
```

---

## 4. Required Jenkins Plugins

Navigate to **Manage Jenkins** -> **Plugins** -> **Available plugins** and install:

| Plugin Name | Purpose |
| :--- | :--- |
| **SSH Build Agents** | Enables Controller-to-Worker execution over SSH |
| **Git** | SCM integration for GitHub repository pulling |
| **Docker Pipeline** | Native DSL support for container builds |
| **Credentials Binding** | Secret management for registry authentication |

---

## 5. Security & Credentials Setup

Navigate to **Manage Jenkins** -> **Credentials** -> **System** -> **Global credentials (unrestricted)** -> **Add Credentials**.

### A. Docker Hub Authentication
* **Kind:** Username with password
* **Scope:** Global
* **ID:** `dockerhub-creds`
* **Username:** `<your-dockerhub-username>`
* **Password:** `<your-dockerhub-access-token>`

### B. Worker Node SSH Authentication
* **Kind:** SSH Username with private key
* **Scope:** Global
* **ID:** `ec2-ssh`
* **Username:** `ubuntu`
* **Private Key:** Select *Enter directly* and paste your EC2 `.pem` key content.

---

## 6. Worker Node Registration

Navigate to **Manage Jenkins** -> **Nodes** -> **New Node**:

1. **Node Name:** `ec2-worker`
2. **Type:** Permanent Agent
3. **Remote Root Directory:** `/home/ubuntu/jenkins`
4. **Labels:** `ec2-worker`
5. **Launch Method:** Launch agents via SSH
   * **Host:** `<WORKER_EC2_PRIVATE_OR_PUBLIC_IP>`
   * **Credentials:** `ec2-ssh`
   * **Host Key Verification Strategy:** Non verifying Verification Strategy
6. Click **Save**, then click **Launch Agent**. Ensure the agent log outputs `Agent successfully connected and online`.

---

## 7. Jenkins Pipeline Job Setup

Navigate to **Jenkins Dashboard** -> **New Item**:

1. **Item Name:** `flask-kind-pipeline`
2. **Project Type:** Pipeline
3. **Build Triggers:** Check **Poll SCM** -> Schedule: `* * * * *` (Polls every minute)
4. **Pipeline Definition:** Pipeline script from SCM
   * **SCM:** Git
   * **Repository URL:** `https://github.com/Shubhamx18/jenkins-pipelines.git`
   * **Branches to analyze:** `*/main`
   * **Script Path:** `Working-W-Jenkins/Ec2-deployment/Jenkinsfile`
5. Click **Save** and trigger **Build Now**.
