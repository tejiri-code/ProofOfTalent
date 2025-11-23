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
    const [privacyConsent, setPrivacyConsent] = useState(false);

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
            <div className="bg-white rounded-2xl shadow-xl p-6 sm:p-8 md:p-10 border border-gray-100">
                <div className="text-center mb-8 sm:mb-10">
                    <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 mb-3 sm:mb-4 text-shadow-sm px-2">
                        UK Global Talent Visa Analysis
                    </h1>
                    <p className="text-base sm:text-lg text-gray-700 font-medium px-2">
                        Get AI-powered analysis of your visa application using <span className="text-blue-600 font-semibold">GPT-4</span>
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6 sm:space-y-8">
                    <div>
                        <label className="block text-xs sm:text-sm font-bold text-gray-800 uppercase tracking-wider mb-3 sm:mb-4 px-1">
                            Select your field
                        </label>
                        <div className="space-y-3 sm:space-y-4">
                            {fields.map((field) => (
                                <label
                                    key={field.id}
                                    className={`group relative block p-4 sm:p-5 md:p-6 border-2 rounded-xl cursor-pointer transition-all duration-200 min-h-[60px] ${selectedField === field.id
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
                                        <div className={`w-5 h-5 sm:w-6 sm:h-6 rounded-full border-2 mr-3 sm:mr-4 flex items-center justify-center transition-colors flex-shrink-0 ${selectedField === field.id ? 'border-blue-500' : 'border-gray-300 group-hover:border-blue-400'
                                            }`}>
                                            {selectedField === field.id && (
                                                <div className="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-blue-500" />
                                            )}
                                        </div>
                                        <span className={`text-base sm:text-lg font-medium transition-colors ${selectedField === field.id ? 'text-blue-900' : 'text-gray-900'}`}>
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

                    {/* Privacy Consent */}
                    <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 sm:p-5">
                        <label className="flex items-start cursor-pointer group">
                            <input
                                type="checkbox"
                                checked={privacyConsent}
                                onChange={(e) => setPrivacyConsent(e.target.checked)}
                                className="mt-1 w-4 h-4 sm:w-5 sm:h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500 focus:ring-2 cursor-pointer flex-shrink-0"
                                required
                            />
                            <span className="ml-3 text-xs sm:text-sm text-gray-700 leading-relaxed">
                                I understand and consent to the collection and processing of my data for visa assessment purposes. Your data will be processed securely and in accordance with GDPR. You can request deletion of your data at any time. By continuing, you acknowledge this is a guidance tool and <strong>not legal advice</strong>.
                            </span>
                        </label>
                    </div>

                    <button
                        type="submit"
                        disabled={!selectedField || !privacyConsent || loading}
                        className="w-full py-3.5 sm:py-4 px-6 bg-blue-600 text-white font-bold text-base sm:text-lg rounded-xl hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-blue-200 hover:shadow-blue-300 transform hover:-translate-y-0.5 min-h-[48px]"
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
