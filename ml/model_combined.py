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
import docx

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
            'question': 'Upload your CV/Resume (PDF or DOCX format)',
            'type': 'file_upload',
            'required': True,
            'file_types': ['pdf', 'docx']
        },
        {
            'id': 'recommendation_letters',
            'question': 'Upload up to 3 recommendation letters (PDF or DOCX format)',
            'type': 'file_upload_multiple',
            'required': True,
            'min_files': 3,
            'max_files': 3,
            'file_types': ['pdf', 'docx']
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
                'id': 'portfolio_url',
                'question': 'Portfolio or personal website URL',
                'type': 'text',
                'required': True,
                'help_text': 'Your portfolio website showcasing your projects, work, and achievements'
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
                'id': 'portfolio_url',
                'question': 'Portfolio, exhibition website, or online gallery URL',
                'type': 'text',
                'required': True,
                'help_text': 'Website showcasing your artistic work, exhibitions, or performances'
            },
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
                'id': 'portfolio_url',
                'question': 'Academic or research profile URL (e.g., personal website, Google Scholar, ResearchGate)',
                'type': 'text',
                'required': False,
                'help_text': 'Link to your academic profile or personal research website'
            },
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


def parse_docx_document(file_path: str) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error parsing DOCX {file_path}: {e}")
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
            
        if path.lower().endswith('.docx'):
            text = parse_docx_document(path)
        else:
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


