import re
import json
import os
from datetime import datetime, timedelta, UTC
from typing import List, Dict, Any, Optional
import requests
from urllib.parse import urlparse

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

# ML libs
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except Exception:
    XGBOOST_AVAILABLE = False

# spaCy + PDF
import spacy
import pdfplumber

try:
    nlp = spacy.load("en_core_web_sm")
except:
    print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")
    nlp = None

# OpenAI
from openai import OpenAI

# API Keys from environment
from dotenv import load_dotenv
load_dotenv()
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Optional, increases rate limit
LINKEDIN_API_KEY = os.getenv("LINKEDIN_API_KEY")  # If using official API

if OPENAI_API_KEY:
 client = OpenAI(api_key=OPENAI_API_KEY)
else:
    print("Warning: OPENAI_API_KEY not set. Roadmap generation will be disabled.")
    client = None


# -------------------------------
# Comprehensive Skill Bank (multi-domain)
# -------------------------------
SKILL_BANK = {
    'tech': ['python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue', 'node.js', 
             'django', 'flask', 'spring boot', 'machine learning', 'deep learning', 'nlp', 
             'computer vision', 'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'sql', 'nosql',
             'mongodb', 'postgresql', 'mysql', 'redis', 'aws', 'azure', 'gcp', 'docker', 
             'kubernetes', 'ci/cd', 'git', 'rest api', 'graphql', 'microservices', 'agile',
             'next.js', 'tailwind', 'data science', 'software engineering', 'devops', 'cloud'],
    'finance': ['accounting', 'financial analysis', 'investment banking', 'portfolio management',
                'risk management', 'financial modeling', 'excel', 'bloomberg', 'cfa', 'frm',
                'derivatives', 'equity research', 'treasury', 'compliance', 'audit', 'tax'],
    'healthcare': ['nursing', 'patient care', 'clinical research', 'medical coding', 'emr/ehr',
                   'healthcare administration', 'pharmacology', 'surgery', 'diagnostics'],
    'marketing': ['digital marketing', 'seo', 'sem', 'content marketing', 'social media',
                  'google analytics', 'email marketing', 'brand management', 'market research'],
    'design': ['ui/ux', 'graphic design', 'adobe creative suite', 'figma', 'sketch', 
               'photoshop', 'illustrator', 'branding', 'web design', 'product design'],
    'business': ['project management', 'pmp', 'scrum', 'product management', 'business analysis',
                 'strategy consulting', 'operations', 'supply chain', 'sales', 'crm'],
    'education': ['teaching', 'curriculum development', 'instructional design', 'e-learning',
                  'educational technology', 'student assessment', 'classroom management'],
    'legal': ['contract law', 'corporate law', 'litigation', 'legal research', 'compliance',
              'intellectual property', 'regulatory affairs', 'legal writing'],
    'engineering': ['mechanical engineering', 'civil engineering', 'electrical engineering',
                    'chemical engineering', 'cad', 'autocad', 'solidworks', 'project engineering']
}

ALL_SKILLS = [skill for category in SKILL_BANK.values() for skill in category]

VISAS = ['uk_global_talent', 'uk_skilled_worker', 'canada_express_entry', 'us_h1b', 'australia_skilled']

