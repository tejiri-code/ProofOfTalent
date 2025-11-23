'use client';

import { useState } from 'react';
import { apiClient } from '@/lib/api';

interface DocumentUploadProps {
    sessionId: string;
    initialFiles?: File[];
    onFilesChange?: (files: File[]) => void;
    onNext: () => void;
    onBack: () => void;
}

export default function DocumentUpload({ sessionId, initialFiles = [], onFilesChange, onNext, onBack }: DocumentUploadProps) {
    const [files, setFiles] = useState<File[]>(initialFiles);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState<string>('');

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            const newFiles = Array.from(e.target.files);
            setFiles(newFiles);
            if (onFilesChange) onFilesChange(newFiles);
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
        const newFiles = files.filter((_, i) => i !== index);
        setFiles(newFiles);
        if (onFilesChange) onFilesChange(newFiles);
    };

    return (
        <div className="max-w-3xl mx-auto">
            <div className="bg-white rounded-2xl shadow-xl p-6 sm:p-8 md:p-10 border border-gray-100">
                <div className="mb-6 sm:mb-8">
                    <h2 className="text-2xl sm:text-2xl md:text-3xl font-bold text-gray-900 mb-2 text-shadow-sm">Upload Documents</h2>
                    <p className="text-sm sm:text-base text-gray-700 font-medium mb-3">
                        Upload your CV, recommendation letters, and portfolio items (PDF or DOCX)
                    </p>
                    <div className="bg-blue-50 border-l-4 border-blue-400 p-3 sm:p-4 rounded-lg">
                        <div className="flex items-start">
                            <svg className="w-4 h-4 sm:w-5 sm:h-5 text-blue-600 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <p className="text-xs sm:text-sm text-blue-800 leading-relaxed">
                                <strong>Privacy Notice:</strong> Your documents are processed securely and encrypted. We do not share your data with third parties. You can request deletion at any time.
                            </p>
                        </div>
                    </div>
                </div>

                <div className="space-y-6 sm:space-y-8">
                    <div className="border-2 border-dashed border-blue-200 rounded-2xl p-8 sm:p-10 text-center bg-blue-50/50 hover:bg-blue-50 transition-colors group">
                        <input
                            type="file"
                            accept=".pdf,.docx"
                            multiple
                            onChange={handleFileChange}
                            className="hidden"
                            id="file-upload"
                        />
                        <label
                            htmlFor="file-upload"
                            className="cursor-pointer flex flex-col items-center justify-center"
                        >
                            <div className="w-14 h-14 sm:w-16 sm:h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                <svg className="w-7 h-7 sm:w-8 sm:h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                </svg>
                            </div>
                            <span className="text-base sm:text-lg font-bold text-blue-600 mb-2 group-hover:text-blue-700">
                                Click to Select PDF or DOCX Files
                            </span>
                            <p className="text-xs sm:text-sm text-gray-500 max-w-sm mx-auto px-2">
                                Upload your CV (1), recommendation letters (3), and other evidence
                            </p>
                        </label>
                    </div>

                    {files.length > 0 && (
                        <div className="space-y-3">
                            <h3 className="font-bold text-base sm:text-lg text-gray-900 flex items-center">
                                <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full mr-2">{files.length}</span>
                                Selected Files
                            </h3>
                            <div className="grid gap-3">
                                {files.map((file, index) => (
                                    <div key={index} className="flex items-center justify-between p-3 w-3/4 md:w-full sm:p-4 bg-white border border-gray-200 rounded-xl hover:shadow-md transition-shadow">
                                        <div className="flex items-center space-x-3 sm:space-x-4 overflow-hidden flex-1 min-w-0">
                                            <div className="w-10 h-10 bg-red-50 rounded-lg flex items-center justify-center flex-shrink-0">
                                                <svg className="w-5 h-5 sm:w-6 sm:h-6 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                                                    <path fillRule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm3 1h6v4H7V5zm6 6H7v2h6v-2z" clipRule="evenodd" />
                                                </svg>
                                            </div>
                                            <div className="min-w-0 flex-1">
                                                <p className="text-sm font-medium text-gray-900 truncate">{file.name}</p>
                                                <p className="text-xs text-gray-500">{(file.size / 1024).toFixed(1)} KB</p>
                                            </div>
                                        </div>
                                        <button
                                            onClick={() => removeFile(index)}
                                            className="p-2 sm:p-2.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors flex-shrink-0 ml-2 min-w-[44px] min-h-[44px] flex items-center justify-center"
                                            title="Remove file"
                                            aria-label="Remove file"
                                        >
                                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                            </svg>
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {error && (
                        <div className="p-4 bg-red-50 border border-red-200 rounded-xl flex items-start">
                            <svg className="w-5 h-5 text-red-500 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <p className="text-sm text-red-600">{error}</p>
                        </div>
                    )}

                    <div className="flex flex-col-reverse sm:flex-row gap-3 sm:gap-4 pt-2 sm:pt-4">
                        <button
                            type="button"
                            onClick={onBack}
                            className="w-full sm:w-auto px-6 sm:px-8 py-3.5 sm:py-4 border-2 border-gray-200 text-gray-700 font-bold rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all min-h-[48px]"
                        >
                            Back
                        </button>
                        <button
                            onClick={handleUpload}
                            disabled={files.length === 0 || uploading}
                            className="flex-1 py-3.5 sm:py-4 px-6 sm:px-8 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 disabled:opacity-50 transition-all shadow-lg shadow-blue-200 hover:shadow-blue-300 transform hover:-translate-y-0.5 min-h-[48px]"
                        >
                            {uploading ? (
                                <span className="flex items-center justify-center">
                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Uploading...
                                </span>
                            ) : `Upload ${files.length} File${files.length !== 1 ? 's' : ''}`}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
