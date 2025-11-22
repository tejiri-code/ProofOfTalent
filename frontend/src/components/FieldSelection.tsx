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
        <div className="max-w-2xl mx-auto p-6">
            <div className="bg-white rounded-lg shadow-lg p-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">
                    UK Global Talent Visa Analysis
                </h1>
                <p className="text-gray-600 mb-8">
                    Get AI-powered analysis of your visa application using GPT-4
                </p>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-4">
                            Select your field
                        </label>
                        <div className="space-y-3">
                            {fields.map((field) => (
                                <label
                                    key={field.id}
                                    className={`block p-4 border-2 rounded-lg cursor-pointer transition-all ${selectedField === field.id
                                            ? 'border-blue-500 bg-blue-50'
                                            : 'border-gray-200 hover:border-gray-300'
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
                                        <div className={`w-5 h-5 rounded-full border-2 mr-3 flex items-center justify-center ${selectedField === field.id ? 'border-blue-500' : 'border-gray-300'
                                            }`}>
                                            {selectedField === field.id && (
                                                <div className="w-3 h-3 rounded-full bg-blue-500" />
                                            )}
                                        </div>
                                        <span className="text-lg font-medium text-gray-900">
                                            {field.name}
                                        </span>
                                    </div>
                                </label>
                            ))}
                        </div>
                    </div>

                    {error && (
                        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                            <p className="text-sm text-red-600">{error}</p>
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={!selectedField || loading}
                        className="w-full py-3 px-4 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        {loading ? 'Creating Session...' : 'Continue'}
                    </button>
                </form>
            </div>
        </div>
    );
}