# -------------------------------
# URL Detection
# -------------------------------
def extract_urls(text: str) -> Dict[str, Optional[str]]:
    """Extract GitHub and LinkedIn URLs from text"""
    urls = {'github': None, 'linkedin': None}
    
    # Find all URLs
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
        # Fetch user info
        user_response = requests.get(f'https://api.github.com/users/{username}', headers=headers, timeout=10)
        user_data = user_response.json() if user_response.status_code == 200 else {}
        
        # Fetch repositories
        repos_response = requests.get(f'https://api.github.com/users/{username}/repos?per_page=100', 
                                      headers=headers, timeout=10)
        repos = repos_response.json() if repos_response.status_code == 200 else []
        
        # Extract features
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos if isinstance(repo, dict))
        total_forks = sum(repo.get('forks_count', 0) for repo in repos if isinstance(repo, dict))
        languages = set()
        recent_activity = []
        
        for repo in repos:
            if isinstance(repo, dict):
                if repo.get('language'):
                    languages.add(repo['language'])
                if repo.get('updated_at'):
                    recent_activity.append(repo['updated_at'])
        
        # Calculate portfolio quality score
        portfolio_score = min(100, (
            total_stars * 2 +
            total_forks * 1.5 +
            len(repos) * 5 +
            len(languages) * 10 +
            (user_data.get('followers', 0) * 1)
        ) / 10)
        
        # Calculate days since last activity
        days_since_last_commit = 365  # default
        if recent_activity:
            try:
                latest = max(datetime.fromisoformat(date.replace('Z', '+00:00')) for date in recent_activity)
                days_since_last_commit = (datetime.now(UTC) - latest).days
            except:
                pass
        
        return {
            'num_repos': len(repos),
            'github_stars': total_stars,
            'github_forks': total_forks,
            'github_languages': list(languages),
            'num_languages': len(languages),
            'github_followers': user_data.get('followers', 0),
            'github_following': user_data.get('following', 0),
            'portfolio_quality_score': portfolio_score,
            'days_since_last_commit': days_since_last_commit,
            'is_active': days_since_last_commit < 90
        }
    except Exception as e:
        print(f"Error fetching GitHub data for {username}: {e}")
        return {}

# -------------------------------
# LinkedIn Analysis (Simulated)
# -------------------------------
def analyze_linkedin_profile(linkedin_url: str) -> Dict[str, Any]:
    """
    Analyze LinkedIn profile. 
    Note: Real LinkedIn scraping requires authentication and is against their ToS.
    This is a placeholder that would need proper LinkedIn API integration.
    """
    # In production, you would use LinkedIn API with proper OAuth
    # For now, returning simulated data structure
    
    print(f"Note: LinkedIn analysis requires official API integration. URL found: {linkedin_url}")
    
    # Placeholder: In real implementation, fetch actual data
    return {
        'num_roles_linkedin': 0,  # Would be populated from API
        'num_skills_linkedin': 0,
        'endorsement_score': 0,
        'num_recommendations': 0,
        'num_connections': 0,
        'linkedin_data_available': False
    }

# -------------------------------
# PDF Parsing
# -------------------------------
def parse_pdf_cv(file_path: str) -> str:
    """Extract text from PDF CV"""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error parsing PDF {file_path}: {e}")
    return text

def extract_skills(text: str) -> List[str]:
    """Extract skills from text based on comprehensive skill bank"""
    text_lower = text.lower()
    found_skills = []
    for skill in ALL_SKILLS:
        # Use word boundaries for better matching
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
    return found_skills

def extract_years_of_experience(text: str) -> float:
    """Extract years of experience from text"""
    # Look for patterns like "5 years", "3+ years", "2-4 years"
    patterns = [
        r'(\d+)[\+\-\s]*(?:years?|yrs?)[\s]+(?:of\s+)?experience',
        r'experience[:\s]+(\d+)[\+\-\s]*(?:years?|yrs?)',
        r'(\d+)[\+\-\s]*(?:years?|yrs?)[\s]+in'
    ]
    
    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        years.extend([float(m) for m in matches])
    
    return max(years) if years else 1.0  # Default to 1 year if not found

def extract_education_level(text: str) -> str:
    """Extract highest education level"""
    text_lower = text.lower()
    
    if any(term in text_lower for term in ['phd', 'ph.d', 'doctorate', 'doctoral']):
        return 'phd'
    elif any(term in text_lower for term in ['master', 'msc', 'm.sc', 'ma', 'm.a', 'mba', 'meng','MSc']):
        return 'masters'
    elif any(term in text_lower for term in ['bachelor', 'bsc', 'b.sc', 'ba', 'b.a', 'beng', 'degree','BSc']):
        return 'bachelors'
    else:
        return 'other'

