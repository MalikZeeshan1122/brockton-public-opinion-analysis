"""
Synthetic Dataset Generator for Brockton MA Public Opinion Analysis
"""

import json
import random
from datetime import datetime, timedelta
import os

def generate_mock_dataset(num_records=500):
    topics = ["Education", "Safety & Crime", "Youth Programs", "Parks & Recreation", "Mental Health", "Jobs & Economy"]
    topic_weights = [0.3, 0.25, 0.15, 0.1, 0.1, 0.1]
    
    sentiments = ["Positive", "Neutral", "Negative"]
    
    # Topic specific sentiment weights to make data look realistic
    sentiment_weights = {
        "Education": [0.2, 0.3, 0.5],
        "Safety & Crime": [0.1, 0.2, 0.7],
        "Youth Programs": [0.6, 0.3, 0.1],
        "Parks & Recreation": [0.5, 0.3, 0.2],
        "Mental Health": [0.1, 0.2, 0.7],
        "Jobs & Economy": [0.2, 0.4, 0.4]
    }

    keywords_by_topic = {
        "Education": ["schools", "teachers", "funding", "students", "high school", "BHS", "budget", "classrooms"],
        "Safety & Crime": ["police", "safety", "crime", "patrol", "neighborhood", "dangerous", "protect"],
        "Youth Programs": ["after school", "boys and girls club", "sports", "mentoring", "summer camp", "activities"],
        "Parks & Recreation": ["parks", "clean", "playground", "dws", "field", "basketball", "outside"],
        "Mental Health": ["counseling", "stress", "support", "therapist", "mental health", "anxiety"],
        "Jobs & Economy": ["summer jobs", "employment", "local business", "hiring", "economy", "opportunity"]
    }
    
    sources = ["Twitter", "Facebook", "Instagram"]
    source_weights = [0.4, 0.45, 0.15]
    
    dataset = []
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180) # Past 6 months
    delta = end_date - start_date
    
    for i in range(num_records):
        # Determine topic
        topic = random.choices(topics, weights=topic_weights)[0]
        
        # Determine sentiment
        sentiment = random.choices(sentiments, weights=sentiment_weights[topic])[0]
        
        # Determine source
        source = random.choices(sources, weights=source_weights)[0]
        
        # Pick 2-3 random keywords for the word cloud
        post_keywords = random.sample(keywords_by_topic[topic], k=random.randint(2, 3))
        
        # Random date
        random_days = random.randrange(delta.days)
        post_date = start_date + timedelta(days=random_days)
        
        record = {
            "id": f"post_{i}",
            "source": source,
            "topic": topic,
            "sentiment": sentiment,
            "keywords": post_keywords,
            "date": post_date.strftime("%Y-%m-%d")
        }
        dataset.append(record)
        
    return dataset

if __name__ == "__main__":
    data = generate_mock_dataset(600)
    # Output to website folder so frontend can fetch it easily
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "website")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "dataset.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Generated {len(data)} synthetic records securely saved to {output_path}")
