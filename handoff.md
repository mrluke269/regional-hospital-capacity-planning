# Project Handoff Report: Regional Hospital Capacity Planning

**Date:** December 18, 2025  
**Project Root:** `regional-hospital-capacity-planning`  
**GitHub:** [[your-repo-url](https://github.com/mrluke269/regional-hospital-capacity-planning)]

---

## Project Goal

Build a demand sensing pipeline that correlates external disease signals (ED visits) with hospital capacity data to predict capacity crunches 14 days in advance.

---

## Phase Structure

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Foundation & Data Exploration | ✅ Complete |
| 2 | Data Ingestion Pipeline | 🟡 Next |
| 3 | Data Modeling & Transformation (dbt) | Not Started |
| 4 | Orchestration (Airflow) | Not Started |
| 5 | Visualization (Power BI) | Not Started |
| 6 | Predictive Analytics (Stretch) | Not Started |

---

## Phase 1 Completed

### Infrastructure

| Component | Details | Status |
|-----------|---------|--------|
| AWS S3 | `hospital-planning-raw-luke` (us-east-2) | ✅ |
| AWS EC2 | Ubuntu, Docker installed | ✅ |
| IAM Role | `snowflake_read_s3` updated for new bucket | ✅ |
| Snowflake Storage Integration | `snowflake_s3` pointing to new bucket | ✅ |
| Snowflake Stage | `HOSPITAL_PLANNING_STAGE` in RAW.HOSPITAL_PLANNING | ✅ |
| Docker/Airflow | Running on EC2, accessible at localhost:8080 | ✅ |
| Git/GitHub | Repo created and synced | ✅ |

### Folder Structure
```
regional-hospital-capacity-planning/
├── README.md
├── requirements.txt
├── .gitignore
├── Dockerfile
├── docker-compose.yaml
├── keys/
│   └── snowflake_key.p8          # (gitignored, copied via scp)
├── airflow/
│   ├── dags/
│   │   └── .gitkeep
│   ├── src/
│   │   ├── config.py             # (gitignored, copied via scp)
│   │   └── ingestion/
│   │       └── .gitkeep
│   ├── logs/
│   │   └── .gitkeep
│   └── plugins/
│       └── .gitkeep
├── dbt/
│   └── .gitkeep
├── docs/
│   ├── data_sources.md
│   └── infrastructure_setup.md
└── notebooks/
    └── 01_data_exploration.ipynb
```

### Data Source Exploration

| Task | Status |
|------|--------|
| Identify capacity data source | ✅ |
| Identify demand data source | ✅ |
| Test API endpoints | ✅ |
| Explore columns | ✅ |
| Select columns to keep | ✅ |
| Document data sources | ✅ |

---

## Data Sources

### Source 1: Hospital Capacity (Supply)

- **Endpoint:** `https://data.cdc.gov/resource/ua7e-t2fy.json`
- **Grain:** Weekly, State-level
- **Geography format:** State abbreviations (`AL`, `CA`)
- **Date range:** 2024-10 to 2025-09

**Selected columns (12):**
- `weekendingdate`, `jurisdiction`
- `numinptbeds`, `numicubeds`
- `numinptbedsocc`, `numicubedsocc`
- `pctinptbedsocc`, `pcticubedsocc`
- `totalconfc19newadm`, `totalconfflunewadm`, `totalconfrsvnewadm`

### Source 2: ED Visits (Demand Signal)

- **Endpoint:** `https://data.cdc.gov/resource/vjzj-u7u8.json`
- **Grain:** Daily, State-level
- **Geography format:** State full names (`Alabama`, `California`)
- **Date range:** 2022-09 to 2025-12
- **Pathogens:** COVID, Influenza, RSV, ARI

**Columns (4):**
- `date`, `geography`, `pathogen`, `percent_visits`

---

## Key Data Integration Decisions

| Issue | Decision |
|-------|----------|
| Geography mismatch | Create state mapping table (abbreviation ↔ full name) |
| Grain mismatch | Aggregate demand from daily → weekly in dbt |
| Date overlap | Use Oct 2024 – Sep 2025 (~11 months) |

---

## Deployment Workflow

### Code Changes (ongoing)
```bash
# Local
git add .
git commit -m "message"
git push origin main

# EC2
cd ~/regional-hospital-capacity-planning
git pull
```

### Secrets (one-time setup)
```powershell
# From local Windows machine
scp -i "C:\Users\Admin\.ssh\EC2_luke.pem" ./keys/snowflake_key.p8 ubuntu@<EC2-IP>:~/regional-hospital-capacity-planning/keys/
scp -i "C:\Users\Admin\.ssh\EC2_luke.pem" ./airflow/src/config.py ubuntu@<EC2-IP>:~/regional-hospital-capacity-planning/airflow/src/
```

### Docker Commands (EC2)
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker logs regional-hospital-capacity-planning_airflow-webserver_1 --tail 50

# Fix logs permission (if needed)
sudo chown -R 50000:0 airflow/logs
```

### Access Airflow UI
```powershell
# SSH with tunnel (from local)
ssh -i "C:\Users\Admin\.ssh\EC2_luke.pem" -L 8080:localhost:8080 ubuntu@<EC2-IP>

# Then open browser to:
http://localhost:8080
# Login: airflow / airflow
```

---

## Files Created

| File | Purpose |
|------|---------|
| `notebooks/01_data_exploration.ipynb` | API testing and column exploration |
| `docs/data_sources.md` | Data dictionary and integration notes |
| `docs/infrastructure_setup.md` | S3, IAM, Snowflake, Docker setup |

---

## Next Steps (Phase 2: Data Ingestion)

1. Create extraction functions in `airflow/src/ingestion/`
   - `extract_hospital_capacity.py`
   - `extract_ed_visits.py`
2. Create DAG definitions in `airflow/dags/`
3. Land raw data in S3
4. Load raw data into Snowflake raw layer
5. Test end-to-end ingestion

---

## Reference: Key Paths

| Location | Path |
|----------|------|
| EC2 project root | `~/regional-hospital-capacity-planning` |
| S3 bucket | `s3://hospital-planning-raw-luke/` |
| Snowflake database | `RAW.HOSPITAL_PLANNING` |
| Snowflake stage | `@HOSPITAL_PLANNING_STAGE` |
| Container dags | `/opt/airflow/dags` |
| Container dbt | `/opt/airflow/dbt` |
| Container keys | `/opt/airflow/keys` |