def parse_cv(text: str) -> Dict[str, Any]:
    """Parse CV text and extract structured information"""
    # Extract URLs first
    urls = extract_urls(text)
    
    parsed = {
        'skills': extract_skills(text),
        'roles': [],
        'education': [],
        'certifications': [],
        'projects': [],
        'publications': [],
        'awards': [],
        'languages': [],
        'urls': urls
    }
    
    # Use spaCy if available
    if nlp:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "ORG":
                parsed['roles'].append(ent.text)
            elif ent.label_ == "PERSON":
                pass  # Skip person names for privacy
            elif ent.label_ == "DATE":
                pass  # Could use for experience calculation
    
    # Extract various sections
    lines = text.split("\n")
    for line in lines:
        line_lower = line.lower()
        
        if any(keyword in line_lower for keyword in ['project', 'portfolio']):
            if len(line.strip()) > 10:
                parsed['projects'].append(line.strip())
        
        if any(keyword in line_lower for keyword in ['publication', 'paper', 'journal', 'conference']):
            if len(line.strip()) > 10:
                parsed['publications'].append(line.strip())
        
        if any(keyword in line_lower for keyword in ['award', 'honor', 'prize', 'recognition']):
            if len(line.strip()) > 10:
                parsed['awards'].append(line.strip())
        
        if any(keyword in line_lower for keyword in ['certification', 'certified', 'certificate']):
            if len(line.strip()) > 10:
                parsed['certifications'].append(line.strip())
        
        if any(keyword in line_lower for keyword in ['language', 'fluent', 'proficient']):
            if len(line.strip()) > 5:
                parsed['languages'].append(line.strip())
    
    # Extract numeric features
    parsed['years_experience'] = extract_years_of_experience(text)
    parsed['num_projects'] = len(parsed['projects'])
    parsed['education_level'] = extract_education_level(text)
    
    return parsed

# -------------------------------
# Feature Engineering
# -------------------------------
def build_comprehensive_features(parsed: Dict[str, Any], 
                                github_data: Dict[str, Any], 
                                linkedin_data: Dict[str, Any]) -> Dict[str, Any]:
    """Build comprehensive feature set from all sources"""
    
    feats = {}
    
    # CV features
    feats['years_experience'] = parsed.get('years_experience', 0.0)
    feats['num_projects'] = parsed.get('num_projects', 0)
    feats['num_skills_cv'] = len(parsed.get('skills', []))
    feats['num_publications'] = len(parsed.get('publications', []))
    feats['num_awards'] = len(parsed.get('awards', []))
    feats['num_certifications'] = len(parsed.get('certifications', []))
    feats['num_languages'] = len(parsed.get('languages', []))
    
    # Education encoding
    edu_level = parsed.get('education_level', 'other')
    feats['education_phd'] = 1 if edu_level == 'phd' else 0
    feats['education_masters'] = 1 if edu_level == 'masters' else 0
    feats['education_bachelors'] = 1 if edu_level == 'bachelors' else 0
    
    # GitHub features (tech candidates)
    feats['github_stars'] = github_data.get('github_stars', 0)
    feats['github_repos'] = github_data.get('num_repos', 0)
    feats['github_languages'] = github_data.get('num_languages', 0)
    feats['github_followers'] = github_data.get('github_followers', 0)
    feats['portfolio_quality_score'] = github_data.get('portfolio_quality_score', 0)
    feats['github_active'] = 1 if github_data.get('is_active', False) else 0
    
    # LinkedIn features (all candidates)
    feats['linkedin_roles'] = linkedin_data.get('num_roles_linkedin', 0)
    feats['linkedin_skills'] = linkedin_data.get('num_skills_linkedin', 0)
    feats['endorsement_score'] = linkedin_data.get('endorsement_score', 0)
    feats['num_recommendations'] = linkedin_data.get('num_recommendations', 0)
    feats['linkedin_connections'] = linkedin_data.get('num_connections', 0)
    
    # Combined features
    feats['total_skills'] = feats['num_skills_cv'] + feats['linkedin_skills']
    feats['total_projects'] = feats['num_projects'] + feats['github_repos']
    
    # Public presence score
    feats['public_presence'] = min(100, (
        feats['num_publications'] * 20 +
        feats['num_awards'] * 15 +
        feats['github_stars'] * 0.5 +
        feats['github_followers'] * 1 +
        feats['num_recommendations'] * 10
    ))
    
    return feats

