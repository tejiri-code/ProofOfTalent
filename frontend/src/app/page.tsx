'use client';

import { useState } from 'react';
import FieldSelection from '@/components/FieldSelection';
import QuestionnaireStep from '@/components/QuestionnaireStep';
import DocumentUpload from '@/components/DocumentUpload';
import AnalysisResults from '@/components/AnalysisResults';

type Step = 'field' | 'questionnaire' | 'upload' | 'results';

export default function Home() {
  const [currentStep, setCurrentStep] = useState<Step>('field');
  const [field, setField] = useState<string>('');
  const [sessionId, setSessionId] = useState<string>('');
  const [questionnaireResponses, setQuestionnaireResponses] = useState<Record<string, any>>({});

  const handleFieldNext = (selectedField: string, newSessionId: string) => {
    setField(selectedField);
    setSessionId(newSessionId);
    setCurrentStep('questionnaire');
  };

  const handleQuestionnaireNext = (responses: Record<string, any>) => {
    setQuestionnaireResponses(responses);
    setCurrentStep('upload');
  };

  const handleUploadNext = () => {
    setCurrentStep('results');
  };

  const handleNewStart = () => {
    setCurrentStep('field');
    setField('');
    setSessionId('');
    setQuestionnaireResponses({});
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-12">
      {/* Progress Bar */}
      <div className="max-w-4xl mx-auto px-6 mb-8">
        <div className="flex items-center justify-between">
          {['Field Selection', 'Questionnaire', 'Documents', 'Analysis'].map((label, idx) => {
            const stepMap: Step[] = ['field', 'questionnaire', 'upload', 'results'];
            const stepIndex = stepMap.indexOf(currentStep);
            const isActive = idx === stepIndex;
            const isComplete = idx < stepIndex;

            return (
              <div key={label} className="flex items-center flex-1">
                <div className="flex items-center">
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold ${isComplete
                        ? 'bg-green-500 text-white'
                        : isActive
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-600'
                      }`}
                  >
                    {isComplete ? (
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    ) : (
                      idx + 1
                    )}
                  </div>
                  <span
                    className={`ml-2 text-sm font-medium ${isActive ? 'text-blue-600' : isComplete ? 'text-green-600' : 'text-gray-500'
                      }`}
                  >
                    {label}
                  </span>
                </div>
                {idx < 3 && (
                  <div
                    className={`flex-1 h-1 mx-4 ${isComplete ? 'bg-green-500' : 'bg-gray-200'
                      }`}
                  />
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Main Content */}
      {currentStep === 'field' && <FieldSelection onNext={handleFieldNext} />}

      {currentStep === 'questionnaire' && (
        <QuestionnaireStep
          field={field}
          sessionId={sessionId}
          onNext={handleQuestionnaireNext}
          onBack={() => setCurrentStep('field')}
        />
      )}

      {currentStep === 'upload' && (
        <DocumentUpload
          sessionId={sessionId}
          onNext={handleUploadNext}
          onBack={() => setCurrentStep('questionnaire')}
        />
      )}

      {currentStep === 'results' && (
        <AnalysisResults
          sessionId={sessionId}
          onNewStart={handleNewStart}
        />
      )}
    </main>
  );
}
