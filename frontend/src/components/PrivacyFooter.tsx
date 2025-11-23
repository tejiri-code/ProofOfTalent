'use client';

import Link from 'next/link';

export default function PrivacyFooter() {
    return (
        <footer className="bg-gray-50 border-t border-gray-200 mt-auto">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {/* Data Protection */}
                    <div>
                        <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4">Data Protection</h3>
                        <ul className="space-y-2 text-sm text-gray-600">
                            <li className="flex items-start">
                                <svg className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                </svg>
                                <span>GDPR Compliant</span>
                            </li>
                            <li className="flex items-start">
                                <svg className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                </svg>
                                <span>End-to-end encryption</span>
                            </li>
                            <li className="flex items-start">
                                <svg className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                </svg>
                                <span>No third-party sharing</span>
                            </li>
                            <li className="flex items-start">
                                <svg className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                </svg>
                                <span>Data deletion on request</span>
                            </li>
                        </ul>
                    </div>

                    {/* Your Rights */}
                    <div>
                        <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4">Your Rights</h3>
                        <ul className="space-y-2 text-sm text-gray-600">
                            <li>• Right to access your data</li>
                            <li>• Right to rectification</li>
                            <li>• Right to erasure</li>
                            <li>• Right to data portability</li>
                            <li>• Right to withdraw consent</li>
                        </ul>
                    </div>

                    {/* How We Use Data */}
                    <div>
                        <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4">How We Use Your Data</h3>
                        <p className="text-sm text-gray-600 leading-relaxed mb-3">
                            We collect and process your data solely to provide visa assessment services. Your information is:
                        </p>
                        <ul className="space-y-2 text-sm text-gray-600">
                            <li>• Stored securely with encryption</li>
                            <li>• Used only for analysis</li>
                            <li>• Never sold or shared</li>
                            <li>• Deleted upon request</li>
                        </ul>
                    </div>
                </div>

                <div className="mt-8 pt-8 border-t border-gray-200">
                    <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
                        <p className="text-xs text-gray-500 text-center sm:text-left">
                            © {new Date().getFullYear()} GtCompass. All rights reserved. This is a guidance tool, not legal advice.
                        </p>
                        <div className="flex gap-4 text-xs text-gray-500">
                            <Link href="/privacy-policy" className="hover:text-gray-700 transition-colors">
                                Privacy Policy
                            </Link>
                            <Link href="/terms" className="hover:text-gray-700 transition-colors">
                                Terms of Service
                            </Link>
                            <a href="mailto:support@gtcompass.com" className="hover:text-gray-700 transition-colors">
                                Contact
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </footer>
    );
}
