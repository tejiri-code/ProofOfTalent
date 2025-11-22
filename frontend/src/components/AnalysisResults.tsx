'use client';

import { useState, useEffect } from 'react';
import { apiClient, type AnalysisResult } from '@/lib/api';

interface AnalysisResultsProps {
    sessionId: string;
    onNewStart: () => void;
}

export default function AnalysisResults({ sessionId, onNewStart }: AnalysisResultsProps) {
    const [results, setResults] = useState<AnalysisResult | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string>('');

    const [loadingStep, setLoadingStep] = useState(0);
    const [progress, setProgress] = useState(0);

    const ANALYSIS_STEPS = [
        "Analyzing CV content and structure...",
        "Extracting key skills and achievements...",
        "Matching against Global Talent Visa criteria...",
        "Identifying evidence gaps...",
        "Generating personalized roadmap..."
    ];

    useEffect(() => {
        if (!loading) return;

        // Simulate progress
        const interval = setInterval(() => {
            setProgress(prev => {
                if (prev >= 95) return prev;
                return prev + 1;
            });
        }, 100);

        // Simulate steps
        const stepInterval = setInterval(() => {
            setLoadingStep(prev => {
                if (prev >= ANALYSIS_STEPS.length - 1) return prev;
                return prev + 1;
            });
        }, 2000);

        return () => {
            clearInterval(interval);
            clearInterval(stepInterval);
        };
    }, [loading]);

    useEffect(() => {
        const runAnalysis = async () => {
            try {
                // Start analysis
                await apiClient.analyzeApplication(sessionId);

                // Poll for results
                const checkResults = async () => {
                    const data = await apiClient.getResults(sessionId);
                    if (data.status === 'completed' && data.results) {
                        setProgress(100);
                        setTimeout(() => {
                            setResults(data);
                            setLoading(false);
                        }, 500); // Small delay to show 100%
                    } else if (data.status === 'error') {
                        setError('Analysis failed. Please try again.');
                        setLoading(false);
                    } else {
                        // Still processing, check again in 2 seconds
                        setTimeout(checkResults, 2000);
                    }
                };

                checkResults();
            } catch (err) {
                setError('Failed to start analysis');
                setLoading(false);
            }
        };

        runAnalysis();
    }, [sessionId]);

    if (loading) {
        return (
            <div className="max-w-2xl mx-auto p-6">
                <div className="bg-white rounded-lg shadow-lg p-8">
                    <div className="text-center mb-8">
                        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
                        <h2 className="text-2xl font-bold text-gray-900 mb-2">Analyzing Your Profile</h2>
                        <p className="text-gray-600">Please wait while we process your documents</p>
                    </div>

                    <div className="space-y-6">
                        {/* Progress Bar */}
                        <div className="w-full bg-gray-200 rounded-full h-2.5">
                            <div
                                className="bg-blue-600 h-2.5 rounded-full transition-all duration-300 ease-out"
                                style={{ width: `${progress}%` }}
                            ></div>
                        </div>

                        {/* Steps */}
                        <div className="space-y-3">
                            {ANALYSIS_STEPS.map((step, index) => (
                                <div key={index} className="flex items-center space-x-3">
                                    <div className={`flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center ${index < loadingStep ? 'bg-green-500 text-white' :
                                            index === loadingStep ? 'bg-blue-500 text-white animate-pulse' :
                                                'bg-gray-200'
                                        }`}>
                                        {index < loadingStep && (
                                            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                                            </svg>
                                        )}
                                    </div>
                                    <span className={`text-sm ${index <= loadingStep ? 'text-gray-900 font-medium' : 'text-gray-400'
                                        }`}>
                                        {step}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    if (error || !results?.results) {
        return (
            <div className="max-w-4xl mx-auto p-6">
                <div className="bg-white rounded-lg shadow-lg p-8">
                    <div className="text-center text-red-600 mb-4">
                        <svg className="w-16 h-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <h2 className="text-2xl font-bold mb-2">Analysis Failed</h2>
                        <p>{error}</p>
                    </div>
                    <button
                        onClick={onNewStart}
                        className="w-full py-3 px-4 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700"
                    >
                        Start New Analysis
                    </button>
                </div>
            </div>
        );
    }

    const { analysis, roadmap } = results.results;
    const likelihoodPercent = (analysis.likelihood * 100).toFixed(1);

    return (
        <div className="max-w-4xl mx-auto p-6 space-y-6">
            {/* Likelihood Score */}
            <div className="bg-white rounded-lg shadow-lg p-8">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">Analysis Complete</h2>

                <div className="flex items-center space-x-4 mb-6">
                    <div className="flex-1">
                        <div className="flex items-baseline space-x-2">
                            <span className="text-5xl font-bold text-blue-600">{likelihoodPercent}%</span>
                            <span className="text-gray-600">likelihood of approval</span>
                        </div>
                        <p className="text-lg text-gray-700 mt-2">
                            Assessment Level: <span className="font-semibold">{analysis.assessment_level}</span>
                        </p>
                    </div>
                    <div className="w-32 h-32">
                        <svg className="transform -rotate-90" viewBox="0 0 120 120">
                            <circle cx="60" cy="60" r="54" fill="none" stroke="#e5e7eb" strokeWidth="12" />
                            <circle
                                cx="60"
                                cy="60"
                                r="54"
                                fill="none"
                                stroke="#3b82f6"
                                strokeWidth="12"
                                strokeDasharray={`${analysis.likelihood * 339.292} 339.292`}
                                strokeLinecap="round"
                            />
                        </svg>
                    </div>
                </div>

                <p className="text-gray-700 bg-gray-50 p-4 rounded-lg">
                    {analysis.overall_assessment}
                </p>
            </div>

            {/* Strengths */}
            {analysis.strengths.length > 0 && (
                <div className="bg-white rounded-lg shadow-lg p-8">
                    <h3 className="text-2xl font-bold text-gray-900 mb-4">Strengths</h3>
                    <ul className="space-y-2">
                        {analysis.strengths.map((strength, idx) => (
                            <li key={idx} className="flex items-start">
                                <svg className="w-6 h-6 text-green-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <span className="text-gray-700">{strength}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Gaps */}
            {analysis.gaps.length > 0 && (
                <div className="bg-white rounded-lg shadow-lg p-8">
                    <h3 className="text-2xl font-bold text-gray-900 mb-4">Areas for Improvement</h3>
                    <div className="space-y-4">
                        {analysis.gaps.map((gap, idx) => (
                            <div key={idx} className="border-l-4 border-yellow-400 pl-4 py-2">
                                <div className="flex items-center space-x-2 mb-1">
                                    <span className={`px-2 py-1 text-xs font-semibold rounded ${gap.severity === 'critical' ? 'bg-red-100 text-red-800' :
                                        gap.severity === 'high' ? 'bg-orange-100 text-orange-800' :
                                            gap.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                                                'bg-blue-100 text-blue-800'
                                        }`}>
                                        {gap.severity.toUpperCase()}
                                    </span>
                                    <span className="font-medium text-gray-900">{gap.type.replace(/_/g, ' ')}</span>
                                </div>
                                <p className="text-gray-700 text-sm">{gap.description}</p>
                                <p className="text-blue-600 text-sm mt-1">💡 {gap.recommendation}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Roadmap */}
            <div className="bg-white rounded-lg shadow-lg p-8">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">Personalized Roadmap</h3>
                <p className="text-gray-600 mb-4">
                    Timeline: {roadmap.total_weeks} weeks
                </p>
                <p className="text-gray-700 bg-blue-50 p-4 rounded-lg mb-6">
                    {roadmap.feasibility_assessment}
                </p>

                <div className="space-y-6">
                    {roadmap.milestones.map((milestone, idx) => (
                        <div key={idx} className="relative pl-8 pb-6 border-l-2 border-gray-200 last:border-l-0">
                            <div className="absolute -left-2 top-0 w-4 h-4 rounded-full bg-blue-600"></div>
                            <div>
                                <div className="flex items-center space-x-2 mb-2">
                                    <h4 className="font-bold text-lg text-gray-900">{milestone.title}</h4>
                                    <span className={`px-2 py-1 text-xs font-semibold rounded ${milestone.priority === 'critical' ? 'bg-red-100 text-red-800' :
                                        milestone.priority === 'high' ? 'bg-orange-100 text-orange-800' :
                                            'bg-blue-100 text-blue-800'
                                        }`}>
                                        {milestone.priority}
                                    </span>
                                    <span className="text-sm text-gray-500">{milestone.duration_weeks} weeks</span>
                                </div>
                                <p className="text-gray-700 mb-3">{milestone.description}</p>
                                {milestone.evidence_to_collect.length > 0 && (
                                    <div className="text-sm">
                                        <span className="font-medium text-gray-900">Evidence to collect:</span>
                                        <ul className="list-disc list-inside text-gray-600 ml-4">
                                            {milestone.evidence_to_collect.map((evidence, i) => (
                                                <li key={i}>{evidence}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <button
                onClick={onNewStart}
                className="w-full py-3 px-4 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700"
            >
                Start New Analysis
            </button>
        </div>
    );
}
