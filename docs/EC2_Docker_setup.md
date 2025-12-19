
## EC2 / Docker Setup

### Project Deployment

**GitHub Workflow:**
- Code changes: Push from local → Pull on EC2
- Secrets (keys, config.py): Copy via scp (never committed to git)

**Clone to EC2:**
```bash
cd ~
git clone https://github.com/<your-username>/regional-hospital-capacity-planning.git
cd regional-hospital-capacity-planning
```

**Create gitignored folders and copy secrets:**
```bash
# On EC2
mkdir keys

# From local machine
scp -i <your-key.pem> ./keys/snowflake_key.p8 ubuntu@<ec2-ip>:~/regional-hospital-capacity-planning/keys/
scp -i <your-key.pem> ./airflow/src/config.py ubuntu@<ec2-ip>:~/regional-hospital-capacity-planning/airflow/src/
```

### Docker / Airflow

**Fix logs permissions (required before first run):**
```bash
sudo chown -R 50000:0 airflow/logs
```

**Start containers:**
```bash
docker-compose up -d
```

**Verify:**
```bash
docker ps  # All containers should show (healthy)
```

**Access Airflow UI:**
- SSH with tunnel: `ssh -i <key.pem> -L 8080:localhost:8080 ubuntu@<ec2-ip>`
- Open: `http://localhost:8080`
- Credentials: airflow / airflow

**Useful commands:**
```bash
docker-compose down          # Stop all containers
docker-compose up -d         # Start all containers
docker logs <container_name> # View container logs
docker ps -a                 # View all containers (including stopped)
```