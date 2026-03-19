"""
Facebook Scraper for Brockton MA Public Opinion Analysis

This script outlines the methodology using the facebook-scraper library 
to extract posts from public community pages. Due to Meta's strict anti-scraping
policies, logging in with cookies is usually required.

Pages targeted:
- Local news (e.g., The Enterprise)
- Community groups (e.g., The Brockton Hub)
- City pages (e.g., City of Brockton)
"""

import json
import time

try:
    from facebook_scraper import get_posts
except ImportError:
    get_posts = None

def scrape_facebook_pages(pages, pages_limit=2):
    if get_posts is None:
        print("facebook_scraper is not installed. Run `pip install facebook-scraper`")
        return []

    print("Initializing Facebook scraper...")
    all_posts = []
    
    for page in pages:
        print(f"Scraping page: {page}")
        try:
            # Requires cookies for reliable scraping
            for post in get_posts(page, pages=pages_limit, options={"comments": False}):
                all_posts.append({
                    'source': 'facebook',
                    'id': post['post_id'],
                    'text': post['text'],
                    'date': post['time'].isoformat() if post['time'] else None,
                    'author': page,
                    'likes': post['likes']
                })
            time.sleep(3)
        except Exception as e:
            print(f"Error scraping Facebook page {page}: {e}")
            
    return all_posts

if __name__ == "__main__":
    # Target public pages relevant to Brockton
    target_pages = [
        "TheBrocktonHub", 
        "enterprisenews",
        "BrocktonPublicSchools"
    ]
    
    data = scrape_facebook_pages(target_pages)
    
    with open("facebook_raw.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data)} Facebook posts to facebook_raw.json")
