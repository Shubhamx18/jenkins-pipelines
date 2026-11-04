# Jenkins Pipeline Setup

## Prerequisites
* Jenkins 2.x+
* Plugins: `Pipeline`, `Git`, `Docker`

---

## Setup Steps

### Option 1: Direct Script
1. **New Item** $\rightarrow$ Select **Pipeline** $\rightarrow$ **OK**
2. **Pipeline** section $\rightarrow$ Select **Pipeline script**
3. Paste code $\rightarrow$ **Save**

### Option 2: From SCM (Jenkinsfile)
1. **New Item** $\rightarrow$ Select **Pipeline** $\rightarrow$ **OK**
2. **Pipeline** section $\rightarrow$ Select **Pipeline script from SCM**
3. **SCM**: Select `Git`
4. **Repository URL**: `https://github.com/Shubhamx18/jenkins-pipelines.git`
5. **Script Path**: `Working-W-Jenkins/DockerJenkins/Jenkinsfile`
6. **Save**

---

## Run Pipeline
Click **Build Now** $\rightarrow$ Check **Console Output**
