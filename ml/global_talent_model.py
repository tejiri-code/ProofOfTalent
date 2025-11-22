"""
UK Global Talent Visa Evidence Analysis System
Uses LLM (GPT-4) to evaluate candidate evidence against official visa criteria
"""

import re
import json
import os
from datetime import datetime, timedelta, UTC
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urlparse

# PDF parsing
import pdfplumber

# spaCy for NLP
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except:
    print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")
    nlp = None

# OpenAI
from openai import OpenAI

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    print("Warning: OPENAI_API_KEY not set. LLM analysis will be disabled.")
    client = None

# -------------------------------
# Global Talent Visa Fields
# -------------------------------
GLOBAL_TALENT_FIELDS = {
    'digital_technology': 'Digital Technology',
    'arts_culture': 'Arts and Culture',
    'science_research': 'Science and Research'
}

# -------------------------------
# Global Talent Visa Criteria by Field
# -------------------------------
def get_global_talent_criteria(field: str) -> Dict[str, Any]:
    """Return detailed criteria for Global Talent visa by field"""
    
    common_mandatory = {
        'cv': 'Detailed CV showing career history (5+ years for Exceptional Talent, 3+ years for Exceptional Promise)',
        'recommendation_letters': '3 letters from senior professionals/organizations in your field',
        'evidence_portfolio': 'Up to 10 pieces of evidence from the last 5 years'
    }
    
    criteria = {
        'digital_technology': {
            'mandatory_documents': common_mandatory,
            'evidence_categories': {
                'innovation': [
                    'Founded or held senior role in product-led digital tech company',
                    'Worked in new digital field or technology',
                    'Made significant technical, commercial, or entrepreneurial contributions'
                ],
                'recognition': [
                    'Published research or technical documentation',
                    'Industry awards or recognition',
                    'Media coverage in tech publications',
                    'Speaking engagements at prominent tech events',
                    'Published open-source code with significant adoption'
                ]
            },
            'assessment_focus': 'Innovation in digital technology and recognition beyond immediate role'
        },
        'arts_culture': {
            'mandatory_documents': common_mandatory,
            'evidence_categories': {
                'international_recognition': [
                    'International media coverage',
                    'International prizes or awards',
                    'International appearances, exhibitions, or performances'
                ],
                'track_record': [
                    'Substantial record of work in at least 2 countries (Exceptional Talent)',
                    'Developing record in at least 1 country (Exceptional Promise)',
                    'Work presented at major venues or platforms',
                    'Critical acclaim or reviews'
                ]
            },
            'assessment_focus': 'International recognition and sustained artistic contribution'
        },
        'science_research': {
            'mandatory_documents': common_mandatory,
            'evidence_categories': {
                'research_output': [
                    'Peer-reviewed publications in reputable journals',
                    'Citations of your work',
                    'Research grants as PI or Co-I',
                    'Patents or intellectual property'
                ],
                'recognition': [
                    'Academic appointments at leading institutions',
                    'Individual fellowships',
                    'Research prizes or awards',
                    'Invited presentations at major conferences',
                    'Editorial roles or peer review activities'
                ]
            },
            'assessment_focus': 'Research excellence and contribution to advancing the field'
        }
    }
    
    return criteria.get(field, criteria['digital_technology'])

# -------------------------------
# PDF Parsing
# -------------------------------
def parse_pdf_document(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error parsing PDF {file_path}: {e}")
        return ""

# -------------------------------
# URL Detection
# -------------------------------
def extract_urls(text: str) -> Dict[str, Optional[str]]:
    """Extract GitHub and LinkedIn URLs from text"""
    urls = {'github': None, 'linkedin': None}
    
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    found_urls = re.findall(url_pattern, text)
    
    for url in found_urls:
        if 'github.com' in url.lower():
            urls['github'] = url
        elif 'linkedin.com' in url.lower():
            urls['linkedin'] = url
    
    return urls

# -------------------------------
# GitHub Analysis
# -------------------------------
def extract_github_username(url: str) -> Optional[str]:
    """Extract username from GitHub URL"""
    try:
        path = urlparse(url).path.strip('/')
        username = path.split('/')[0]
        return username if username else None
    except:
        return None

def analyze_github_profile(github_url: str) -> Dict[str, Any]:
    """Fetch and analyze GitHub profile data"""
    username = extract_github_username(github_url)
    if not username:
        return {}
    
    headers = {}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    
    try:
        user_response = requests.get(f'https://api.github.com/users/{username}', headers=headers, timeout=10)
        user_data = user_response.json() if user_response.status_code == 200 else {}
        
        repos_response = requests.get(f'https://api.github.com/users/{username}/repos?per_page=100', 
                                      headers=headers, timeout=10)
        repos = repos_response.json() if repos_response.status_code == 200 else []
        
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos if isinstance(repo, dict))
        total_forks = sum(repo.get('forks_count', 0) for repo in repos if isinstance(repo, dict))
        languages = set()
        
        for repo in repos:
            if isinstance(repo, dict) and repo.get('language'):
                languages.add(repo['language'])
        
        return {
            'username': username,
            'public_repos': user_data.get('public_repos', 0),
            'followers': user_data.get('followers', 0),
            'total_stars': total_stars,
            'total_forks': total_forks,
            'languages': list(languages),
            'bio': user_data.get('bio', ''),
            'company': user_data.get('company', ''),
            'location': user_data.get('location', '')
        }
    
    except Exception as e:
        print(f"Error fetching GitHub data: {e}")
        return {}

# -------------------------------
# LinkedIn Analysis (Simplified)
# -------------------------------
def analyze_linkedin_profile(linkedin_url: str) -> Dict[str, Any]:
    """Extract LinkedIn profile info (limited without API access)"""
    return {
        'url': linkedin_url,
        'note': 'Full LinkedIn analysis requires API access or manual data entry'
    }

# -------------------------------
# Evidence Document Parsing
# -------------------------------
def parse_multiple_documents(file_paths: List[str]) -> Dict[str, Any]:
    """Parse multiple evidence documents (CV, letters, portfolio items)"""
    documents = {
        'cv': None,
        'recommendation_letters': [],
        'portfolio_items': []
    }
    
    for path in file_paths:
        text = parse_pdf_document(path)
        filename = os.path.basename(path).lower()
        
        # Classify document type based on filename or content
        if 'cv' in filename or 'resume' in filename:
            documents['cv'] = {'path': path, 'text': text}
        elif 'letter' in filename or 'recommendation' in filename:
            documents['recommendation_letters'].append({'path': path, 'text': text})
        else:
            documents['portfolio_items'].append({'path': path, 'text': text})
    
    return documents

if __name__ == "__main__":
    print("Global Talent Visa Analysis System")
    print("Fields supported:", list(GLOBAL_TALENT_FIELDS.values()))
