'use client';

import { useState, useEffect } from 'react';
import { apiClient, type Question } from '@/lib/api';

interface QuestionnaireStepProps {
    field: string;
    sessionId: string;
    onNext: (responses: Record<string, any>) => void;
    onBack: () => void;
}

export default function QuestionnaireStep({ field, sessionId, onNext, onBack }: QuestionnaireStepProps) {
    const [questions, setQuestions] = useState<Question[]>([]);
    const [responses, setResponses] = useState<Record<string, any>>({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string>('');

    useEffect(() => {
        apiClient.getQuestionnaire(field)
            .then(data => setQuestions(data.questions.filter(q => q.type !== 'file_upload' && q.type !== 'file_upload_multiple')))
            .catch(err => setError('Failed to load questionnaire'));
    }, [field]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await apiClient.submitQuestionnaire(sessionId, responses);
            onNext(responses);
        } catch (err) {
            setError('Failed to submit questionnaire');
        } finally {
            setLoading(false);
        }
    };

    const renderQuestion = (question: Question) => {
        const value = responses[question.id];

        switch (question.type) {
            case 'number':
                return (
                    <input
                        type="number"
                        value={value ?? ''}
                        onChange={(e) => setResponses({ ...responses, [question.id]: e.target.valueAsNumber })}
                        className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-50 focus:border-blue-500 text-gray-900 transition-all outline-none"
                        required={question.required}
                        placeholder="0"
                    />
                );
            case 'yes_no':
                return (
                    <div className="flex space-x-4">
                        {['yes', 'no'].map((option) => (
                            <label key={option} className={`flex-1 flex items-center justify-center p-4 border-2 rounded-xl cursor-pointer transition-all ${(option === 'yes' && value === true) || (option === 'no' && value === false)
                                    ? 'border-blue-500 bg-blue-50 text-blue-700 font-bold'
                                    : 'border-gray-200 hover:border-gray-300 text-gray-600'
                                }`}>
                                <input
                                    type="radio"
                                    name={question.id}
                                    value={option}
                                    checked={
                                        option === 'yes'
                                            ? value === true
                                            : option === 'no' && value === false
                                    }
                                    onChange={() => setResponses({ ...responses, [question.id]: option === 'yes' })}
                                    className="sr-only"
                                    required={question.required}
                                />
                                <span className="capitalize">{option}</span>
                            </label>
                        ))}
                    </div>
                );
            case 'text':
            default:
                return (
                    <textarea
                        value={value || ''}
                        onChange={(e) => setResponses({ ...responses, [question.id]: e.target.value })}
                        rows={4}
                        className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-50 focus:border-blue-500 text-gray-900 transition-all outline-none resize-none"
                        required={question.required}
                        placeholder="Type your answer here..."
                    />
                );
        }
    };

    return (
        <div className="max-w-3xl mx-auto">
            <div className="bg-white rounded-2xl shadow-xl p-8 md:p-10 border border-gray-100">
                <div className="mb-8">
                    <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-2">Questionnaire</h2>
                    <p className="text-gray-600">Please answer the following questions to help us assess your profile.</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-8">
                    {questions.map((question) => (
                        <div key={question.id} className="bg-gray-50 p-6 rounded-xl border border-gray-100">
                            <label className="block text-base font-semibold text-gray-900 mb-3">
                                {question.question}
                                {question.required && <span className="text-red-500 ml-1">*</span>}
                            </label>
                            {renderQuestion(question)}
                        </div>
                    ))}

                    {error && (
                        <div className="p-4 bg-red-50 border border-red-200 rounded-xl flex items-start">
                            <svg className="w-5 h-5 text-red-500 mr-3 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <p className="text-sm text-red-600">{error}</p>
                        </div>
                    )}

                    <div className="flex flex-col-reverse md:flex-row gap-4 pt-4">
                        <button
                            type="button"
                            onClick={onBack}
                            className="px-8 py-4 border-2 border-gray-200 text-gray-700 font-bold rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all"
                        >
                            Back
                        </button>
                        <button
                            type="submit"
                            disabled={loading}
                            className="flex-1 py-4 px-8 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 disabled:opacity-50 transition-all shadow-lg shadow-blue-200 hover:shadow-blue-300 transform hover:-translate-y-0.5"
                        >
                            {loading ? (
                                <span className="flex items-center justify-center">
                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Submitting...
                                </span>
                            ) : 'Continue'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
