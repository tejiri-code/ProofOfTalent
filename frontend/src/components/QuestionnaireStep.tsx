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
                        value={value || ''}
                        onChange={(e) => setResponses({ ...responses, [question.id]: e.target.valueAsNumber })}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
                        required={question.required}
                    />
                );
            case 'yes_no':
                return (
                    <div className="flex space-x-4">
                        {['yes', 'no'].map((option) => (
                            <label key={option} className="flex items-center">
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
                                    className="mr-2 text-gray-900"
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
                        rows={3}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
                        required={question.required}
                    />
                );
        }
    };

    return (
        <div className="max-w-3xl mx-auto p-6">
            <div className="bg-white rounded-lg shadow-lg p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Questionnaire</h2>

                <form onSubmit={handleSubmit} className="space-y-6">
                    {questions.map((question) => (
                        <div key={question.id}>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                {question.question}
                                {question.required && <span className="text-red-500 ml-1">*</span>}
                            </label>
                            {renderQuestion(question)}
                        </div>
                    ))}

                    {error && (
                        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                            <p className="text-sm text-red-600">{error}</p>
                        </div>
                    )}

                    <div className="flex space-x-4">
                        <button
                            type="button"
                            onClick={onBack}
                            className="px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
                        >
                            Back
                        </button>
                        <button
                            type="submit"
                            disabled={loading}
                            className="flex-1 py-3 px-4 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
                        >
                            {loading ? 'Submitting...' : 'Continue'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