def analyze_portfolio_website(portfolio_url: str) -> Dict[str, Any]:
    """Fetch and analyze portfolio website content
    
    Args:
        portfolio_url: URL of the portfolio website to analyze
        
    Returns:
        Dict containing portfolio URL and extracted content/metadata
    """
    if not portfolio_url or not portfolio_url.startswith('http'):
        return {
            'error': 'Invalid portfolio URL',
            'url': portfolio_url
        }
    
    try:
        # Fetch portfolio content with timeout
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(portfolio_url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return {
                'url': portfolio_url,
                'error': f'Failed to fetch portfolio (Status: {response.status_code})',
                'accessible': False
            }
        
        # Get raw HTML content
        html_content = response.text
        
        # Basic content extraction (strip HTML tags for simple text analysis)
        # In production, could use BeautifulSoup for better parsing
        import re
        text_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        text_content = re.sub(r'<style[^>]*>.*?</style>', '', text_content, flags=re.DOTALL | re.IGNORECASE)
        text_content = re.sub(r'<[^>]+>', ' ', text_content)
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        
        # Check if we got meaningful content (JavaScript-heavy sites might return very little)
        if len(text_content) < 100 or 'enable JavaScript' in text_content:
            print(f"⚠️  Portfolio appears to be JavaScript-heavy (only {len(text_content)} chars extracted)")
            print("   Attempting to use rendering service...")
            
            # Try using a headless browser rendering service as fallback
            # Using a free public API that renders JavaScript
            try:
                render_url = f"https://r.jina.ai/{portfolio_url}"
                render_response = requests.get(render_url, headers=headers, timeout=20)
                
                if render_response.status_code == 200:
                    rendered_text = render_response.text
                    # Clean up the rendered content
                    rendered_text = re.sub(r'\s+', ' ', rendered_text).strip()
                    
                    if len(rendered_text) > len(text_content):
                        print(f"✅ Successfully rendered JavaScript content ({len(rendered_text)} chars)")
                        text_content = rendered_text
                    else:
                        print("   Rendering service didn't improve results, using original")
                else:
                    print(f"   Rendering service returned status {render_response.status_code}")
            except Exception as render_error:
                print(f"   Rendering service failed: {render_error}")
                print("   Continuing with original extraction...")
        
        # Truncate if too long (keep first 5000 chars for LLM context)
        if len(text_content) > 5000:
            text_content = text_content[:5000] + "... [truncated]"
        
        return {
            'url': portfolio_url,
            'accessible': True,
            'content': text_content,
            'content_length': len(html_content),
            'extracted_text_length': len(text_content)
        }
    
    except requests.exceptions.Timeout:
        return {
            'url': portfolio_url,
            'error': 'Portfolio website request timed out',
            'accessible': False
        }
    except Exception as e:
        return {
            'url': portfolio_url,
            'error': f'Error analyzing portfolio: {str(e)}',
            'accessible': False
        }


if __name__ == "__main__":
    print("UK Global Talent Visa Analysis System")
    print("Supported fields:", list(GLOBAL_TALENT_FIELDS.values()))
    
    # Example: generate questionnaire for digital technology
    questions = generate_evidence_questionnaire('digital_technology')
    print(f"\nQuestionnaire has {len(questions)} questions")
# Add to end of model_new.py - LLM Analysis Functions

# -------------------------------
# LLM-Based Global Talent Evidence Analysis
# -------------------------------
def analyze_evidence_with_llm(
    field: str,
    documents: Dict[str, Any],
    questionnaire_responses: Dict[str, Any],
    github_data: Optional[Dict[str, Any]] = None,
    portfolio_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Main LLM analysis function for Global Talent visa evidence
    
    Uses GPT-4 to evaluate all evidence against field-specific criteria
    Returns likelihood score and detailed gap analysis
    """
    
    if not client:
        return {
            'error': 'OpenAI client not configured. Please set OPENAI_API_KEY.',
            'likelihood': 0.0,
            'gaps': [],
            'recommendation': 'Cannot perform analysis without LLM access'
        }
    
    # Get field-specific criteria
    criteria = get_global_talent_criteria(field)
    
    # Construct comprehensive prompt
    prompt = f"""
You are an expert UK immigration advisor specializing in the Global Talent visa. Your task is to evaluate a candidate's evidence for the {GLOBAL_TALENT_FIELDS[field]} field.

**OFFICIAL VISA CRITERIA:**
{json.dumps(criteria, indent=2)}

**CANDIDATE EVIDENCE:**

1. **CV/Resume:**
{documents.get('cv', {}).get('text', 'NOT PROVIDED')[:3000]}

2. **Recommendation Letters ({len(documents.get('recommendation_letters', []))} provided, 3 required):**
"""
    
    # Add recommendation letter summaries
    for i, letter in enumerate(documents.get('recommendation_letters', []), 1):
        prompt += f"\nLetter {i}: {letter.get('text', '')[:1000]}\n"
    
    prompt += f"""

3. **Portfolio Evidence ({len(documents.get('portfolio_items', []))} items provided, up to 10 allowed):**
"""
    
    for i, item in enumerate(documents.get('portfolio_items', []), 1):
        prompt += f"\nItem {i} ({item.get('filename', 'Unknown')}): {item.get('text', '')[:800]}\n"
    
    prompt += f"""

4. **Questionnaire Responses:**
{json.dumps(questionnaire_responses, indent=2)}
"""
    
    if github_data:
        prompt += f"""

5. **GitHub Profile Data:**
{json.dumps(github_data, indent=2)}
"""
    
    if portfolio_data and portfolio_data.get('accessible'):
        prompt += f"""

6. **Portfolio Website:**
URL: {portfolio_data.get('url')}
Content Preview:
{portfolio_data.get('content', 'No content extracted')[:2500]}
"""
    elif portfolio_data and portfolio_data.get('error'):
        prompt += f"""

6. **Portfolio Website:**
URL: {portfolio_data.get('url')}
Note: Portfolio could not be accessed - {portfolio_data.get('error')}
"""
    
    prompt += """

**YOUR TASK:**
Evaluate this candidate's application against the official Global Talent visa criteria. Provide a detailed, comprehensive assessment in JSON format with the following structure:

{
    "likelihood": <float between 0.0 and 1.0>,
    "assessment_level": "<Exceptional Talent or Exceptional Promise>",
    "evidence_present": {
        "mandatory_documents": {
            "cv": <"complete" or "incomplete" or "missing">,
            "recommendation_letters": <"complete" (3 letters) or "incomplete" (fewer than 3) or "missing">,
            "portfolio_evidence": <"strong" or "adequate" or "weak">
        },
        "innovation_evidence": [<list of identified innovation evidence with details>],
        "recognition_evidence": [<list of identified recognition evidence with details>]
    },
    "portfolio_summary": {
        "accessible": <true/false - was the portfolio successfully accessed>,
        "url": "<portfolio URL if provided>",
        "key_findings": [<list of 3-5 specific projects, achievements, or highlights found on the portfolio>],
        "strengths_from_portfolio": "<paragraph describing what strengths are evident from the portfolio>",
        "gaps_from_portfolio": "<paragraph describing what's missing or could be improved in the portfolio>"
    },
    "cv_feedback": {
        "score": <integer 0-10 representing CV quality for this visa>,
        "strengths": [<list of 4-6 detailed, specific strengths with examples from CV>],
        "weaknesses": [<list of 4-6 detailed, specific weaknesses with examples>],
        "improvement_recommendations": [<list of 3-5 actionable recommendations to improve the CV>]
    },
    "gaps": [
        {
            "type": "<gap type>",
            "severity": "<critical, high, medium, low>",
            "description": "<detailed 2-3 sentence description of what's missing>",
            "recommendation": "<detailed, specific action to address this gap with examples>"
        }
    ],
    "strengths": [<list of 5-7 key strengths with specific details and CV/portfolio references>],
    "overall_assessment": "<detailed 3-4 paragraph assessment explaining the likelihood score, key strengths, main concerns, and overall recommendation>",
    "next_steps": [<list of 5-8 prioritized, actionable recommendations>]
}

**CRITICAL INSTRUCTIONS:**
1. BE DETAILED AND DESCRIPTIVE: Each point should be a complete sentence or two, not just a brief phrase. Provide context and specific examples.

2. For "portfolio_summary":
   - If portfolio was accessible, list 3-5 SPECIFIC projects, tools, or achievements you found
   - Quote or describe actual content you saw on the portfolio
   - Explain how the portfolio complements or contradicts the CV
   - If portfolio was not accessible, explain why and what impact this has

3. For "cv_feedback.strengths": Write 4-6 DETAILED points (2-3 sentences each) referencing specific CV content:
   - "The CV demonstrates 8+ years of progressive experience in software engineering, starting as a Junior Developer at [Company A] in 2015 and advancing to Senior Tech Lead at [Company B] by 2020. This clear career progression shows sustained growth in the field."
   - "Strong evidence of technical innovation is shown through leading the development of [specific system/product], which [specific achievement like 'reduced processing time by 60%' or 'serves 2M users daily']."
   
4. For "cv_feedback.weaknesses": Write 4-6 DETAILED points (2-3 sentences each) with specific examples:
   - "While the CV lists multiple projects, it lacks quantifiable metrics for impact. For example, the [Project X] description should include metrics like user adoption, performance improvements, or business value generated."
   - "The CV does not provide evidence of international recognition such as speaking engagements, awards, or publications in reputable venues, which are important criteria for this visa category."

5. For "cv_feedback.improvement_recommendations": Provide 3-5 ACTIONABLE suggestions:
   - "Add a 'Key Achievements' section at the top highlighting your 3-5 most impressive accomplishments with quantifiable metrics"
   - "Under each role, include specific metrics (team size, budget, users impacted, performance improvements)"
   
6. For "strengths": List 5-7 detailed strengths (2-3 sentences each) that cite SPECIFIC evidence:
   - "Demonstrated innovation leadership through founding [Company/Project Name] in [Year], which achieved [specific milestone like funding, users, or recognition]. This is evidenced in both the CV employment history and corroborated by the portfolio showing the live product."
   - "Strong open-source contribution record with [X] GitHub stars across [Y] repositories, particularly the [Project Name] which has been adopted by [specific companies or use cases]. This demonstrates recognition beyond immediate employment."

7. For "overall_assessment": Write 3-4 DETAILED paragraphs:
   - Paragraph 1: Overall likelihood assessment and key strengths
   - Paragraph 2: Main areas of concern or gaps
   - Paragraph 3: Comparison to typical successful applications
   - Paragraph 4: Final recommendation and confidence level

8. **PORTFOLIO INTEGRATION**: Whenever you mention a strength or weakness, check if the portfolio provides additional evidence. Explicitly state: "This is further evidenced by the portfolio which shows..." or "However, the portfolio does not demonstrate..."

9. AVOID: Generic phrases like "good experience", "strong background", "many achievements". ALWAYS be specific with names, numbers, dates, and concrete examples.

10. Cross-reference ALL sources (CV, portfolio, GitHub, letters) in your analysis. Point out consistencies and discrepancies.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=3500
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
        
        result = json.loads(content)
        return result
    
    except Exception as e:
        print(f"Error in LLM analysis: {e}")
        return {
            'error': str(e),
            'likelihood': 0.0,
            'gaps': [{'type': 'analysis_error', 'severity': 'critical', 'description': f'Failed to analyze: {str(e)}'}],
            'overall_assessment': 'Analysis failed due to technical error'
        }


def generate_roadmap(analysis_result: Dict[str, Any], field: str, timeline_weeks: int = 40) -> Dict[str, Any]:
    """Generate actionable roadmap based on LLM analysis results"""
    
    if not client:
        return {
            'milestones': [],
            'total_weeks': 0,
            'feasibility': 'Cannot generate roadmap without LLM access'
        }
    
    gaps = analysis_result.get('gaps', [])
    strengths = analysis_result.get('strengths', [])
    next_steps = analysis_result.get('next_steps', [])
    
    prompt = f"""
You are an expert immigration advisor. Create a detailed, actionable roadmap to strengthen a UK Global Talent visa application in the {GLOBAL_TALENT_FIELDS[field]} field.

**CURRENT ASSESSMENT:**
- Likelihood: {analysis_result.get('likelihood', 0)}
- Strengths: {json.dumps(strengths, indent=2)}
- Gaps: {json.dumps(gaps, indent=2)}
- Suggested Next Steps: {json.dumps(next_steps, indent=2)}

**AVAILABLE TIME:** {timeline_weeks} weeks

Create a roadmap with specific, achievable milestones. Output ONLY valid JSON:

{{
    "milestones": [
        {{
            "title": "<milestone title>",
            "description": "<detailed actions>",
            "duration_weeks": <number>,
            "priority": "<critical/high/medium/low>",
            "evidence_to_collect": ["<specific evidence item 1>", "<specific evidence item 2>"],
            "addresses_gaps": ["<gap type 1>", "<gap type 2>"]
        }}
    ],
    "total_weeks": <total duration>,
    "feasibility_assessment": "<assessment of whether timeline is realistic>",
    "critical_path": ["<list of must-do items>"]
}}
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean markdown
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
            'error': str(e),
            'milestones': [],
            'total_weeks': 0
        }


# -------------------------------
# Complete Analysis Pipeline
# -------------------------------
def analyze_global_talent_application(
    field: str,
    document_paths: List[str],
    questionnaire_responses: Dict[str, Any]
) -> Dict[str, Any]:
    """Complete end-to-end analysis pipeline for Global Talent visa
    
    Args:
        field: One of 'digital_technology', 'arts_culture', 'science_research'
        document_paths: List of paths to PDF documents (CV, letters, portfolio)
        questionnaire_responses: Dict of answers to field-specific questions
        
    Returns:
        Complete analysis results with likelihood, gaps, and roadmap
    """
    
    print(f"Analyzing Global Talent application for {GLOBAL_TALENT_FIELDS[field]}...")
    
    # Parse all documents
    print("Parsing documents...")
    documents = parse_multiple_documents(document_paths)
    
    # Extract URLs from CV if available
    github_data = None
    linkedin_data = None
    portfolio_data = None
    
    if documents.get('cv'):
        cv_text = documents['cv'].get('text', '')
        urls = extract_urls(cv_text)
        
        if urls.get('github'):
            print("Fetching GitHub data...")
            github_data = analyze_github_profile(urls['github'])
        
        if urls.get('linkedin'):
            linkedin_data = analyze_linkedin_profile(urls['linkedin'])
    
    # Check for portfolio URL in questionnaire responses
    portfolio_url = questionnaire_responses.get('portfolio_url')
    if portfolio_url:
        print(f"Fetching portfolio data from {portfolio_url}...")
        portfolio_data = analyze_portfolio_website(portfolio_url)
        if portfolio_data.get('error'):
            print(f"Warning: Could not fetch portfolio - {portfolio_data.get('error')}")
    
    # Run LLM analysis
    print("Running LLM analysis...")
    analysis = analyze_evidence_with_llm(
        field=field,
        documents=documents,
        questionnaire_responses=questionnaire_responses,
        github_data=github_data,
        portfolio_data=portfolio_data
    )
    
    # Generate roadmap
    print("Generating roadmap...")
    roadmap = generate_roadmap(analysis, field)
    
    # Compile final result
    result = {
        'field': field,
        'timestamp': datetime.now(UTC).isoformat(),
        'documents_analyzed': {
            'cv': documents.get('cv') is not None,
            'recommendation_letters_count': len(documents.get('recommendation_letters', [])),
            'portfolio_items_count': len(documents.get('portfolio_items', []))
        },
        'external_data': {
            'github': github_data is not None,
            'linkedin': linkedin_data is not None
        },
        'analysis': analysis,
        'roadmap': roadmap
    }
    
    return result


def save_analysis_results(results: Dict[str, Any], output_path: str):
    """Save analysis results to JSON file"""
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to: {output_path}")