# -------------------------------
# Visa Gap Analysis
# -------------------------------
def find_gaps(features: Dict[str, Any], visa: str) -> List[Dict[str, Any]]:
    """Identify gaps for specific visa requirements"""
    gaps = []
    
    if visa == 'uk_global_talent':
        if features.get('years_experience', 0) < 3:
            gaps.append({'type': 'experience_years', 'current': features.get('years_experience', 0), 'needed': 3})
        if features.get('num_awards', 0) < 1:
            gaps.append({'type': 'awards', 'current': features.get('num_awards', 0), 'needed': 1})
        if features.get('num_publications', 0) < 2:
            gaps.append({'type': 'publications', 'current': features.get('num_publications', 0), 'needed': 2})
        gaps.append({'type': 'recommendation_letters', 'current': 0, 'needed': 3})
        if features.get('public_presence', 0) < 50:
            gaps.append({'type': 'public_presence', 'current': features.get('public_presence', 0), 'needed': 50})
            
    elif visa == 'uk_skilled_worker':
        if features.get('years_experience', 0) < 1:
            gaps.append({'type': 'experience_years', 'current': features.get('years_experience', 0), 'needed': 1})
        if features.get('total_skills', 0) < 5:
            gaps.append({'type': 'skills', 'current': features.get('total_skills', 0), 'needed': 5})
            
    elif visa == 'canada_express_entry':
        if features.get('years_experience', 0) < 1:
            gaps.append({'type': 'experience_years', 'current': features.get('years_experience', 0), 'needed': 1})
        if features.get('education_bachelors', 0) == 0:
            gaps.append({'type': 'education', 'current': 'none', 'needed': 'bachelors'})
        if features.get('num_certifications', 0) < 1:
            gaps.append({'type': 'certifications', 'current': features.get('num_certifications', 0), 'needed': 1})
            
    elif visa == 'us_h1b':
        if features.get('years_experience', 0) < 2:
            gaps.append({'type': 'experience_years', 'current': features.get('years_experience', 0), 'needed': 2})
        if features.get('education_bachelors', 0) == 0:
            gaps.append({'type': 'education', 'current': 'none', 'needed': 'bachelors'})
            
    elif visa == 'australia_skilled':
        if features.get('years_experience', 0) < 3:
            gaps.append({'type': 'experience_years', 'current': features.get('years_experience', 0), 'needed': 3})
        if features.get('total_skills', 0) < 8:
            gaps.append({'type': 'skills', 'current': features.get('total_skills', 0), 'needed': 8})
        if features.get('num_certifications', 0) < 1:
            gaps.append({'type': 'certifications', 'current': features.get('num_certifications', 0), 'needed': 1})
    
    return gaps

# -------------------------------
# ML Model Training
# -------------------------------
def train_visa_models(training_data: pd.DataFrame) -> Dict[str, Any]:
    """Train separate models for each visa type"""
    models = {}
    
    feature_cols = [
        'years_experience', 'num_projects', 'num_publications', 'num_awards',
        'github_stars', 'portfolio_quality_score', 'endorsement_score',
        'public_presence', 'education_phd', 'education_masters', 'total_skills'
    ]
    
    for visa in VISAS:
        # Filter data for this visa (in real scenario, you'd have labeled data per visa)
        X = training_data[feature_cols].fillna(0)
        y = training_data[f'{visa}_approved']  # Assumes you have this column
        
        if len(X) < 10:  # Skip if insufficient data
            continue
        
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)
        
        # Train model
        if XGBOOST_AVAILABLE:
            model = xgb.XGBClassifier(
                use_label_encoder=False,
                eval_metric='logloss',
                n_estimators=100,
                max_depth=4,
                learning_rate=0.1
            )
            model.fit(X_train_scaled, y_train)
        else:
            from sklearn.ensemble import RandomForestClassifier
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = model.predict_proba(X_val_scaled)[:, 1]
        auc = roc_auc_score(y_val, y_pred)
        
        models[visa] = {
            'model': model,
            'scaler': scaler,
            'feature_cols': feature_cols,
            'auc': auc,
            'feature_importances': dict(zip(feature_cols, model.feature_importances_))
        }
    
    return models

