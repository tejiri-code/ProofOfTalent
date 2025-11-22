# Add to end of model_new.py - LLM Analysis Functions

# -------------------------------
# LLM-Based Global Talent Evidence Analysis
# -------------------------------
def analyze_evidence_with_llm(
    field: str,
    documents: Dict[str, Any],
    questionnaire_responses: Dict[str, Any],
    github_data: Optional[Dict[str, Any]] = None
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
    
    prompt += """

**YOUR TASK:**
Evaluate this candidate's application against the official Global Talent visa criteria. Provide a detailed assessment in JSON format with the following structure:

{
    "likelihood": <float between 0.0 and 1.0>,
    "assessment_level": "<Exceptional Talent or Exceptional Promise>",
    "evidence_present": {
        "mandatory_documents": {
            "cv": <"complete" or "incomplete" or "missing">,
            "recommendation_letters": <"complete" (3 letters) or "incomplete" (fewer than 3) or "missing">,
            "portfolio_evidence": <"strong" or "adequate" or "weak">
        },
        "innovation_evidence": [<list of identified innovation evidence>],
        "recognition_evidence": [<list of identified recognition evidence>]
    },
    "gaps": [
        {
            "type": "<gap type>",
            "severity": "<critical, high, medium, low>",
            "description": "<detailed description of what's missing>",
            "recommendation": "<specific action to address this gap>"
        }
    ],
    "strengths": [<list of key strengths in the application>],
    "overall_assessment": "<detailed paragraph explaining the likelihood score>",
    "next_steps": [<list of recommended actions>]
}

Be thorough and precise. Base your assessment on actual evidence provided, not assumptions.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=2000
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
    
    if documents.get('cv'):
        cv_text = documents['cv'].get('text', '')
        urls = extract_urls(cv_text)
        
        if urls.get('github'):
            print("Fetching GitHub data...")
            github_data = analyze_github_profile(urls['github'])
        
        if urls.get('linkedin'):
            linkedin_data = analyze_linkedin_profile(urls['linkedin'])
    
    # Run LLM analysis
    print("Running LLM analysis...")
    analysis = analyze_evidence_with_llm(
        field=field,
        documents=documents,
        questionnaire_responses=questionnaire_responses,
        github_data=github_data
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
