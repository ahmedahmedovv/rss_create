from flask import Flask, render_template
import json
from datetime import datetime
import os

app = Flask(__name__)

# Add custom datetime filter
@app.template_filter('datetime')
def format_datetime(value):
    try:
        if isinstance(value, str):
            dt = datetime.fromisoformat(value)
        else:
            dt = value
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return value

@app.route('/')
def index():
    try:
        with open('public/feeds.json', 'r', encoding='utf-8') as f:
            feeds_data = json.load(f)
    except FileNotFoundError:
        feeds_data = {
            'feeds': [],
            'last_updated': datetime.now().isoformat()
        }
    
    return render_template('index.html', feeds=feeds_data['feeds'], 
                         last_updated=feeds_data['last_updated'])

if __name__ == '__main__':
    app.run(debug=True) 