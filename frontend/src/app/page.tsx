'use client';

import { useState } from 'react';
import FieldSelection from '@/components/FieldSelection';
import QuestionnaireStep from '@/components/QuestionnaireStep';
import DocumentUpload from '@/components/DocumentUpload';
import AnalysisResults from '@/components/AnalysisResults';
import Header from '@/components/Header';
import LandingPage from '@/components/LandingPage';
import CookieConsent from '@/components/CookieConsent';

type Step = 'landing' | 'field' | 'questionnaire' | 'upload' | 'results';

export default function Home() {
  const [currentStep, setCurrentStep] = useState<Step>('landing');
  const [field, setField] = useState<string>('');
  const [sessionId, setSessionId] = useState<string>('');
  const [questionnaireResponses, setQuestionnaireResponses] = useState<Record<string, any>>({});
  const [files, setFiles] = useState<File[]>([]);

  const handleStart = () => {
    setCurrentStep('field');
  };

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
    setFiles([]);
  };

  // Navigation handler
  const handleStepClick = (stepIndex: number) => {
    const steps: Step[] = ['field', 'questionnaire', 'upload', 'results'];
    // Adjust index for landing page
    if (currentStep === 'landing') return;

    const currentStepIndex = steps.indexOf(currentStep);

    // Allow going back to any previous step
    // Allow going forward only if we have the necessary data for that step
    if (stepIndex < currentStepIndex) {
      setCurrentStep(steps[stepIndex]);
    } else if (stepIndex === currentStepIndex) {
      // Do nothing if clicking current step
      return;
    } else {
      // Logic for forward navigation via progress bar (optional, usually restricted)
      // For now, we only allow clicking if we've already completed the previous steps
      // But since we don't track "completed" separately from "current", 
      // we can just check if we have the data.

      if (stepIndex === 1 && field && sessionId) {
        setCurrentStep('questionnaire');
      } else if (stepIndex === 2 && Object.keys(questionnaireResponses).length > 0) {
        setCurrentStep('upload');
      }
      // We generally don't allow jumping to results without uploading
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
      <Header />

      {currentStep === 'landing' ? (
        <LandingPage onStart={handleStart} />
      ) : (
        <div className="pt-24 pb-12">
          {/* Progress Bar */}
          <div className="max-w-4xl mx-auto px-4 md:px-6 mb-8 md:mb-12">
            <div className="flex items-center justify-between overflow-x-auto pb-4 md:pb-0">
              {['Field Selection', 'Questionnaire', 'Documents', 'Analysis'].map((label, idx) => {
                const stepMap: Step[] = ['field', 'questionnaire', 'upload', 'results'];
                const stepIndex = stepMap.indexOf(currentStep);
                const isActive = idx === stepIndex;
                const isComplete = idx < stepIndex;

                // Determine if step is clickable
                const isClickable = idx < stepIndex || (idx === 1 && field && sessionId) || (idx === 2 && Object.keys(questionnaireResponses).length > 0);

                return (
                  <div
                    key={label}
                    className={`flex items-center flex-1 min-w-[120px] md:min-w-0 ${isClickable ? 'cursor-pointer' : 'cursor-not-allowed'}`}
                    onClick={() => isClickable && handleStepClick(idx)}
                  >
                    <div className="flex items-center">
                      <div
                        className={`w-8 h-8 md:w-10 md:h-10 rounded-full flex items-center justify-center font-semibold text-sm md:text-base transition-colors duration-300 ${isComplete
                          ? 'bg-green-500 text-white shadow-md shadow-green-200'
                          : isActive
                            ? 'bg-blue-600 text-white shadow-md shadow-blue-200 ring-4 ring-blue-50'
                            : 'bg-white border-2 border-gray-200 text-gray-400'
                          }`}
                      >
                        {isComplete ? (
                          <svg className="w-5 h-5 md:w-6 md:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                          </svg>
                        ) : (
                          idx + 1
                        )}
                      </div>
                      <span
                        className={`ml-2 md:ml-3 text-xs md:text-sm font-medium whitespace-nowrap transition-colors duration-300 ${isActive ? 'text-blue-600' : isComplete ? 'text-green-600' : 'text-gray-400'
                          }`}
                      >
                        {label}
                      </span>
                    </div>
                    {idx < 3 && (
                      <div
                        className={`flex-1 h-0.5 md:h-1 mx-2 md:mx-4 rounded-full transition-colors duration-500 ${isComplete ? 'bg-green-500' : 'bg-gray-200'
                          }`}
                      />
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Main Content */}
          <div className="px-4 md:px-6">
            {currentStep === 'field' && <FieldSelection onNext={handleFieldNext} />}

            {currentStep === 'questionnaire' && (
              <QuestionnaireStep
                field={field}
                sessionId={sessionId}
                initialResponses={questionnaireResponses}
                onNext={handleQuestionnaireNext}
                onBack={() => setCurrentStep('field')}
              />
            )}

            {currentStep === 'upload' && (
              <DocumentUpload
                sessionId={sessionId}
                initialFiles={files}
                onFilesChange={setFiles}
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
          </div>
        </div>
      )}
      <CookieConsent />
    </main>
  );
}
