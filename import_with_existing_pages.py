#!/usr/bin/env python3
"""
Import WordPress comments to existing Talkyard pages
Using the page mappings provided by Talkyard admin
"""

import json
import requests
import time
import base64
import os

def create_targeted_import_data():
    """Create import data targeting existing Talkyard pages"""
    
    # Load our original converted data
    with open('talkyard_comments_import.json', 'r', encoding='utf-8') as f:
        original_data = json.load(f)
    
    # Map WordPress post IDs to existing Talkyard pages based on admin info
    wp_to_talkyard_mapping = {
        # WordPress post 83 (KC/QMGS school song) -> Talkyard page 5 
        83: {
            'talkyard_page_id': 5,
            'urls': [
                '/2020-06-07/2-different-schools-but-the-same-song-kc-and-qmgs',
                'https://bankole.org/2020-06-07/2-different-schools-but-the-same-song-kc-and-qmgs'
            ]
        },
        # WordPress post 175 (Buffett/Munger) -> might map to another page or create new
        175: {
            'talkyard_page_id': None,  # Will create new page
            'urls': ['/2020-03-15/how-to-make-better-decisions-what-i-learned-from-buffett-and-munger']
        },
        # WordPress post 164 (Digital Infrastructure) -> might be another page or create new  
        164: {
            'talkyard_page_id': None,  # Will create new page
            'urls': ['/digital-infrastructure']
        }
    }
    
    # Create import data structure
    import_data = {
        "upsertOptions": {"sendNotifications": False},
        "posts": [],
        "users": []
    }
    
    # Track users we've added
    users_added = set()
    user_id_counter = 2000000001
    user_id_mapping = {}
    
    # Process each comment from original data
    for post in original_data['posts']:
        # Find which WordPress post this comment belongs to
        wp_post_id = None
        for page in original_data['pages']:
            if post['pageId'] == page['id']:
                # Extract WP post ID from page extId (format: wp-post-{id})
                wp_post_id = int(page['extId'].split('-')[-1])
                break
        
        if not wp_post_id or wp_post_id not in wp_to_talkyard_mapping:
            continue
            
        mapping = wp_to_talkyard_mapping[wp_post_id]
        
        # Handle user
        user_key = None
        for user in original_data['users']:
            if user['id'] == post['authorId']:
                user_key = (user['fullName'], user['email'])
                break
                
        if user_key and user_key not in users_added:
            users_added.add(user_key)
            user_id = user_id_counter
            user_id_counter += 1
            user_id_mapping[post['authorId']] = user_id
            
            # Find original user data
            for user in original_data['users']:
                if user['id'] == post['authorId']:
                    import_user = {
                        "id": user_id,
                        "extId": user['extId'],
                        "username": user['username'],
                        "fullName": user['fullName'],
                        "email": user['email'],
                        "createdAt": user['createdAt'],
                        "isEmailVerified": True,
                        "trustLevel": "NewMember"
                    }
                    import_data['users'].append(import_user)
                    break
        
        # Create the post/comment
        if mapping['talkyard_page_id']:
            # Comment on existing page
            import_post = {
                "id": 2000000000 + len(import_data['posts']) + 1,
                "extId": post['extId'],
                "pageId": mapping['talkyard_page_id'],
                "authorId": user_id_mapping.get(post['authorId'], user_id_counter - 1),
                "createdAt": post['createdAt'],
                "approvedAt": post['approvedAt'],
                "nr": 2000000000 + len(import_data['posts']) + 1,
                "parentNr": None,  # Start with no threading for simplicity
                "type": "Normal",
                "text": post['text']
            }
            import_data['posts'].append(import_post)
    
    return import_data

def import_to_existing_pages():
    """Import comments to existing Talkyard pages"""
    
    # IMPORTANT: Set your API secret via environment variable for security:
    # export TALKYARD_API_SECRET="your-secret-here"
    API_SECRET = os.getenv("TALKYARD_API_SECRET", "")
    if not API_SECRET:
        print("❌ Error: TALKYARD_API_SECRET environment variable not set!")
        print("Set it with: export TALKYARD_API_SECRET='your-secret-here'")
        return
    
    TALKYARD_URL = "https://site-1hamqpkqkr.talkyard.net"
    
    # Create targeted import data
    import_data = create_targeted_import_data()
    
    print(f"Importing {len(import_data['posts'])} posts from {len(import_data['users'])} users to existing pages...")
    
    # Construct Authorization header using the provided API secret
    # Format: tyid=2:{api_secret} encoded in Base64
    auth_string = f"tyid=2:{API_SECRET}"
    auth_b64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth_b64}'
    }
    
    # Try importing users first
    if import_data['users']:
        print("Importing users...")
        user_payload = {
            "upsertOptions": {"sendNotifications": False},
            "users": import_data['users']
        }
        
        try:
            response = requests.post(f"{TALKYARD_URL}/-/v0/upsert", 
                                   json=user_payload, headers=headers, timeout=60)
            if response.status_code == 200:
                print("✅ Users imported successfully!")
            else:
                print(f"⚠️  User import status: {response.status_code}")
                print(f"Response: {response.text[:500]}")
        except Exception as e:
            print(f"User import error: {e}")
        
        time.sleep(2)
    
    # Import posts in small batches
    if import_data['posts']:
        batch_size = 3
        for i in range(0, len(import_data['posts']), batch_size):
            batch = import_data['posts'][i:i + batch_size]
            print(f"Importing posts batch {i//batch_size + 1} ({len(batch)} posts)...")
            
            post_payload = {
                "upsertOptions": {"sendNotifications": False},
                "posts": batch
            }
            
            try:
                response = requests.post(f"{TALKYARD_URL}/-/v0/upsert", 
                                       json=post_payload, headers=headers, timeout=60)
                if response.status_code == 200:
                    print(f"✅ Batch {i//batch_size + 1} imported successfully!")
                else:
                    print(f"⚠️  Batch {i//batch_size + 1} status: {response.status_code}")
                    print(f"Response: {response.text[:500]}")
            except Exception as e:
                print(f"Batch import error: {e}")
            
            time.sleep(2)
    
    print("\n🎉 Import process completed!")
    print("Check your Talkyard site to see if comments appeared.")

if __name__ == "__main__":
    import_to_existing_pages()