# -------------------------------
# Roadmap Generation
# -------------------------------
def generate_roadmap_openai(features: Dict[str, Any], gaps: List[Dict[str, Any]], 
                           visa: str, time_left_weeks: int) -> Dict[str, Any]:
    """Generate actionable roadmap using OpenAI"""
    if not client:
        return {
            "milestones": [],
            "total_weeks": 0,
            "feasibility_comment": "Roadmap generation unavailable (OpenAI API key not set)"
        }
    
    prompt = f"""
You are an expert immigration advisor. Generate a detailed, actionable roadmap in JSON format for the {visa.replace('_', ' ').title()} visa.

Current Profile Features: {json.dumps(features, indent=2)}
Identified Gaps: {json.dumps(gaps, indent=2)}
Available Time (weeks): {time_left_weeks}

Create a realistic, step-by-step roadmap with specific milestones. Each milestone should:
- Address one or more gaps
- Include concrete actions
- Specify evidence to collect
- Estimate duration realistically

Output ONLY valid JSON with this exact structure:
{{
    "milestones": [
        {{
            "title": "Milestone title",
            "description": "Detailed actions to take",
            "duration_weeks": integer,
            "evidence_items": ["specific evidence 1", "specific evidence 2"],
            "addresses_gaps": ["gap type 1", "gap type 2"]
        }}
    ],
    "total_weeks": integer,
    "feasibility_comment": "Brief assessment of feasibility given available time"
}}
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean markdown code blocks
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        return json.loads(content)
    
    except Exception as e:
        print(f"Error generating roadmap: {e}")
        return {
            "milestones": [{
                "title": "Review visa requirements",
                "description": "Study official requirements and gather initial documentation",
                "duration_weeks": 2,
                "evidence_items": ["Requirements checklist"],
                "addresses_gaps": []
            }],
            "total_weeks": 2,
            "feasibility_comment": f"Error generating detailed roadmap: {str(e)}"
        }

def estimate_timeline(roadmap: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate timeline from roadmap"""
    total_weeks = roadmap.get('total_weeks', 0)
    if total_weeks == 0:
        total_weeks = sum(m.get('duration_weeks', 0) for m in roadmap.get('milestones', []))
    
    completion_date = datetime.now(UTC) + timedelta(weeks=total_weeks)
    
    return {
        'projected_completion_weeks': total_weeks,
        'projected_completion_date': completion_date.strftime('%Y-%m-%d'),
        'start_date': datetime.now(UTC).strftime('%Y-%m-%d'),
        'is_feasible': total_weeks <= 52  # Within one year
    }

# -------------------------------
# Complete Analysis Pipeline
# -------------------------------
def analyze_candidate_comprehensive(parsed: Dict[str, Any], models: Dict[str, Any]) -> Dict[str, Any]:
    """Run complete analysis for all visa types"""
    
    # Fetch external data
    urls = parsed.get('urls', {})
    github_data = analyze_github_profile(urls['github']) if urls.get('github') else {}
    linkedin_data = analyze_linkedin_profile(urls['linkedin']) if urls.get('linkedin') else {}
    
    # Build features
    features = build_comprehensive_features(parsed, github_data, linkedin_data)
    
    # Analyze each visa
    visa_analysis = {}
    
    for visa in VISAS:
        # Get model if available
        visa_model = models.get(visa)
        
        # Calculate ML-based likelihood
        if visa_model:
            feature_cols = visa_model['feature_cols']
            X_input = np.array([[features.get(col, 0) for col in feature_cols]])
            X_scaled = visa_model['scaler'].transform(X_input)
            base_likelihood = float(visa_model['model'].predict_proba(X_scaled)[0, 1])
        else:
            # Fallback heuristic if no model
            base_likelihood = min(1.0, (
                features.get('years_experience', 0) * 0.1 +
                features.get('public_presence', 0) * 0.005 +
                features.get('total_skills', 0) * 0.02
            ))
        
        # Find gaps
        gaps = find_gaps(features, visa)
        
        # Apply penalty for gaps
        penalty = min(0.5, len(gaps) * 0.08)
        likelihood = max(0, base_likelihood - penalty)
        
        # Generate roadmap
        roadmap = generate_roadmap_openai(features, gaps, visa, time_left_weeks=40)
        
        # Calculate timeline
        timeline = estimate_timeline(roadmap)
        
        visa_analysis[visa] = {
            'likelihood': round(likelihood, 4),
            'confidence': 'high' if visa_model else 'low',
            'gaps_identified': gaps,
            'roadmap': roadmap,
            'timeline': timeline,
            'recommendation': 'highly_recommended' if likelihood > 0.7 else 'recommended' if likelihood > 0.5 else 'challenging'
        }
    
    return {
        'parsed': parsed,
        'external_data': {
            'github': github_data,
            'linkedin': linkedin_data
        },
        'features': features,
        'visa_analysis': visa_analysis
    }

