import os
import yaml
from scrapers.scraper_factory import create_scrapers_from_config
from scrapers.rss_generator import RSSGenerator
import json
from datetime import datetime

def ensure_output_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_feeds_index(rss_dir, output_dir, public_dir):
    """Generate a feeds.json file containing information about all available feeds"""
    feeds = []
    
    # Get all XML files from rss directory
    for filename in os.listdir(rss_dir):
        if filename.endswith('.xml'):
            feed_id = filename.replace('.xml', '')
            
            # Try to get timestamp from corresponding JSON file
            try:
                with open(os.path.join(output_dir, f"{feed_id}.json"), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    timestamp = data.get('timestamp')
            except:
                timestamp = datetime.now().isoformat()
            
            feeds.append({
                'id': feed_id,
                'title': feed_id.upper(),
                'rss_url': f'/rss/{filename}',
                'json_url': f'/headlines/{feed_id}.json',
                'last_updated': timestamp
            })
    
    # Sort feeds by ID
    feeds.sort(key=lambda x: x['id'])
    
    # Save feeds index
    index_data = {
        'feeds': feeds,
        'last_updated': datetime.now().isoformat()
    }
    
    # Save to public directory
    with open(os.path.join(public_dir, 'feeds.json'), 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)

def main():
    output_dir = "headlines"
    rss_dir = "rss"
    public_dir = "public"
    
    # Read base URL from environment variable or config file
    base_url = os.getenv('RSS_BASE_URL', 'http://localhost')  # Default fallback to localhost
    
    # Alternative: Read from config file
    try:
        with open('config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file)
            base_url = config.get('base_url', 'http://localhost')
    except FileNotFoundError:
        print("Warning: config.yaml not found, using default base URL")
    
    # Create directories if they don't exist
    for directory in [output_dir, rss_dir, public_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Create scrapers from yaml config file
    scrapers = create_scrapers_from_config("config.yaml", output_dir)
    
    # Run all scrapers
    for scraper in scrapers:
        print(f"Running {scraper.site_id} scraper...")
        scraper.get_headlines()
    
    # Generate RSS feeds
    rss_generator = RSSGenerator(output_dir, rss_dir, base_url)
    rss_generator.generate_all_feeds()
    
    # Generate feeds index
    generate_feeds_index(rss_dir, output_dir, public_dir)

if __name__ == "__main__":
    main() 