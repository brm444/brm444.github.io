#!/usr/bin/env python3
"""
Import WordPress comments to Talkyard in smaller batches
"""

import json
import requests
import time

def import_batch(data_type, data, talkyard_url):
    """Import a specific type of data"""
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic dHlpZD0yOjExc3g2cWNpZThvZWNlbWdoNDlhZ3JmbXVm'
    }
    
    api_url = f"{talkyard_url}/-/v0/upsert"
    
    payload = {"upsertOptions": {"sendNotifications": False}}
    payload[data_type] = data
    
    print(f"Importing {len(data)} {data_type}...")
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            print(f"✅ {data_type} imported successfully!")
            return True
        else:
            print(f"❌ {data_type} import failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    TALKYARD_URL = "https://site-1hamqpkqkr.talkyard.net"
    JSON_FILE = "talkyard_comments_import.json"
    
    # Load the JSON data
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("🚀 Starting batch import...")
    
    # Import in order: users first, then pages, then posts
    success = True
    
    # 1. Import users
    if data.get('users'):
        success &= import_batch('users', data['users'], TALKYARD_URL)
        time.sleep(2)  # Wait between requests
    
    # 2. Import pages
    if data.get('pages'):
        success &= import_batch('pages', data['pages'], TALKYARD_URL)
        time.sleep(2)
    
    # 3. Import posts in smaller batches of 5
    if data.get('posts'):
        posts = data['posts']
        batch_size = 5
        
        for i in range(0, len(posts), batch_size):
            batch = posts[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            print(f"\n--- Batch {batch_num} ---")
            
            success &= import_batch('posts', batch, TALKYARD_URL)
            time.sleep(2)  # Wait between batches
    
    if success:
        print("\n🎉 All imports completed successfully!")
    else:
        print("\n💔 Some imports failed.")

if __name__ == "__main__":
    main()