import requests
import time


base_url = "https://data.cdc.gov/resource/ua7e-t2fy.json"
PAGE_SIZE = 1000
RATE_LIMIT_DELAY = 1 


def extract_hospital_capacity(max_records=None):
    results_combined = []
    # Get total count of records
    count_response = requests.get(base_url, params={"$select": "count(*)"})
    total_count = int(count_response.json()[0]['count'])
    print(f"Total records to fetch: {total_count}")
      
    # Initialize offset
    offset = 0
  
    # Pagination loop
    if max_records is None:
    
        while offset < total_count:
            response = requests.get(base_url, 
                                params={"$limit": PAGE_SIZE, "$offset": offset})
            data = response.json()
            results_combined.extend(data)
            print(f"Extracted {len(data)} records starting from {offset}")
            offset += len(data)
            time.sleep(RATE_LIMIT_DELAY) 

    else:
        response = requests.get(base_url, 
                                params={"$limit": max_records})
        data = response.json()
        results_combined.extend(data)
        print(f"Extracted {len(data)} records for testing")
    print(f"Total records extracted: {len(results_combined)}")
    return results_combined

if __name__ == "__main__":
    data = extract_hospital_capacity(max_records=2)
    print(f"Total records fetched: {len(data)}")
    print(f"First record: {data[0]}")