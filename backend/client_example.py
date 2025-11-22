"""
Example Python client for UK Global Talent Visa Analysis API
Demonstrates how to use the API endpoints
"""

import requests
import json
from typing import List, Dict, Any

BASE_URL = "http://localhost:8000"


class GlobalTalentAPIClient:
    """Client for interacting with the Global Talent Analysis API"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session_id = None
    
    def get_fields(self) -> Dict[str, Any]:
        """Get available fields"""
        response = requests.get(f"{self.base_url}/api/fields")
        return response.json()
    
    def create_session(self, field: str) -> Dict[str, Any]:
        """Create a new analysis session"""
        response = requests.post(
            f"{self.base_url}/api/session/create",
            json={"field": field}
        )
        result = response.json()
        self.session_id = result["session_id"]
        return result
    
    def get_questionnaire(self, field: str) -> Dict[str, Any]:
        """Get field-specific questionnaire"""
        response = requests.get(f"{self.base_url}/api/questionnaire/{field}")
        return response.json()
    
    def upload_documents(self, file_paths: List[str]) -> Dict[str, Any]:
        """Upload documents to the session"""
        if not self.session_id:
            raise ValueError("No active session. Create a session first.")
        
        files = [('files', open(path, 'rb')) for path in file_paths]
        
        try:
            response = requests.post(
                f"{self.base_url}/api/upload/{self.session_id}",
                files=files
            )
            return response.json()
        finally:
            # Close all file handles
            for _, file in files:
                file.close()
    
    def submit_questionnaire(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Submit questionnaire responses for the session"""
        if not self.session_id:
            raise ValueError("No active session. Create a session first.")
        
        response = requests.post(
            f"{self.base_url}/api/session/{self.session_id}/questionnaire",
            json=responses
        )
        return response.json()
    
    def analyze(self) -> Dict[str, Any]:
        """Run analysis on the session"""
        if not self.session_id:
            raise ValueError("No active session. Create a session first.")
        
        response = requests.post(f"{self.base_url}/api/analyze/{self.session_id}")
        return response.json()
    
    def get_results(self) -> Dict[str, Any]:
        """Get analysis results"""
        if not self.session_id:
            raise ValueError("No active session. Create a session first.")
        
        response = requests.get(f"{self.base_url}/api/results/{self.session_id}")
        return response.json()
    
    def get_session_status(self) -> Dict[str, Any]:
        """Get current session status"""
        if not self.session_id:
            raise ValueError("No active session. Create a session first.")
        
        response = requests.get(f"{self.base_url}/api/session/{self.session_id}/status")
        return response.json()
    
    def delete_session(self) -> Dict[str, Any]:
        """Delete the current session"""
        if not self.session_id:
            raise ValueError("No active session. Create a session first.")
        
        response = requests.delete(f"{self.base_url}/api/session/{self.session_id}")
        result = response.json()
        self.session_id = None
        return result


def example_workflow():
    """Example workflow using the  API"""
    
    # Initialize client
    client = GlobalTalentAPIClient()
    
    print("=" * 60)
    print("UK Global Talent Visa Analysis - API Client Example")
    print("=" * 60)
    print()
    
    # Step 1: Get available fields
    print("Step 1: Getting available fields...")
    fields = client.get_fields()
    print(f"Available fields: {json.dumps(fields, indent=2)}")
    print()
    
    # Step 2: Create session
    field = "digital_technology"
    print(f"Step 2: Creating session for {field}...")
    session = client.create_session(field)
    print(f"Session created: {session['session_id']}")
    print()
    
    # Step 3: Get questionnaire
    print("Step 3: Getting questionnaire...")
    questionnaire = client.get_questionnaire(field)
    print(f"Questionnaire has {len(questionnaire['questions'])} questions")
    print("Sample questions:")
    for q in questionnaire['questions'][:3]:
        print(f"  - {q['question']}")
    print()
    
    # Step 4: Submit questionnaire responses
    print("Step 4: Submitting questionnaire responses...")
    responses = {
        "years_experience": 7,
        "github_url": "https://github.com/example",
        "has_founded_company": True,
        "publications": 15,
        "speaking_engagements": True,
        "awards": "Best Paper Award 2023",
        "open_source": "5000+ GitHub stars"
    }
    result = client.submit_questionnaire(responses)
    print(f"Questionnaire submitted: {result['status']}")
    print()
    
    # Step 5: Upload documents (example - would fail without real files)
    print("Step 5: Document upload (skipped - requires real PDF files)")
    print("In production, you would call:")
    print("  client.upload_documents(['cv.pdf', 'letter1.pdf', 'letter2.pdf', 'letter3.pdf'])")
    print()
    
    # Step 6: Check session status
    print("Step 6: Checking session status...")
    status = client.get_session_status()
    print(f"Session status: {json.dumps(status, indent=2)}")
    print()
    
    # Step 7: Analysis (would run if documents were uploaded)
    print("Step 7: Analysis (skipped - requires documents)")
    print("In production, you would call:")
    print("  results = client.analyze()")
    print("  print(results)")
    print()
    
    # Step 8: Clean up
    print("Step 8: Cleaning up session...")
    delete_result = client.delete_session()
    print(f"Session deleted: {delete_result['status']}")
    print()
    
    print("=" * 60)
    print("Example workflow complete!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        example_workflow()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server.")
        print("Make sure the server is running:")
        print("  cd backend && ./start.sh")
    except Exception as e:
        print(f"Error: {e}")
