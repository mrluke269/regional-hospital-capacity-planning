from config import SNOWFLAKE_CONFIG
import snowflake.connector

def copy_data_to_snowflake(key):


     # Establish Snowflake connection
    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    # Create a cursor object
    cs = conn.cursor()

    # Delete existing records for idempotency
    try:
        delete_command = f"""
        DELETE FROM RAW.HOSPITAL_PLANNING.CAPACITY_REPORTS
        WHERE source_file = '{key}';
        """

        cs.execute(delete_command)
    except Exception as e:
        print(f"Error during deletion for idempotency: {e}")
        raise

    #  COPY INTO command
    try:
        copy_command = f"""
        COPY INTO RAW.HOSPITAL_PLANNING.CAPACITY_REPORTS(
        raw_data,
        loaded_at,
        source_file
        )
        FROM (
            SELECT
                $1,
                current_timestamp(),
                METADATA$FILENAME
            FROM @RAW.HOSPITAL_PLANNING.HOSPITAL_PLANNING_STAGE/{key}
        )
        FILE_FORMAT = (TYPE = 'JSON', STRIP_OUTER_ARRAY = TRUE)
        FORCE = TRUE;"""

        cs.execute(copy_command)

        result = cs.fetchone()
        print(result)
        
    except Exception as e:
        print(f"Error during COPY INTO operation: {e}")
        raise
    finally:
        cs.close()
        conn.close()



if __name__ == "__main__":
    import extract_hospital_capacity
    data = extract_hospital_capacity.extract_hospital_capacity(max_records=2)
    import load_capacity_S3
    key = load_capacity_S3.load_capacity_S3(data)
    copy_data_to_snowflake(key)