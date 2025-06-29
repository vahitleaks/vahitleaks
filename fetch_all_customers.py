#!/usr/bin/env python3
import requests
import json
import time
import urllib.parse

def fetch_customers_batch(start, length, draw):
    """Fetch a batch of customers from the API"""
    
    url = "https://tekbas.hamurlabs.io/customer/list/search/"
    
    headers = {
        "Host": "tekbas.hamurlabs.io",
        "Cookie": "csrftoken=dfRzwgXNQNQg8XH114OFKk2WHbjZX3CDhjxfnY384U62h0r3dseSFFJkrBuSsF4w; sessionid=87yim331q9scdrk1veehld5mj0gugmam",
        "X-Csrftoken": "dfRzwgXNQNQg8XH114OFKk2WHbjZX3CDhjxfnY384U62h0r3dseSFFJkrBuSsF4w",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br"
    }
    
    # Build the data payload
    columns = [
        "id", "external_id", "name", "email", "price_group", "is_corporate", 
        "is_fraud", "is_active", "country", "city", "created_at", "source", 
        "segment", "customer_group", "tc_kimlik_no", "tax_no", "integration_external_id"
    ]
    
    data_dict = {
        f"draw": draw,
        f"start": start,
        f"length": length,
        "search[value]": "",
        "search[regex]": "false",
        "order[0][column]": "0",
        "order[0][dir]": "asc"
    }
    
    # Add column definitions
    for i, col in enumerate(columns):
        data_dict[f"columns[{i}][data]"] = col
        data_dict[f"columns[{i}][name]"] = ""
        data_dict[f"columns[{i}][searchable]"] = "true"
        data_dict[f"columns[{i}][orderable]"] = "true"
        data_dict[f"columns[{i}][search][value]"] = ""
        data_dict[f"columns[{i}][search][regex]"] = "false"
    
    # URL encode the data
    data = urllib.parse.urlencode(data_dict)
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching batch start={start}, length={length}: {e}")
        return None

def main():
    print("Starting to fetch all customer records...")
    
    all_customers = []
    batch_size = 1000
    start = 0
    draw = 1
    total_records = 63722
    
    while start < total_records:
        print(f"Fetching records {start} to {start + batch_size - 1}...")
        
        batch_data = fetch_customers_batch(start, batch_size, draw)
        
        if batch_data and 'data' in batch_data:
            all_customers.extend(batch_data['data'])
            print(f"Fetched {len(batch_data['data'])} records. Total so far: {len(all_customers)}")
            
            # Update total if needed
            if 'recordsTotal' in batch_data:
                total_records = batch_data['recordsTotal']
        else:
            print(f"Failed to fetch batch starting at {start}")
            break
            
        start += batch_size
        draw += 1
        
        # Small delay to be nice to the server
        time.sleep(0.5)
    
    # Save all customers to JSON file
    output_file = "all_customers_complete.json"
    final_data = {
        "total_records": len(all_customers),
        "recordsTotal": total_records,
        "customers": all_customers
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully saved {len(all_customers)} customer records to {output_file}")

if __name__ == "__main__":
    main()