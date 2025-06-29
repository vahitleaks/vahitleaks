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

def download_document(url, docs_folder):
    """Download a document from the given URL"""
    
    try:
        # Parse URL to get filename
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # If no filename, create one from the URL
        if not filename or '.' not in filename:
            filename = f"document_{hash(url) % 10000}.pdf"
        
        # Ensure docs folder exists
        os.makedirs(docs_folder, exist_ok=True)
        
        filepath = os.path.join(docs_folder, filename)
        
        print(f"Downloading: {filename}")
        
        # Download with timeout
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()
        
        # Save file
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✓ Downloaded: {filename} ({len(response.content)} bytes)")
        return True
        
    except Exception as e:
        print(f"✗ Failed to download {url}: {e}")
        return False

def main():
    json_file = "documents_response.json"
    docs_folder = "docs"
    
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
        if download_document(url, docs_folder):
            success_count += 1
        
        # Small delay between downloads
        time.sleep(0.5)
    
    print(f"\n\nDownload completed!")
    print(f"Successfully downloaded: {success_count}/{total_count} documents")
    print(f"Documents saved to: {os.path.abspath(docs_folder)}")

if __name__ == "__main__":
    main()