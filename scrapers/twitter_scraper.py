"""
Twitter/X Scraper for Brockton MA Public Opinion Analysis

This script demonstrates data collection from Twitter using the ntscraper library.
Since Twitter frequently updates its DOM and rate limits anonymous scrapers, this
script serves as the methodological approach. For a guaranteed demonstration, 
use the synthetic dataset generator provided.
"""

import json
import time

try:
    from ntscraper import Nitter
except ImportError:
    Nitter = None

def scrape_twitter(queries, max_tweets=50):
    if Nitter is None:
        print("ntscraper is not installed. Run `pip install ntscraper`")
        print("Falling back to simulated collection for demonstration purposes.")
        return []

    print("Initializing Nitter scraper...")
    scraper = Nitter(log_level=1, skip_instance_check=False)
    
    all_tweets = []
    
    for query in queries:
        print(f"Scraping query: {query}")
        try:
            # fetch tweets using a public nitter instance
            results = scraper.get_tweets(query, mode='term', number=max_tweets)
            if results and 'tweets' in results:
                for tweet in results['tweets']:
                    all_tweets.append({
                        'source': 'twitter',
                        'id': tweet['link'],
                        'text': tweet['text'],
                        'date': tweet['date'],
                        'author': tweet['user']['name']
                    })
            time.sleep(2)  # pause to avoid rate limits
        except Exception as e:
            print(f"Error scraping {query}: {e}")
            
    return all_tweets

if __name__ == "__main__":
    target_queries = [
        "Brockton youth",
        "Brockton high school",
        "Brockton parks",
        "Brockton community safety"
    ]
    
    data = scrape_twitter(target_queries)
    
    with open("twitter_raw.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data)} tweets to twitter_raw.json")
