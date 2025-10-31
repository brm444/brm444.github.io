#!/usr/bin/env python3
"""
Import WordPress comments to Talkyard in smaller batches
"""

import json
import requests
import time
import base64
import os

def import_batch(data_type, data, talkyard_url, api_secret):
    """Import a specific type of data"""
    
    # Construct Authorization header using the provided API secret
    # Format: tyid=2:{api_secret} encoded in Base64
    auth_string = f"tyid=2:{api_secret}"
    auth_b64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth_b64}'
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
    # IMPORTANT: Set your API secret via environment variable for security:
    # export TALKYARD_API_SECRET="your-secret-here"
    API_SECRET = os.getenv("TALKYARD_API_SECRET", "")
    if not API_SECRET:
        print("❌ Error: TALKYARD_API_SECRET environment variable not set!")
        print("Set it with: export TALKYARD_API_SECRET='your-secret-here'")
        return
    
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
        success &= import_batch('users', data['users'], TALKYARD_URL, API_SECRET)
        time.sleep(2)  # Wait between requests
    
    # 2. Import pages
    if data.get('pages'):
        success &= import_batch('pages', data['pages'], TALKYARD_URL, API_SECRET)
        time.sleep(2)
    
    # 3. Import posts in smaller batches of 5
    if data.get('posts'):
        posts = data['posts']
        batch_size = 5
        
        for i in range(0, len(posts), batch_size):
            batch = posts[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            print(f"\n--- Batch {batch_num} ---")
            
            success &= import_batch('posts', batch, TALKYARD_URL, API_SECRET)
            time.sleep(2)  # Wait between batches
    
    if success:
        print("\n🎉 All imports completed successfully!")
    else:
        print("\n💔 Some imports failed.")

if __name__ == "__main__":
    main()