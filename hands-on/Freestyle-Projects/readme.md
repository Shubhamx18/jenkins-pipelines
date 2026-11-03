# Jenkins Freestyle Projects Workflow

This directory contains standalone source code files and setup documentation for executing UI-configured **Freestyle Projects** in Jenkins[cite: 2].

---

## 1. Directory Structure

```text
hands-on/Freestyle Projects/
├── python-app/
│   └── app.py
├── java-app/
│   ├── HelloWorld.java
│   └── Calculator.java
└── README.md
```[cite: 2]

---

## 2. Required Plugins

Depending on your chosen execution method, ensure the following plugins are installed in Jenkins[cite: 2]:

| Plugin Name | Minimum Version | Required For | Installation Path |
| :--- | :--- | :--- | :--- |
| **Git Plugin** | Installed by Default | Repository cloning[cite: 2] | `Manage Jenkins` > `Plugins` > `Available plugins` > Search `Git`[cite: 2] |
| **Python Plugin** | Optional | **Option B** (Execute Python Script build step)[cite: 2] | `Manage Jenkins` > `Plugins` > `Available plugins` > Search `Python Plugin`[cite: 2] |

*Note: Option A (**Execute shell**) uses your system shell directly and requires no extra plugins beyond the default Git plugin[cite: 2].*

---

## 3. Automation Tasks Overview

| Job Name | Task Type | Source File Path | Execution Method |
| :--- | :--- | :--- | :--- |
| `01_python_job` | Python Script[cite: 2] | `hands-on/Freestyle Projects/python-app/app.py`[cite: 2] | Execute shell / Execute Python script[cite: 2] |
| `02_java_hello` | Java Program[cite: 2] | `hands-on/Freestyle Projects/java-app/HelloWorld.java`[cite: 2] | Execute shell / Execute Python script[cite: 2] |
| `03_java_calc` | Java Program[cite: 2] | `hands-on/Freestyle Projects/java-app/Calculator.java`[cite: 2] | Execute shell / Execute Python script[cite: 2] |

---

## 4. General Jenkins Configuration (Standard for All Jobs)

1. Navigate to your **Jenkins Dashboard** and click **New Item**[cite: 2].
2. Enter the **Item Name** (e.g., `01_python_job`) and select **Freestyle project**[cite: 2].
3. Under **Source Code Management**[cite: 2]:
   - Select **Git**[cite: 2].
   - **Repository URL**: `https://github.com/Shubhamx18/jenkins-pipelines.git`[cite: 2]
   - **Credentials**: Select your GitHub Personal Access Token[cite: 2].
   - **Branch Specifier**: `*/main`[cite: 2]

---

## 5. Execution Methods per Project

### Project 1: Python Script Execution

#### Option A: Via Execute shell (No Plugin Required)
- **Build Step**: Add build step > **Execute shell**[cite: 2]
- **Command**:
  ```bash
  python3 "hands-on/Freestyle Projects/python-app/app.py"
  ```[cite: 2]

#### Option B: Via Execute Python script *(Requires `Python Plugin`)*
- **Build Step**: Add build step > **Execute Python script**[cite: 2]
- **Script**:
  ```python
  import subprocess

  script_path = "hands-on/Freestyle Projects/python-app/app.py"
  with open(script_path) as f:
      exec(f.read())
  ```[cite: 2]

---

### Project 2: Java Hello World Execution

#### Option A: Via Execute shell (No Plugin Required)
- **Build Step**: Add build step > **Execute shell**[cite: 2]
- **Command**:
  ```bash
  cd "hands-on/Freestyle Projects/java-app"
  javac HelloWorld.java
  java HelloWorld
  ```[cite: 2]

#### Option B: Via Execute Python script *(Requires `Python Plugin`)*
- **Build Step**: Add build step > **Execute Python script**[cite: 2]
- **Script**:
  ```python
  import subprocess

  work_dir = "hands-on/Freestyle Projects/java-app"
  subprocess.run(["javac", "HelloWorld.java"], cwd=work_dir, check=True)
  subprocess.run(["java", "HelloWorld"], cwd=work_dir, check=True)
  ```[cite: 2]

---

### Project 3: Java Calculator Execution

#### Option A: Via Execute shell (No Plugin Required)
- **Build Step**: Add build step > **Execute shell**[cite: 2]
- **Command**:
  ```bash
  cd "hands-on/Freestyle Projects/java-app"
  javac Calculator.java
  java Calculator
  ```[cite: 2]

#### Option B: Via Execute Python script *(Requires `Python Plugin`)*
- **Build Step**: Add build step > **Execute Python script**[cite: 2]
- **Script**:
  ```python
  import subprocess

  work_dir = "hands-on/Freestyle Projects/java-app"
  subprocess.run(["javac", "Calculator.java"], cwd=work_dir, check=True)
  subprocess.run(["java", "Calculator"], cwd=work_dir, check=True)
  ```[cite: 2]

---

## 6. Local Pre-check Commands

Run these commands in your local terminal to verify execution before triggering a build in Jenkins[cite: 2]:

```bash
# Test Python Script (Shell)
python3 "hands-on/Freestyle Projects/python-app/app.py"

# Test Java Hello World (Shell)
cd "hands-on/Freestyle Projects/java-app"
javac HelloWorld.java
java HelloWorld

# Test Java Calculator (Shell)
javac Calculator.java
java Calculator
```[cite: 2]
