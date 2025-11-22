'use client';

import { useState } from 'react';
import { apiClient } from '@/lib/api';

interface DocumentUploadProps {
    sessionId: string;
    onNext: () => void;
    onBack: () => void;
}

export default function DocumentUpload({ sessionId, onNext, onBack }: DocumentUploadProps) {
    const [files, setFiles] = useState<File[]>([]);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState<string>('');

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFiles(Array.from(e.target.files));
        }
    };

    const handleUpload = async () => {
        if (files.length === 0) {
            setError('Please select at least one file');
            return;
        }

        setUploading(true);
        setError('');

        try {
            await apiClient.uploadDocuments(sessionId, files);
            onNext();
        } catch (err) {
            setError('Failed to upload documents');
        } finally {
            setUploading(false);
        }
    };

    const removeFile = (index: number) => {
        setFiles(files.filter((_, i) => i !== index));
    };

    return (
        <div className="max-w-3xl mx-auto p-6">
            <div className="bg-white rounded-lg shadow-lg p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Upload Documents</h2>
                <p className="text-gray-600 mb-6">
                    Upload your CV, recommendation letters, and portfolio items (PDF only)
                </p>

                <div className="space-y-6">
                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                        <input
                            type="file"
                            accept=".pdf"
                            multiple
                            onChange={handleFileChange}
                            className="hidden"
                            id="file-upload"
                        />
                        <label
                            htmlFor="file-upload"
                            className="cursor-pointer inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
                        >
                            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                            </svg>
                            Select PDF Files
                        </label>
                        <p className="mt-2 text-sm text-gray-500">
                            Upload your CV (1), recommendation letters (3), and other evidence
                        </p>
                    </div>

                    {files.length > 0 && (
                        <div className="space-y-2">
                            <h3 className="font-medium text-gray-900">Selected Files ({files.length})</h3>
                            {files.map((file, index) => (
                                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                    <div className="flex items-center space-x-3">
                                        <svg className="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm3 1h6v4H7V5zm6 6H7v2h6v-2z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-700">{file.name}</span>
                                        <span className="text-xs text-gray-500">({(file.size / 1024).toFixed(1)} KB)</span>
                                    </div>
                                    <button
                                        onClick={() => removeFile(index)}
                                        className="text-red-600 hover:text-red-700"
                                    >
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                        </svg>
                                    </button>
                                </div>
                            ))}
                        </div>
                    )}

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
                            onClick={handleUpload}
                            disabled={files.length === 0 || uploading}
                            className="flex-1 py-3 px-4 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
                        >
                            {uploading ? 'Uploading...' : `Upload ${files.length} File${files.length !== 1 ? 's' : ''}`}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
