# Workshop Setup & Troubleshooting Guide

Everything you need to verify your environment is ready for the workshop — and fix it if it isn't.

---

## Quick Verification Checklist

Run each command below. If any step fails, jump to [Common Problems](#common-problems).

### 1. Verify Linux

```bash
uname -a
lsb_release -a
```

You should see a Linux kernel version and an Ubuntu (or similar) release.

### 2. Verify Git

```bash
git --version
```

Expected output (version may differ):

```
git version 2.25.1
```

### 3. Verify Docker

```bash
docker --version
```

Expected output (version may differ):

```
Docker version 20.10.17, build 100c701
```

### 4. Verify Docker Compose

```bash
docker compose version
```

Expected output (version may differ):

```
Docker Compose version v2.6.0
```

> **Note:** The modern Docker CLI uses `docker compose` (with a space). The older standalone binary was `docker-compose` (with a hyphen). Both work, but `docker compose` is the recommended form.

### 5. Verify Docker Daemon

```bash
docker info
```

If this prints system-wide information about Docker (storage driver, number of containers, etc.), the daemon is running.

### 6. Test Docker Container Execution

```bash
docker run --rm hello-world
```

You should see a message starting with:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

### 7. Verify Python

```bash
python3 --version
pip3 --version
```

You need Python 3.9 or above.

### 8. Verify GitHub SSH Access

```bash
ssh -T git@github.com
```

Expected output:

```
Hi <your-username>! You've successfully authenticated, but GitHub does not provide shell access.
```

---

## Automated Check

Instead of running each command manually, use the verification script:

```bash
chmod +x scripts/check_setup.sh
./scripts/check_setup.sh
```

It checks every prerequisite and prints a clear **[OK]** / **[FAIL]** report.

---

## Common Problems

### Docker: permission denied

**Symptom:**

```
Got permission denied while trying to connect to the Docker daemon socket
```

**Fix:**

```bash
sudo usermod -aG docker $USER
newgrp docker
```

Then log out and log back in (or reboot) for the group change to take full effect.

### Docker daemon not running

**Symptom:**

```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

**Fix:**

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### `docker-compose` command not found

**Symptom:**

```
docker-compose: command not found
```

**Fix:** Modern Docker installations include Compose as a plugin. Use:

```bash
docker compose up -d
```

instead of:

```bash
docker-compose up -d
```

If neither works, install the Compose plugin:

```bash
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

### Port already in use

**Symptom:**

```
Error starting userland proxy: listen tcp4 0.0.0.0:8000: bind: address already in use
```

**Fix:** Find and stop whatever is using the port:

```bash
# Check port 8000 (Python service)
sudo lsof -i :8000

# Check port 5434 (PostgreSQL service)
sudo lsof -i :5434
```

Then stop the conflicting process, or change the port mapping in `docker-compose.yaml`.

### Container name already in use

**Symptom:**

```
The container name "/workshop_python_container" is already in use
```

**Fix:**

```bash
# List all containers (including stopped ones)
docker ps -a

# Remove the old container
docker rm workshop_python_container

# Or remove it forcefully if it's still running
docker rm -f workshop_python_container
```

### Cannot access GitHub over SSH

**Symptom:**

```
ssh: connect to host github.com port 22: Connection refused
```

or

```
Permission denied (publickey).
```

**Fix:**

1. Check if you have an SSH key:

   ```bash
   ls -la ~/.ssh/
   ```

2. If no key exists, generate one:

   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

3. Start the SSH agent and add your key:

   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```

4. Copy the public key and add it to your [GitHub SSH settings](https://github.com/settings/keys):

   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

5. Test the connection:

   ```bash
   ssh -T git@github.com
   ```

### Python version too old / pip3 missing

**Symptom:**

```
python3: command not found
```

or Python version is below 3.9.

**Fix:**

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

To check your version:

```bash
python3 --version
```

---

## Useful Docker Commands Reference

A quick reference for commands used during the workshop.

| Command | Description |
|---------|-------------|
| `docker images` | List all local images |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers (including stopped) |
| `docker pull <image>` | Download an image from Docker Hub |
| `docker build ./ -t <name>` | Build an image from a Dockerfile |
| `docker run -ti <image>` | Run an image interactively |
| `docker exec -it <container> sh` | Open a shell inside a running container |
| `docker stop <container>` | Stop a running container |
| `docker rm <container>` | Remove a stopped container |
| `docker rmi <image>` | Remove an image |
| `docker compose up -d` | Start services defined in docker-compose.yaml |
| `docker compose down` | Stop and remove services |
| `docker compose logs` | View service logs |

---

## Still stuck?

If none of the above fixes your issue, try these steps:

1. **Restart Docker:**

   ```bash
   sudo systemctl restart docker
   ```

2. **Reboot your machine** — some group/permission changes only take effect after a full reboot.

3. **Re-run the install script:**

   ```bash
   sudo prerequisites/install_docker.sh
   ```

4. **Open an issue** on the [workshop repository](https://github.com/UniCourt/DataEngineering-Workshop1/issues) describing your problem and the output of:

   ```bash
   uname -a
   docker --version
   docker compose version
   python3 --version
   ```
