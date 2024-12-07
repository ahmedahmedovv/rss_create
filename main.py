import os
import yaml
from scrapers.scraper_factory import create_scrapers_from_config
from scrapers.rss_generator import RSSGenerator

def ensure_output_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    output_dir = "headlines"
    rss_dir = "rss"
    
    # Read base URL from environment variable or config file
    base_url = os.getenv('RSS_BASE_URL', 'http://localhost')  # Default fallback to localhost
    
    # Alternative: Read from config file
    try:
        with open('config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file)
            base_url = config.get('base_url', 'http://localhost')
    except FileNotFoundError:
        print("Warning: config.yaml not found, using default base URL")
    
    ensure_output_dir(output_dir)
    ensure_output_dir(rss_dir)
    
    # Create scrapers from yaml config file
    scrapers = create_scrapers_from_config("config.yaml", output_dir)
    
    # Run all scrapers
    for scraper in scrapers:
        print(f"Running {scraper.site_id} scraper...")
        scraper.get_headlines()
    
    # Generate RSS feeds
    rss_generator = RSSGenerator(output_dir, rss_dir, base_url)
    rss_generator.generate_all_feeds()

if __name__ == "__main__":
    main() 