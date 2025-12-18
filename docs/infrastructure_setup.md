# Infrastructure Setup: S3 to Snowflake Pipeline



## Overview

This document describes the infrastructure that enables data flow from AWS S3 into Snowflake.
```
S3 Bucket → (IAM Role) → Storage Integration → Stage → Snowflake Tables
```

---

## AWS Components

### S3 Bucket
- **Bucket Name:** `hospital-planning-raw-luke`
- **Region:** us-east-2
- **Purpose:** Landing zone for raw data files (hospital capacity, ED visits)

### IAM Role
- **Role Name:** `snowflake_read_s3`
- **ARN:** `arn:aws:iam::565569641650:role/snowflake_read_s3`
- **Policy:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::hospital-planning-raw-luke",
                "arn:aws:s3:::hospital-planning-raw-luke/*"
            ]
        }
    ]
}
```

---

## Snowflake Components

### Storage Integration (Account-Level)
```sql
-- View integration details
DESC STORAGE INTEGRATION snowflake_s3;

-- Update allowed locations (if needed)
ALTER STORAGE INTEGRATION snowflake_s3
SET STORAGE_ALLOWED_LOCATIONS = ('s3://hospital-planning-raw-luke/');
```

### Stage (Database-Level)
- **Database:** RAW
- **Schema:** HOSPITAL_PLANNING
- **Stage Name:** HOSPITAL_PLANNING_STAGE
```sql
CREATE OR REPLACE STAGE hospital_planning_stage
  URL = 's3://hospital-planning-raw-luke/'
  STORAGE_INTEGRATION = snowflake_s3;

-- Verify
SHOW STAGES;
LIST @hospital_planning_stage;
```

---

## Verification Commands
```sql
-- Check storage integration
DESC STORAGE INTEGRATION snowflake_s3;

-- Check stage exists
SHOW STAGES IN SCHEMA RAW.HOSPITAL_PLANNING;

-- List files in stage (once data is loaded)
LIST @hospital_planning_stage;
```