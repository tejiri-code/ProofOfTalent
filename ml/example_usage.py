#!/usr/bin/env python3
"""
Example usage of the UK Global Talent Visa Analysis System
Demonstrates how to use the refactored LLM-based analysis
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.model_combined import (
    GLOBAL_TALENT_FIELDS,
    generate_evidence_questionnaire,
    analyze_global_talent_application,
    save_analysis_results
)


def main():
    """Example workflow for Global Talent visa analysis"""
    
    print("=" * 60)
    print("UK Global Talent Visa Analysis System - Example Usage")
    print("=" * 60)
    print()
    
    # Step 1: Select field
    print("Step 1: Select your field")
    print("Available fields:")
    for i, (key, name) in enumerate(GLOBAL_TALENT_FIELDS.items(), 1):
        print(f"  {i}. {name} ({key})")
    
    field = 'digital_technology'  # For this example
    print(f"\nSelected: {GLOBAL_TALENT_FIELDS[field]}\n")
    
    # Step 2: Show questionnaire
    print("Step 2: Questionnaire (would be interactive in real app)")
    questions = generate_evidence_questionnaire(field)
    print(f"Generated {len(questions)} questions for {GLOBAL_TALENT_FIELDS[field]}")
    print("\nSample questions:")
    for q in questions[:3]:
        print(f"  - {q['question']} (Type: {q['type']}, Required: {q['required']})")
    print("  ... and more\n")
    
    # Step 3: Example questionnaire responses
    questionnaire_responses = {
        'years_experience': 7,
        'github_url': 'https://github.com/example-user',
        'has_founded_company': True,
        'publications': 15,
        'speaking_engagements': True,
        'awards': 'Best Paper Award at Tech Conference 2023',
        'open_source': 'Main contributor to popular open-source project with 5000+ stars'
    }
    
    # Step 4: Example document paths (would be uploaded by user)
    example_docs = [
        'data/sample_cvs/john_doe_cv.pdf',  # CV
        'data/sample_cvs/letter1.pdf',       # Recommendation letter 1
        'data/sample_cvs/letter2.pdf',       # Recommendation letter 2
        'data/sample_cvs/letter3.pdf',       # Recommendation letter 3
        'data/sample_cvs/publication.pdf',   # Portfolio item 1
        'data/sample_cvs/award_certificate.pdf'  # Portfolio item 2
    ]
    
    print("Step 3: Document Upload")
    print(f"Example documents to process: {len(example_docs)}")
    print("  - 1 CV")
    print("  - 3 Recommendation letters")
    print("  - 2 Portfolio items\n")
    
    # Step 5: Run analysis
    print("Step 4: Running LLM Analysis...")
    print("Note: This example would fail without actual documents and OpenAI API key")
    print("In production, this would:")
    print("  1. Parse all uploaded PDFs")
    print("  2. Extract GitHub data if URL provided")
    print("  3. Send comprehensive prompt to GPT-4")
    print("  4. Receive detailed analysis with likelihood score and gaps")
    print("  5. Generate personalized roadmap\n")
    
    # Example of what the analysis call would look like:
    # results = analyze_global_talent_application(
    #     field=field,
    #     document_paths=example_docs,
    #     questionnaire_responses=questionnaire_responses
    # )
    # save_analysis_results(results, 'output/analysis_results.json')
    
    # Example output structure:
    example_output = {
        'field': 'digital_technology',
        'timestamp': '2024-11-22T11:30:00Z',
        'documents_analyzed': {
            'cv': True,
            'recommendation_letters_count': 3,
            'portfolio_items_count': 2
        },
        'analysis': {
            'likelihood': 0.78,
            'assessment_level': 'Exceptional Talent',
            'evidence_present': {
                'mandatory_documents': {
                    'cv': 'complete',
                    'recommendation_letters': 'complete',
                    'portfolio_evidence': 'strong'
                }
            },
            'gaps': [
                {
                    'type': 'media_coverage',
                    'severity': 'medium',
                    'description': 'Limited evidence of media coverage in tech publications',
                    'recommendation': 'Seek speaking opportunities and publish thought leadership articles'
                }
            ],
            'strengths': [
                'Strong GitHub presence with significant open-source contributions',
                '7 years of experience with leadership role in product company',
                'Multiple publications and speaking engagements'
            ],
            'overall_assessment': 'Strong candidate with clear evidence of innovation and recognition...'
        },
        'roadmap': {
            'milestones': [
                {
                    'title': 'Increase Media Visibility',
                    'description': 'Publish articles in tech publications, seek interviews',
                    'duration_weeks': 8,
                    'priority': 'high'
                }
            ],
            'total_weeks': 12,
            'feasibility_assessment': 'Application can be strengthened significantly within timeline'
        }
    }
    
    print("Step 5: Example Analysis Results")
    print(f"Likelihood: {example_output['analysis']['likelihood'] * 100}%")
    print(f"Assessment Level: {example_output['analysis']['assessment_level'] }")
    print(f"Identified Gaps: {len(example_output['analysis']['gaps'])}")
    print(f"Key Strengths: {len(example_output['analysis']['strengths'])}")
    print(f"\nRoadmap: {len(example_output['roadmap']['milestones'])} milestones over {example_output['roadmap']['total_weeks']} weeks")
    print()
    
    print("=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
