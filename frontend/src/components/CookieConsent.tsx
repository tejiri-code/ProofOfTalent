'use client';

import { useState, useEffect } from 'react';

export default function CookieConsent() {
    const [showBanner, setShowBanner] = useState(false);
    const [showSettings, setShowSettings] = useState(false);
    const [preferences, setPreferences] = useState({
        necessary: true, // Always true, can't be disabled
        analytics: false,
        marketing: false
    });

    useEffect(() => {
        // Check if user has already made a choice
        const consent = localStorage.getItem('cookieConsent');
        if (!consent) {
            // Show banner after a short delay for better UX
            setTimeout(() => setShowBanner(true), 1000);
        } else {
            // Load saved preferences
            try {
                const saved = JSON.parse(consent);
                setPreferences(prev => ({ ...prev, ...saved }));
            } catch (e) {
                // Invalid JSON, show banner
                setShowBanner(true);
            }
        }
    }, []);

    const handleAcceptAll = () => {
        const allAccepted = {
            necessary: true,
            analytics: true,
            marketing: true
        };
        setPreferences(allAccepted);
        localStorage.setItem('cookieConsent', JSON.stringify(allAccepted));
        localStorage.setItem('cookieConsentDate', new Date().toISOString());
        setShowBanner(false);
        setShowSettings(false);
    };

    const handleRejectAll = () => {
        const onlyNecessary = {
            necessary: true,
            analytics: false,
            marketing: false
        };
        setPreferences(onlyNecessary);
        localStorage.setItem('cookieConsent', JSON.stringify(onlyNecessary));
        localStorage.setItem('cookieConsentDate', new Date().toISOString());
        setShowBanner(false);
        setShowSettings(false);
    };

    const handleSavePreferences = () => {
        localStorage.setItem('cookieConsent', JSON.stringify(preferences));
        localStorage.setItem('cookieConsentDate', new Date().toISOString());
        setShowBanner(false);
        setShowSettings(false);
    };

    if (!showBanner) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-in fade-in duration-300">
            <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full border border-gray-200 animate-in slide-in-from-bottom duration-300">
                {!showSettings ? (
                    // Main Banner
                    <div className="p-6 sm:p-8">
                        <div className="flex items-start mb-4">
                            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-blue-100 rounded-xl flex items-center justify-center mr-4 flex-shrink-0">
                                <svg className="w-6 h-6 sm:w-7 sm:h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                                </svg>
                            </div>
                            <div className="flex-1">
                                <h3 className="text-xl sm:text-2xl font-bold text-gray-900 mb-2">Cookie Preferences</h3>
                                <p className="text-sm sm:text-base text-gray-700 leading-relaxed">
                                    We use cookies to provide essential functionality and improve your experience. We do not use advertising or tracking cookies. You can customize your preferences below.
                                </p>
                            </div>
                        </div>

                        <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-lg mb-6">
                            <p className="text-xs sm:text-sm text-blue-800">
                                <strong>Essential cookies only:</strong> We only use necessary cookies to maintain your session and provide our service. No personal data is shared with third parties for marketing.
                            </p>
                        </div>

                        <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
                            <button
                                onClick={handleAcceptAll}
                                className="flex-1 py-3 px-6 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition-all shadow-lg shadow-blue-200 hover:shadow-blue-300 transform hover:-translate-y-0.5 min-h-[48px]"
                            >
                                Accept All
                            </button>
                            <button
                                onClick={handleRejectAll}
                                className="flex-1 py-3 px-6 bg-white border-2 border-gray-200 text-gray-700 font-bold rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all min-h-[48px]"
                            >
                                Reject All
                            </button>
                            <button
                                onClick={() => setShowSettings(true)}
                                className="flex-1 py-3 px-6 bg-white border-2 border-gray-200 text-gray-700 font-bold rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all min-h-[48px]"
                            >
                                Customize
                            </button>
                        </div>

                        <p className="text-xs text-gray-500 mt-4 text-center">
                            By continuing to use our site, you agree to our use of cookies. See our{' '}
                            <a href="/privacy-policy" className="text-blue-600 hover:text-blue-700 underline">Privacy Policy</a> for details.
                        </p>
                    </div>
                ) : (
                    // Settings Panel
                    <div className="p-6 sm:p-8">
                        <div className="flex items-center justify-between mb-6">
                            <h3 className="text-xl sm:text-2xl font-bold text-gray-900">Cookie Settings</h3>
                            <button
                                onClick={() => setShowSettings(false)}
                                className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
                                aria-label="Close settings"
                            >
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>

                        <div className="space-y-4 mb-6">
                            {/* Necessary Cookies */}
                            <div className="bg-gray-50 p-4 rounded-xl border border-gray-200">
                                <div className="flex items-center justify-between mb-2">
                                    <h4 className="font-bold text-gray-900">Necessary Cookies</h4>
                                    <div className="flex items-center">
                                        <span className="text-xs text-gray-500 mr-2">Always Active</span>
                                        <div className="w-10 h-6 bg-blue-600 rounded-full flex items-center px-1">
                                            <div className="w-4 h-4 bg-white rounded-full ml-auto"></div>
                                        </div>
                                    </div>
                                </div>
                                <p className="text-sm text-gray-600">
                                    Required for the website to function. These cookies maintain your session and cannot be disabled.
                                </p>
                            </div>

                            {/* Analytics Cookies */}
                            <div className="bg-gray-50 p-4 rounded-xl border border-gray-200">
                                <div className="flex items-center justify-between mb-2">
                                    <h4 className="font-bold text-gray-900">Analytics Cookies</h4>
                                    <button
                                        onClick={() => setPreferences(prev => ({ ...prev, analytics: !prev.analytics }))}
                                        className={`w-10 h-6 rounded-full flex items-center px-1 transition-colors ${preferences.analytics ? 'bg-blue-600' : 'bg-gray-300'}`}
                                        aria-label="Toggle analytics cookies"
                                    >
                                        <div className={`w-4 h-4 bg-white rounded-full transition-transform ${preferences.analytics ? 'ml-auto' : ''}`}></div>
                                    </button>
                                </div>
                                <p className="text-sm text-gray-600">
                                    Help us understand how visitors use our site to improve user experience. No personal data is collected.
                                </p>
                            </div>

                            {/* Marketing Cookies */}
                            <div className="bg-gray-50 p-4 rounded-xl border border-gray-200 opacity-50">
                                <div className="flex items-center justify-between mb-2">
                                    <h4 className="font-bold text-gray-900">Marketing Cookies</h4>
                                    <div className="flex items-center">
                                        <span className="text-xs text-gray-500 mr-2">Not Used</span>
                                        <div className="w-10 h-6 bg-gray-300 rounded-full flex items-center px-1">
                                            <div className="w-4 h-4 bg-white rounded-full"></div>
                                        </div>
                                    </div>
                                </div>
                                <p className="text-sm text-gray-600">
                                    We do not use marketing or advertising cookies.
                                </p>
                            </div>
                        </div>

                        <div className="flex flex-col sm:flex-row gap-3">
                            <button
                                onClick={handleSavePreferences}
                                className="flex-1 py-3 px-6 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition-all shadow-lg shadow-blue-200 hover:shadow-blue-300 min-h-[48px]"
                            >
                                Save Preferences
                            </button>
                            <button
                                onClick={() => setShowSettings(false)}
                                className="flex-1 py-3 px-6 bg-white border-2 border-gray-200 text-gray-700 font-bold rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all min-h-[48px]"
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
