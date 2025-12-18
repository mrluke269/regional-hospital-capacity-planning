# Data Sources Documentation

## Overview

This project integrates two CDC data sources to enable regional capacity planning and demand sensing for hospital systems.

---

## Source 1: Hospital Capacity (Supply)

**Name:** NHSN Weekly Hospital Respiratory Data  
**Endpoint:** `https://data.cdc.gov/resource/ua7e-t2fy.json`  
**Update Frequency:** Weekly  
**Grain:** Weekly, State-level  
**Date Range:** 2024-10 to 2025-09  

### Selected Columns

| Column | Description |
|--------|-------------|
| `weekendingdate` | End date of the reporting week |
| `jurisdiction` | State abbreviation (e.g., AL, CA, TX) |
| `numinptbeds` | Total inpatient beds |
| `numicubeds` | Total ICU beds |
| `numinptbedsocc` | Inpatient beds occupied |
| `numicubedsocc` | ICU beds occupied |
| `pctinptbedsocc` | Percent inpatient beds occupied |
| `pcticubedsocc` | Percent ICU beds occupied |
| `totalconfc19newadm` | New COVID-19 admissions |
| `totalconfflunewadm` | New influenza admissions |
| `totalconfrsvnewadm` | New RSV admissions |

---

## Source 2: Emergency Department Visits (Demand Signal)

**Name:** NSSP Emergency Department Respiratory Daily  
**Endpoint:** `https://data.cdc.gov/resource/vjzj-u7u8.json`  
**Update Frequency:** Weekly (Wednesdays)  
**Grain:** Daily, State-level  
**Date Range:** 2022-09 to 2025-12  

### Columns

| Column | Description |
|--------|-------------|
| `date` | Observation date |
| `geography` | State full name (e.g., Alabama, California) |
| `pathogen` | Disease type: COVID, Influenza, RSV, ARI |
| `percent_visits` | Percent of ED visits for this pathogen |

### Pathogen Values

- `COVID` — COVID-19
- `Influenza` — Seasonal flu
- `RSV` — Respiratory Syncytial Virus
- `ARI` — Acute Respiratory Illness (likely aggregate)

---

## Data Integration Notes

### Entity Resolution

| Attribute | Capacity | Demand | Resolution |
|-----------|----------|--------|------------|
| Geography | `AL` | `Alabama` | Mapping table required |

### Grain Alignment

| Source | Grain | Action |
|--------|-------|--------|
| Capacity | Weekly | None |
| Demand | Daily | Aggregate to weekly in dbt |

### Date Overlap

- **Usable range:** October 2024 – September 2025 (~11 months)
- Demand data extends beyond capacity data on both ends

---

## Potential Join Keys
```
capacity.jurisdiction = state_mapping.abbreviation
demand.geography = state_mapping.full_name

capacity.weekendingdate = demand.week_ending (after aggregation)
```

---

