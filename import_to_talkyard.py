#!/usr/bin/env python3
"""
Import WordPress comments to Talkyard using the /-/v0/upsert API
"""

import json
import requests
import sys
import time
import base64
from datetime import datetime

def fix_talkyard_ids(data):
    """
    Fix the ID sequence to start from 2,000,000,001 as required by Talkyard
    """
    # Talkyard requires IDs to start from 2,000,000,001
    id_base = 2000000000
    
    # Fix user IDs
    user_id_mapping = {}
    for i, user in enumerate(data['users']):
        old_id = user['id']
        new_id = id_base + i + 1
        user['id'] = new_id
        user_id_mapping[old_id] = new_id
    
    # Fix page IDs
    page_id_mapping = {}
    for i, page in enumerate(data['pages']):
        old_id = page['id']
        new_id = f"page-{id_base + i + 1}"
        page['id'] = new_id
        page_id_mapping[old_id] = new_id
    
    # Fix post IDs and references
    for i, post in enumerate(data['posts']):
        # Update post ID
        post['id'] = id_base + i + 1
        
        # Update author ID reference
        for old_user_id, new_user_id in user_id_mapping.items():
            if post['authorId'] == old_user_id:
                post['authorId'] = new_user_id
                break
        
        # Update page ID reference
        for old_page_id, new_page_id in page_id_mapping.items():
            if post['pageId'] == old_page_id:
                post['pageId'] = new_page_id
                break
        
        # Update post nr (post number) to start from 2,000,000,001
        post['nr'] = id_base + i + 1
        
        # Update parent nr if it exists
        if post.get('parentNr'):
            # Find the corresponding post and update parent reference
            for j, other_post in enumerate(data['posts']):
                if other_post.get('nr') == post['parentNr']:
                    post['parentNr'] = id_base + j + 1
                    break
    
    return data

def import_to_talkyard(json_file_path, api_secret, talkyard_url):
    """
    Import comments to Talkyard using the /-/v0/upsert API
    """
    
    # Load the JSON data
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Fix IDs according to Talkyard requirements
    data = fix_talkyard_ids(data)
    
    # Prepare the upsert payload
    upsert_payload = {
        "upsertOptions": {
            "sendNotifications": False  # Don't send notifications for imported comments
        },
        "pages": data['pages'],
        "posts": data['posts'],
        "users": data['users']
    }
    
    # API endpoint
    api_url = f"{talkyard_url}/-/v0/upsert"
    
    # Construct Authorization header using the provided API secret
    # Format: tyid=2:{api_secret} encoded in Base64
    auth_string = f"tyid=2:{api_secret}"
    auth_b64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth_b64}'
    }
    
    print(f"Importing {len(data['posts'])} posts from {len(data['users'])} users...")
    print(f"Sending to: {api_url}")
    
    try:
        # Make the API request
        response = requests.post(api_url, json=upsert_payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            print("✅ Comments imported successfully!")
            print(f"Response: {response.text}")
            return True
        else:
            print(f"❌ Import failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """
    Main function - you'll need to provide your API secret and Talkyard URL
    """
    
    # Configuration
    # IMPORTANT: Set your API secret via environment variable for security:
    # export TALKYARD_API_SECRET="your-secret-here"
    # Or update the value below (not recommended for production)
    import os
    TALKYARD_URL = "https://site-1hamqpkqkr.talkyard.net"
    API_SECRET = os.getenv("TALKYARD_API_SECRET", "")  # Read from environment variable
    if not API_SECRET:
        print("❌ Error: TALKYARD_API_SECRET environment variable not set!")
        print("Set it with: export TALKYARD_API_SECRET='your-secret-here'")
        sys.exit(1)
    JSON_FILE = "talkyard_comments_import.json"
    
    print("🚀 Starting Talkyard import...")
    print(f"Talkyard URL: {TALKYARD_URL}")
    print(f"JSON file: {JSON_FILE}")
    
    success = import_to_talkyard(JSON_FILE, API_SECRET, TALKYARD_URL)
    
    if success:
        print("\n🎉 Import completed successfully!")
        print("\nNext steps:")
        print("1. Visit your Talkyard site to verify the comments were imported")
        print("2. Check that the comments appear on the correct pages")
        print("3. Test that comment threading is working correctly")
    else:
        print("\n💔 Import failed. Please check the error messages above.")

if __name__ == "__main__":
    main()