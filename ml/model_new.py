"""
UK Global Talent Visa Evidence Analysis System
Simplified version focused exclusively on UK Global Talent visa using LLM (GPT-4)
Removes all ML models and other visa types
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


def get_global_talent_criteria(field: str) -> Dict[str, Any]:
    """Return detailed criteria for Global Talent visa by field
    
    Based on official UK government guidance for the Global Talent visa endorsement requirements.
    """
    
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
                    'Published open-source code with significant adoption',
                    'Significant contributions to open-source projects'
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
# Interactive Questionnaire
# -------------------------------
def generate_evidence_questionnaire(field: str) -> List[Dict[str, Any]]:
    """Generate interactive questionnaire based on field to gather evidence information
    
    Returns list of questions with type (text, number, yes/no, multiple_choice, file_upload)
    """
    common_questions = [
        {
            'id': 'years_experience',
            'question': 'How many years of professional experience do you have in your field?',
            'type': 'number',
            'required': True
        },
        {
            'id': 'cv_uploaded',
            'question': 'Upload your CV/Resume (PDF format)',
            'type': 'file_upload',
            'required': True,
            'file_types': ['pdf']
        },
        {
            'id': 'recommendation_letters',
            'question': 'Upload up to 3 recommendation letters (PDF format)',
            'type': 'file_upload_multiple',
            'required': True,
            'min_files': 3,
            'max_files': 3,
            'file_types': ['pdf']
        }
    ]
    
    field_specific = {
        'digital_technology': [
            {
                'id': 'github_url',
                'question': 'GitHub profile URL (if applicable)',
                'type': 'text',
                'required': False
            },
            {
                'id': 'has_founded_company',
                'question': 'Have you founded or held a senior role in a product-led digital technology company?',
                'type': 'yes_no',
                'required': True
            },
            {
                'id': 'publications',
                'question': 'Number of technical publications, research papers, or significant blog posts',
                'type': 'number',
                'required': True
            },
            {
                'id': 'speaking_engagements',
                'question': 'Have you spoken at prominent tech conferences or events?',
                'type': 'yes_no',
                'required': True
            },
            {
                'id': 'awards',
                'question': 'List any industry awards or recognition you have received',
                'type': 'text',
                'required': False
            },
           {
                'id': 'open_source',
                'question': 'Do you have significant open-source contributions? (provide GitHub stars/forks if applicable)',
                'type': 'text',
                'required': False
            }
        ],
        'arts_culture': [
            {
                'id': 'countries_worked',
                'question': 'How many countries have you worked or exhibited in?',
                'type': 'number',
                'required': True
            },
            {
                'id': 'international_prizes',
                'question': 'List any international prizes or awards',
                'type': 'text',
                'required': False
            },
            {
                'id': 'media_coverage',
                'question': 'Have you received international media coverage?',
                'type': 'yes_no',
                'required': True
            },
            {
                'id': 'major_venues',
                'question': 'List major venues or platforms where your work has been presented',
                'type': 'text',
                'required': False
            }
        ],
        'science_research': [
            {
                'id': 'peer_reviewed_pubs',
                'question': 'Number of peer-reviewed publications',
                'type': 'number',
                'required': True
            },
            {
                'id': 'citations',
                'question': 'Approximate number of citations of your work',
                'type': 'number',
                'required': False
            },
            {
                'id': 'research_grants',
                'question': 'Have you been PI or Co-I on research grants?',
                'type': 'yes_no',
                'required': True
            },
            {
                'id': 'academic_position',
                'question': 'Do you hold an academic position at a leading institution?',
                'type': 'yes_no',
                'required': True
            },
            {
                'id': 'fellowships',
                'question': 'List any individual fellowships or research prizes',
                'type': 'text',
                'required': False
            }
        ]
    }
    
    return common_questions + field_specific.get(field, [])


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


def parse_multiple_documents(file_paths: List[str]) -> Dict[str, Any]:
    """Parse multiple evidence documents (CV, letters, portfolio items)
    
    Automatically classifies documents based on filename patterns
    """
    documents = {
        'cv': None,
        'recommendation_letters': [],
        'portfolio_items': []
    }
    
    for path in file_paths:
        if not os.path.exists(path):
            print(f"Warning: File not found: {path}")
            continue
            
        text = parse_pdf_document(path)
        filename = os.path.basename(path).lower()
        
        # Classify document type based on filename
        if 'cv' in filename or 'resume' in filename:
            documents['cv'] = {'path': path, 'text': text, 'filename': os.path.basename(path)}
        elif 'letter' in filename or 'recommendation' in filename or 'reference' in filename:
            documents['recommendation_letters'].append({
                'path': path,
                'text': text,
                'filename': os.path.basename(path)
            })
        else:
            # Portfolio items: publications, awards, media coverage, etc.
            documents['portfolio_items'].append({
                'path': path,
                'text': text,
                'filename': os.path.basename(path)
            })
    
    return documents


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


def analyze_linkedin_profile(linkedin_url: str) -> Dict[str, Any]:
    """Extract LinkedIn profile info (limited without API access)"""
    return {
        'url': linkedin_url,
        'note': 'Full LinkedIn analysis requires API access or manual data entry'
    }


if __name__ == "__main__":
    print("UK Global Talent Visa Analysis System")
    print("Supported fields:", list(GLOBAL_TALENT_FIELDS.values()))
    
    # Example: generate questionnaire for digital technology
    questions = generate_evidence_questionnaire('digital_technology')
    print(f"\nQuestionnaire has {len(questions)} questions")
