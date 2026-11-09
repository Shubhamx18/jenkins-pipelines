# Jenkins Installation on Linux (Ubuntu/Debian)

Jenkins is a CI/CD server written in Java. After install it runs as a service and opens its web UI on **port 8080**.

## 1. Install Java

Install Java **first**. If Jenkins goes in before Java, the service fails to start.

```bash
sudo apt update
sudo apt install -y fontconfig openjdk-21-jre
java -version
```

## 2. Add the Jenkins repository

This tells `apt` where Jenkins packages live and which key to trust. We use the **LTS** (stable) line.

```bash
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] \
https://pkg.jenkins.io/debian-stable binary/" | \
sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

> Older tutorials use `jenkins.io-2023.key`. It has expired and causes a `NO_PUBKEY` error on `apt update`. Use the 2026 key above.

## 3. Install and start Jenkins

```bash
sudo apt update
sudo apt install -y jenkins
sudo systemctl enable --now jenkins
sudo systemctl status jenkins
```

You want to see `active (running)`. Press `q` to exit the status screen.

> **WSL2:** `systemctl` works only with systemd enabled. Put this in `/etc/wsl.conf`, then run `wsl --shutdown` in PowerShell and reopen WSL:
> ```
> [boot]
> systemd=true
> ```

## 4. First login

1. Open `http://localhost:8080`
2. Get the unlock password:
   ```bash
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword
   ```
3. Paste it, click **Install suggested plugins**, create your admin user.

## 5. Let Jenkins run Docker (needed to build images in pipelines)

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
sudo -u jenkins docker ps      # must work without an error
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `NO_PUBKEY` on `apt update` | You used the old 2023 key. Redo step 2 with the 2026 key. |
| "failed to find a valid Java installation" | Install Java (step 1), then `sudo systemctl restart jenkins`. |
| Page won't load | `sudo systemctl status jenkins`, then `sudo journalctl -u jenkins -e` to see the error. |
| Port 8080 already used | `sudo systemctl edit jenkins`, add `[Service]` and `Environment="JENKINS_PORT=8081"`, then restart. |
| `permission denied` for Docker in a pipeline | Step 5, then restart Jenkins. |

**Good to know:** all Jenkins data (jobs, plugins, config) is in `/var/lib/jenkins`. Back that folder up before upgrades.

*Source: [Jenkins Linux install docs](https://www.jenkins.io/doc/book/installing/linux/)*
