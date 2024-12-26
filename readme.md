# Student Results Scraper

An automated web scraping solution that extracts student result data from the university website using Selenium automation and AI-powered CAPTCHA bypass.

## Features

- **Automated Data Extraction**: Utilizes Selenium WebDriver to navigate and scrape student results from the university portal
- **CAPTCHA Bypass**: Integrates Google's Gemini model via LangChain for intelligent text recognition and CAPTCHA solving
- **FastAPI Backend**: RESTful API implementation for efficient data processing and retrieval
- **Performance Impact**: Achieved 70% reduction in faculty workload for result verification

## Tech Stack

- Python
- Selenium WebDriver
- FastAPI
- LangChain
- Google Gemini AI Model

## Prerequisites

```bash
Python 3.8+
Chrome/Firefox WebDriver
Valid API key for Google Gemini
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/student-results-scraper.git
cd student-results-scraper
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
GEMINI_API_KEY=your_api_key_here
UNIVERSITY_URL=your_university_portal_url
```

## Usage

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Run the scraper:
```bash
python scraper.py
```