# -------------------------------
# Batch Processing
# -------------------------------
def process_cv_file(file_path: str, models: Dict[str, Any]) -> Dict[str, Any]:
    """Process single CV file"""
    text = parse_pdf_cv(file_path)
    parsed = parse_cv(text)
    result = analyze_candidate_comprehensive(parsed, models)
    result['source_file'] = file_path
    return result

def process_all_cvs(folder_path: str, models: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Process all CVs in folder"""
    results = []
    
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} not found")
        return results
    
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    for i, filename in enumerate(pdf_files, 1):
        print(f"Processing {i}/{len(pdf_files)}: {filename}")
        file_path = os.path.join(folder_path, filename)
        try:
            result = process_cv_file(file_path, models)
            results.append(result)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    return results

# -------------------------------
# Generate Synthetic Training Data
# -------------------------------
def generate_synthetic_training_data(n_samples: int = 500) -> pd.DataFrame:
    """Generate synthetic training data for model development"""
    np.random.seed(42)
    
    data = []
    for _ in range(n_samples):
        # Generate correlated features
        years_exp = np.random.uniform(0.5, 15)
        education = np.random.choice(['bachelors', 'masters', 'phd'], p=[0.5, 0.35, 0.15])
        
        base_score = years_exp * 10 + (30 if education == 'phd' else 20 if education == 'masters' else 10)
        
        row = {
            'years_experience': years_exp,
            'num_projects': int(np.random.poisson(years_exp * 0.8)),
            'num_publications': int(np.random.poisson(years_exp * 0.3)) if education != 'bachelors' else 0,
            'num_awards': int(np.random.poisson(0.5)),
            'github_stars': int(np.random.exponential(50)) if np.random.rand() > 0.3 else 0,
            'portfolio_quality_score': min(100, np.random.normal(base_score, 20)),
            'endorsement_score': int(np.random.normal(years_exp * 5, 10)),
            'public_presence': min(100, np.random.normal(base_score, 15)),
            'education_phd': 1 if education == 'phd' else 0,
            'education_masters': 1 if education == 'masters' else 0,
            'total_skills': int(np.random.normal(8, 3))
        }
        
        # Generate visa approval labels based on features (synthetic logic)
        for visa in VISAS:
            if visa == 'uk_global_talent':
                prob = min(0.95, (row['years_experience'] / 10 + row['num_publications'] * 0.1 + 
                          row['num_awards'] * 0.15 + row['public_presence'] * 0.005))
            elif visa == 'uk_skilled_worker':
                prob = min(0.95, (row['years_experience'] / 5 + row['total_skills'] * 0.05))
            elif visa == 'canada_express_entry':
                prob = min(0.95, (row['years_experience'] / 8 + row['education_phd'] * 0.3 + 
                          row['education_masters'] * 0.2 + row['total_skills'] * 0.03))
            elif visa == 'us_h1b':
                prob = min(0.95, (row['years_experience'] / 6 + 
                          (row['education_phd'] + row['education_masters']) * 0.25))
            else:  # australia_skilled
                prob = min(0.95, (row['years_experience'] / 7 + row['total_skills'] * 0.04 + 
                          row['education_masters'] * 0.15))
            
            row[f'{visa}_approved'] = 1 if np.random.rand() < prob else 0
        
        data.append(row)
    
    return pd.DataFrame(data)

# -------------------------------
# Main Execution
# -------------------------------
def main(folder_path: str = "uploaded_cvs", output_file: str = "cv_analysis_results.json"):
    """Main execution pipeline"""
    
    print("=" * 80)
    print("COMPREHENSIVE CV ANALYSIS SYSTEM")
    print("Multi-Domain | GitHub + LinkedIn Integration | ML-Powered Predictions")
    print("=" * 80)
    
    # Step 1: Generate/Load training data
    print("\n[1/4] Generating synthetic training data...")
    training_data = generate_synthetic_training_data(n_samples=500)
    print(f"✓ Generated {len(training_data)} training samples")
    
    # Step 2: Train models
    print("\n[2/4] Training ML models for each visa type...")
    models = train_visa_models(training_data)
    print(f"✓ Trained {len(models)} visa-specific models")
    for visa, model_info in models.items():
        print(f"  - {visa}: AUC = {model_info['auc']:.4f}")
    
    # Step 3: Process CVs
    print(f"\n[3/4] Processing CVs from folder: {folder_path}")
    results = process_all_cvs(folder_path, models)
    print(f"✓ Processed {len(results)} CVs successfully")
    
    # Step 4: Save results
    print(f"\n[4/4] Saving results to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ Results saved successfully")
    
    # Display summary
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    
    if results:
        for i, result in enumerate(results[:3], 1):  # Show first 3
            print(f"\n--- Candidate {i}: {result.get('source_file', 'Unknown')} ---")
            
            features = result.get('features', {})
            print(f"Experience: {features.get('years_experience', 0):.1f} years")
            print(f"Skills: {features.get('total_skills', 0)}")
            print(f"Projects: {features.get('total_projects', 0)}")
            print(f"Publications: {features.get('num_publications', 0)}")
            print(f"GitHub Stars: {features.get('github_stars', 0)}")
            
            print("\nVisa Recommendations:")
            visa_analysis = result.get('visa_analysis', {})
            
            # Sort by likelihood
            sorted_visas = sorted(visa_analysis.items(), 
                                 key=lambda x: x[1].get('likelihood', 0), 
                                 reverse=True)
            
            for visa, data in sorted_visas:
                likelihood = data.get('likelihood', 0)
                recommendation = data.get('recommendation', 'unknown')
                gaps = len(data.get('gaps_identified', []))
                weeks = data.get('timeline', {}).get('projected_completion_weeks', 0)
                
                status = "✓" if likelihood > 0.7 else "○" if likelihood > 0.5 else "✗"
                print(f"  {status} {visa.replace('_', ' ').title():30} | "
                      f"Likelihood: {likelihood:.2%} | "
                      f"Gaps: {gaps} | "
                      f"Timeline: {weeks}w")
        
        if len(results) > 3:
            print(f"\n... and {len(results) - 3} more candidates")
    
    print("\n" + "=" * 80)
    print(f"✓ Complete! Full analysis available in {output_file}")
    print("=" * 80)
    
    return results

# -------------------------------
# Utility Functions
# -------------------------------
def view_detailed_report(results: List[Dict[str, Any]], candidate_index: int = 0):
    """View detailed report for a specific candidate"""
    if not results or candidate_index >= len(results):
        print("No results available or invalid index")
        return
    
    result = results[candidate_index]
    
    print("\n" + "=" * 80)
    print(f"DETAILED REPORT - Candidate {candidate_index + 1}")
    print("=" * 80)
    
    # Profile Summary
    print("\n### PROFILE SUMMARY ###")
    features = result.get('features', {})
    for key, value in features.items():
        if isinstance(value, float):
            print(f"{key:30}: {value:.2f}")
        else:
            print(f"{key:30}: {value}")
    
    # External Data
    print("\n### EXTERNAL PROFILES ###")
    external = result.get('external_data', {})
    github = external.get('github', {})
    linkedin = external.get('linkedin', {})
    
    if github:
        print("\nGitHub:")
        for key, value in github.items():
            if key != 'github_languages':
                print(f"  {key}: {value}")
    
    if linkedin.get('linkedin_data_available'):
        print("\nLinkedIn:")
        for key, value in linkedin.items():
            print(f"  {key}: {value}")
    
    # Visa Analysis
    print("\n### VISA ANALYSIS ###")
    visa_analysis = result.get('visa_analysis', {})
    
    for visa, data in visa_analysis.items():
        print(f"\n{visa.replace('_', ' ').title().upper()}")
        print("-" * 40)
        print(f"Likelihood: {data.get('likelihood', 0):.2%}")
        print(f"Recommendation: {data.get('recommendation', 'unknown')}")
        print(f"Confidence: {data.get('confidence', 'unknown')}")
        
        gaps = data.get('gaps_identified', [])
        if gaps:
            print(f"\nGaps ({len(gaps)}):")
            for gap in gaps:
                print(f"  - {gap['type']}: Current={gap.get('current', 'N/A')}, Needed={gap.get('needed', 'N/A')}")
        
        timeline = data.get('timeline', {})
        print(f"\nTimeline:")
        print(f"  Completion: {timeline.get('projected_completion_weeks', 0)} weeks")
        print(f"  Target Date: {timeline.get('projected_completion_date', 'N/A')}")
        print(f"  Feasible: {'Yes' if timeline.get('is_feasible', False) else 'No'}")
        
        roadmap = data.get('roadmap', {})
        milestones = roadmap.get('milestones', [])
        if milestones:
            print(f"\nRoadmap ({len(milestones)} milestones):")
            for i, milestone in enumerate(milestones, 1):
                print(f"  {i}. {milestone.get('title', 'Unknown')} ({milestone.get('duration_weeks', 0)}w)")
                print(f"     {milestone.get('description', 'No description')}")

def compare_candidates(results: List[Dict[str, Any]], visa_type: str = 'uk_global_talent'):
    """Compare multiple candidates for a specific visa"""
    if not results:
        print("No results to compare")
        return
    
    print(f"\n{'='*80}")
    print(f"CANDIDATE COMPARISON - {visa_type.replace('_', ' ').title()}")
    print('='*80)
    
    comparison_data = []
    for i, result in enumerate(results):
        visa_data = result.get('visa_analysis', {}).get(visa_type, {})
        features = result.get('features', {})
        
        comparison_data.append({
            'index': i,
            'file': result.get('source_file', 'Unknown'),
            'likelihood': visa_data.get('likelihood', 0),
            'experience': features.get('years_experience', 0),
            'skills': features.get('total_skills', 0),
            'gaps': len(visa_data.get('gaps_identified', [])),
            'weeks': visa_data.get('timeline', {}).get('projected_completion_weeks', 0)
        })
    
    # Sort by likelihood
    comparison_data.sort(key=lambda x: x['likelihood'], reverse=True)
    
    # Print table
    print(f"\n{'Rank':<6}{'Candidate':<30}{'Likelihood':<12}{'Experience':<12}{'Skills':<8}{'Gaps':<8}{'Timeline'}")
    print('-' * 90)
    
    for rank, candidate in enumerate(comparison_data, 1):
        print(f"{rank:<6}"
              f"{candidate['file'][:28]:<30}"
              f"{candidate['likelihood']:.2%}      "
              f"{candidate['experience']:.1f}y       "
              f"{candidate['skills']:<8}"
              f"{candidate['gaps']:<8}"
              f"{candidate['weeks']}w")
    
    print('='*80)

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == '__main__':
    # Run main pipeline
    results = main(folder_path="uploaded_cvs", output_file="cv_analysis_results.json")
    
    # Optional: View detailed report for first candidate
    if results:
        print("\n" + "="*80)
        print("Press Enter to see detailed report for first candidate...")
        input()
        view_detailed_report(results, candidate_index=0)
        
        print("\n" + "="*80)
        print("Press Enter to see candidate comparison for UK Global Talent...")
        input()
        compare_candidates(results, visa_type='uk_global_talent')