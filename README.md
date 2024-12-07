# News Headlines Scraper

A Python-based web scraping tool that automatically collects headlines from various news websites and generates RSS feeds. This tool supports multiple news sources and can be easily configured through a YAML file.

## 🚀 Features

- Multi-source headline scraping
- Automatic RSS feed generation
- Markdown and JSON output formats
- YAML-based configuration
- Support for both CSS selectors and XPath
- Handles relative and absolute URLs
- Error handling and logging

## 📋 Prerequisites

- Python 3.7 or higher
- pip package manager

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd news-headlines-scraper
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

The scraper is configured through `config.yaml`. Add your news sources in the following format: # rss_create
