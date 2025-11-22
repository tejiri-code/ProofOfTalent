// API Client for UK Global Talent Visa Analysis

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Field {
  id: string;
  name: string;
}

export interface Question {
  id: string;
  question: string;
  type: string;
  required: boolean;
  file_types?: string[];
  min_files?: number;
  max_files?: number;
}

export interface Session {
  session_id: string;
  field: string;
  field_name: string;
}

export interface AnalysisResult {
  session_id: string;
  status: string;
  results?: {
    field: string;
    analysis: {
      likelihood: number;
      assessment_level: string;
      evidence_present: any;
      gaps: Array<{
        type: string;
        severity: string;
        description: string;
        recommendation: string;
      }>;
      strengths: string[];
      overall_assessment: string;
    };
    roadmap: {
      milestones: Array<{
        title: string;
        description: string;
        duration_weeks: number;
        priority: string;
        evidence_to_collect: string[];
        addresses_gaps: string[];
      }>;
      total_weeks: number;
      feasibility_assessment: string;
    };
  };
}

class APIClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  async getFields(): Promise<{ fields: Field[] }> {
    const response = await fetch(`${this.baseURL}/api/fields`);
    if (!response.ok) throw new Error('Failed to fetch fields');
    return response.json();
  }

  async createSession(field: string): Promise<Session> {
    const response = await fetch(`${this.baseURL}/api/session/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ field }),
    });
    if (!response.ok) throw new Error('Failed to create session');
    return response.json();
  }

  async getQuestionnaire(field: string): Promise<{ field: string; field_name: string; questions: Question[] }> {
    const response = await fetch(`${this.baseURL}/api/questionnaire/${field}`);
    if (!response.ok) throw new Error('Failed to fetch questionnaire');
    return response.json();
  }

  async uploadDocuments(sessionId: string, files: File[]): Promise<any> {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));

    const response = await fetch(`${this.baseURL}/api/upload/${sessionId}`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) throw new Error('Failed to upload documents');
    return response.json();
  }

  async submitQuestionnaire(sessionId: string, responses: Record<string, any>): Promise<any> {
    const response = await fetch(`${this.baseURL}/api/session/${sessionId}/questionnaire`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(responses),
    });
    if (!response.ok) throw new Error('Failed to submit questionnaire');
    return response.json();
  }

  async analyzeApplication(sessionId: string): Promise<AnalysisResult> {
    const response = await fetch(`${this.baseURL}/api/analyze/${sessionId}`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to analyze application');
    return response.json();
  }

  async getResults(sessionId: string): Promise<AnalysisResult> {
    const response = await fetch(`${this.baseURL}/api/results/${sessionId}`);
    if (!response.ok) throw new Error('Failed to fetch results');
    return response.json();
  }

  async getSessionStatus(sessionId: string): Promise<any> {
    const response = await fetch(`${this.baseURL}/api/session/${sessionId}/status`);
    if (!response.ok) throw new Error('Failed to fetch session status');
    return response.json();
  }

  async deleteSession(sessionId: string): Promise<any> {
    const response = await fetch(`${this.baseURL}/api/session/${sessionId}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete session');
    return response.json();
  }
}

export const apiClient = new APIClient();
