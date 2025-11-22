'use client';

import { useState } from 'react';
import { apiClient, type Field } from '@/lib/api';

interface FieldSelectionProps {
    onNext: (field: string, sessionId: string) => void;
}

export default function FieldSelection({ onNext }: FieldSelectionProps) {
    const [fields, setFields] = useState<Field[]>([]);
    const [selectedField, setSelectedField] = useState<string>('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string>('');

    // Load fields on mount
    useState(() => {
        apiClient.getFields()
            .then(data => setFields(data.fields))
            .catch(err => setError('Failed to load fields'));
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!selectedField) return;

        setLoading(true);
        setError('');

        try {
            const session = await apiClient.createSession(selectedField);
            onNext(selectedField, session.session_id);
        } catch (err) {
            setError('Failed to create session. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto">
            <div className="bg-white rounded-2xl shadow-xl p-8 md:p-10 border border-gray-100">
                <div className="text-center mb-10">
                    <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                        UK Global Talent Visa Analysis
                    </h1>
                    <p className="text-lg text-gray-600">
                        Get AI-powered analysis of your visa application using GPT-4
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-8">
                    <div>
                        <label className="block text-sm font-bold text-gray-700 uppercase tracking-wide mb-4">
                            Select your field
                        </label>
                        <div className="space-y-4">
                            {fields.map((field) => (
                                <label
                                    key={field.id}
                                    className={`group relative block p-6 border-2 rounded-xl cursor-pointer transition-all duration-200 ${selectedField === field.id
                                        ? 'border-blue-500 bg-blue-50 shadow-md shadow-blue-100'
                                        : 'border-gray-100 hover:border-blue-200 hover:bg-gray-50'
                                        }`}
                                >
                                    <input
                                        type="radio"
                                        name="field"
                                        value={field.id}
                                        checked={selectedField === field.id}
                                        onChange={(e) => setSelectedField(e.target.value)}
                                        className="sr-only"
                                    />
                                    <div className="flex items-center">
                                        <div className={`w-6 h-6 rounded-full border-2 mr-4 flex items-center justify-center transition-colors ${selectedField === field.id ? 'border-blue-500' : 'border-gray-300 group-hover:border-blue-400'
                                            }`}>
                                            {selectedField === field.id && (
                                                <div className="w-3 h-3 rounded-full bg-blue-500" />
                                            )}
                                        </div>
                                        <span className={`text-lg font-medium transition-colors ${selectedField === field.id ? 'text-blue-900' : 'text-gray-900'}`}>
                                            {field.name}
                                        </span>
                                    </div>
                                </label>
                            ))}
                        </div>
                    </div>

                    {error && (
                        <div className="p-4 bg-red-50 border border-red-200 rounded-xl flex items-start">
                            <svg className="w-5 h-5 text-red-500 mr-3 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <p className="text-sm text-red-600">{error}</p>
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={!selectedField || loading}
                        className="w-full py-4 px-6 bg-blue-600 text-white font-bold text-lg rounded-xl hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-blue-200 hover:shadow-blue-300 transform hover:-translate-y-0.5"
                    >
                        {loading ? (
                            <span className="flex items-center justify-center">
                                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Creating Session...
                            </span>
                        ) : 'Continue'}
                    </button>
                </form>
            </div>
        </div>
    );
}
