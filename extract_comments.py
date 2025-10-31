#!/usr/bin/env python3
"""
WordPress to Talkyard Comment Converter
Extracts legitimate comments from WordPress database and converts them to Talkyard JSON format
"""

import re
import gzip
import json
from datetime import datetime
from urllib.parse import urlparse
import hashlib

def extract_comments_from_sql(sql_file_path):
    """Extract comments from WordPress SQL dump"""
    comments = []
    
    with gzip.open(sql_file_path, 'rt', encoding='utf-8') as f:
        content = f.read()
    
    # Find the INSERT statement for comments
    pattern = r"INSERT INTO `wpcu_comments` VALUES \((.*?)\);"
    matches = re.findall(pattern, content, re.DOTALL)
    
    if matches:
        # Parse the VALUES part
        values_string = matches[0]
        # Split by ),( to get individual comment records
        comment_records = re.split(r'\),\(', values_string)
        
        for record in comment_records:
            # Clean up the record
            record = record.strip('()')
            
            # Parse the comma-separated values, being careful with quoted strings
            values = []
            current_value = ""
            in_quotes = False
            escape_next = False
            
            i = 0
            while i < len(record):
                char = record[i]
                
                if escape_next:
                    current_value += char
                    escape_next = False
                elif char == '\\':
                    current_value += char
                    escape_next = True
                elif char == "'" and not escape_next:
                    in_quotes = not in_quotes
                    current_value += char
                elif char == ',' and not in_quotes:
                    values.append(current_value.strip())
                    current_value = ""
                else:
                    current_value += char
                
                i += 1
            
            # Don't forget the last value
            if current_value:
                values.append(current_value.strip())
            
            if len(values) >= 15:  # Ensure we have enough fields
                comment_id = values[0]
                post_id = values[1]
                author = values[2].strip("'")
                author_email = values[3].strip("'")
                author_url = values[4].strip("'")
                author_ip = values[5].strip("'")
                comment_date = values[6].strip("'")
                comment_date_gmt = values[7].strip("'")
                comment_content = values[8].strip("'")
                comment_approved = values[10].strip("'")
                comment_parent = values[13]
                
                # Only include approved comments (not spam)
                if comment_approved == '1':
                    comments.append({
                        'id': int(comment_id),
                        'post_id': int(post_id),
                        'author': author,
                        'author_email': author_email,
                        'author_url': author_url,
                        'author_ip': author_ip,
                        'date': comment_date,
                        'date_gmt': comment_date_gmt,
                        'content': comment_content.replace('\\r\\n', '\n').replace('\\n', '\n'),
                        'parent': int(comment_parent) if comment_parent != '0' else 0
                    })
    
    return comments

def get_post_slug_from_id(post_id):
    """Map WordPress post IDs to Jekyll post slugs based on known mappings"""
    # You'll need to map these based on your actual post IDs from WordPress
    post_mappings = {
        83: "2-different-schools-but-the-same-song-kc-lagos-and-qmgs-walsall",
        175: "how-to-make-better-decisions-what-i-learned-from-buffett-and-munger", 
        164: "digital-infrastructure",
        # Add more mappings as needed
    }
    return post_mappings.get(post_id, f"post-{post_id}")

def generate_external_id(comment):
    """Generate a unique external ID for the comment"""
    # Use a combination of comment ID and author email hash
    email_hash = hashlib.md5(comment['author_email'].encode()).hexdigest()[:8]
    return f"wp-{comment['id']}-{email_hash}"

def convert_to_talkyard_json(comments):
    """Convert WordPress comments to Talkyard JSON format"""
    
    # Group comments by post
    posts_comments = {}
    for comment in comments:
        post_id = comment['post_id']
        if post_id not in posts_comments:
            posts_comments[post_id] = []
        posts_comments[post_id].append(comment)
    
    # Create Talkyard JSON structure
    talkyard_data = {
        "meta": {
            "exportedAt": datetime.now().isoformat(),
            "formatVersion": "0.0.1",
            "sourceSystem": "WordPress"
        },
        "site": {
            "id": "bankole-org-import",
            "extId": "bankole-org-wp",
            "name": "Bankole.org Comments",
            "createdAt": "2020-01-01T00:00:00Z"
        },
        "pages": [],
        "posts": [],
        "users": []
    }
    
    # Keep track of users we've seen
    users_seen = set()
    user_id_counter = 1
    user_mapping = {}
    
    # Process each post and its comments
    for post_id, post_comments in posts_comments.items():
        post_slug = get_post_slug_from_id(post_id)
        
        # Create page for this post
        page = {
            "id": f"page-{post_id}",
            "extId": f"wp-post-{post_id}",
            "title": post_slug.replace('-', ' ').title(),
            "url": f"/{post_slug}/",
            "createdAt": min(comment['date'] for comment in post_comments) + "Z",
            "htmlTagCssClasses": "",
            "htmlHeadTags": "",
            "layout": "DiscussionPageLayout"
        }
        talkyard_data["pages"].append(page)
        
        # Create posts (comments) for this page
        for comment in post_comments:
            # Handle user
            user_key = (comment['author'], comment['author_email'])
            if user_key not in users_seen:
                users_seen.add(user_key)
                user_id = f"user-{user_id_counter}"
                user_id_counter += 1
                user_mapping[user_key] = user_id
                
                # Create user
                user = {
                    "id": user_id,
                    "extId": generate_external_id(comment) + "-user",
                    "username": comment['author'].replace(' ', '').lower()[:20],
                    "fullName": comment['author'],
                    "email": comment['author_email'],
                    "createdAt": comment['date'] + "Z",
                    "isEmailVerified": True,
                    "trustLevel": "NewMember"
                }
                talkyard_data["users"].append(user)
            else:
                user_id = user_mapping[user_key]
            
            # Create post (comment)
            post = {
                "id": f"post-{comment['id']}",
                "extId": generate_external_id(comment),
                "pageId": f"page-{post_id}",
                "authorId": user_id,
                "createdAt": comment['date'] + "Z",
                "approvedAt": comment['date'] + "Z",
                "nr": comment['id'],
                "parentNr": comment['parent'] if comment['parent'] > 0 else None,
                "type": "Normal",
                "text": comment['content']
            }
            talkyard_data["posts"].append(post)
    
    return talkyard_data

def main():
    print("Extracting WordPress comments...")
    
    # Extract comments from SQL dump
    comments = extract_comments_from_sql('backup/database/bankoleo_wp352.sql.gz')
    print(f"Found {len(comments)} legitimate comments")
    
    # Convert to Talkyard format
    talkyard_data = convert_to_talkyard_json(comments)
    print(f"Converted to Talkyard format with {len(talkyard_data['posts'])} posts from {len(talkyard_data['users'])} users")
    
    # Save to JSON file
    with open('talkyard_comments_import.json', 'w', encoding='utf-8') as f:
        json.dump(talkyard_data, f, indent=2, ensure_ascii=False)
    
    print("Comments exported to: talkyard_comments_import.json")
    
    # Also create a summary
    print("\nComment Summary:")
    post_counts = {}
    for comment in comments:
        post_id = comment['post_id']
        post_counts[post_id] = post_counts.get(post_id, 0) + 1
    
    for post_id, count in post_counts.items():
        slug = get_post_slug_from_id(post_id)
        print(f"  Post {post_id} ({slug}): {count} comments")

if __name__ == "__main__":
    main()