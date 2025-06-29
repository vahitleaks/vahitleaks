#!/usr/bin/env python3
import json
import re
import os
import requests
from urllib.parse import urlparse
import time

def extract_amazon_links(json_file):
    """Extract all Amazon S3 download links from the JSON response"""
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    amazon_links = []
    
    # Look for Amazon S3 URLs in the data
    json_str = json.dumps(data)
    
    # Find all amazonaws.com URLs
    amazon_pattern = r'https://[^"]*\.amazonaws\.com/[^"]*'
    matches = re.findall(amazon_pattern, json_str)
    
    # Also look for any S3 URLs
    s3_pattern = r'https://s3[^"]*amazonaws\.com/[^"]*'
    s3_matches = re.findall(s3_pattern, json_str)
    
    all_links = list(set(matches + s3_matches))
    
    # Clean up links (remove any trailing characters)
    cleaned_links = []
    for link in all_links:
        # Remove any trailing non-URL characters
        link = re.sub(r'[^a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=%].*$', '', link)
        if link and 'amazonaws.com' in link:
            cleaned_links.append(link)
    
    return list(set(cleaned_links))

def download_document_with_auth(url, docs_folder, session):
    """Download a document from the given URL with authentication"""
    
    try:
        # Parse URL to get filename
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # If no filename, create one from the URL
        if not filename or '.' not in filename:
            filename = f"document_{hash(url) % 10000}.xlsx"
        
        # Ensure docs folder exists
        os.makedirs(docs_folder, exist_ok=True)
        
        filepath = os.path.join(docs_folder, filename)
        
        print(f"Downloading: {filename}")
        
        # Download with authentication headers
        response = session.get(url, timeout=30, stream=True)
        response.raise_for_status()
        
        # Save file
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = os.path.getsize(filepath)
        print(f"✓ Downloaded: {filename} ({file_size} bytes)")
        return True
        
    except Exception as e:
        print(f"✗ Failed to download {url}: {e}")
        return False

def main():
    json_file = "documents_response.json"
    docs_folder = "docs"
    
    # Setup session with authentication headers
    session = requests.Session()
    session.headers.update({
        "Cookie": "csrftoken=dfRzwgXNQNQg8XH114OFKk2WHbjZX3CDhjxfnY384U62h0r3dseSFFJkrBuSsF4w; sessionid=87yim331q9scdrk1veehld5mj0gugmam",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Referer": "https://tekbas.hamurlabs.io/document/list/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    })
    
    print("Extracting Amazon download links...")
    
    # Extract links
    amazon_links = extract_amazon_links(json_file)
    
    if not amazon_links:
        print("No Amazon S3 links found in the response.")
        return
    
    print(f"Found {len(amazon_links)} Amazon S3 download links:")
    for i, link in enumerate(amazon_links, 1):
        print(f"{i}. {link}")
    
    print(f"\nStarting download to '{docs_folder}' folder...")
    
    # Download each document
    success_count = 0
    total_count = len(amazon_links)
    
    for i, url in enumerate(amazon_links, 1):
        print(f"\n[{i}/{total_count}]", end=" ")
        if download_document_with_auth(url, docs_folder, session):
            success_count += 1
        
        # Small delay between downloads
        time.sleep(1)
    
    print(f"\n\nDownload completed!")
    print(f"Successfully downloaded: {success_count}/{total_count} documents")
    print(f"Documents saved to: {os.path.abspath(docs_folder)}")

if __name__ == "__main__":
    main()