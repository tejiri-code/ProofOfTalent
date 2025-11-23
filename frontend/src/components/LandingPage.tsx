import Image from 'next/image';
import PrivacyFooter from './PrivacyFooter';

interface LandingPageProps {
    onStart: () => void;
}

export default function LandingPage({ onStart }: LandingPageProps) {
    return (
        <div className="min-h-screen flex flex-col pt-10 overflow-y-hidden">
            {/* Hero Section */}
            <section className="flex-1 flex flex-col justify-center items-center text-center px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-blue-50/50 via-white to-white relative overflow-hidden">
                {/* Background Elements */}
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full max-w-7xl pointer-events-none">
                    <div className="absolute top-10 sm:top-20 left-5 sm:left-10 w-48 h-48 sm:w-72 sm:h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
                    <div className="absolute top-10 sm:top-20 right-5 sm:right-10 w-48 h-48 sm:w-72 sm:h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
                    <div className="absolute -bottom-8 left-1/2 w-48 h-48 sm:w-72 sm:h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
                </div>

                <div className="relative z-10 max-w-4xl mx-auto space-y-6 sm:space-y-8 py-12 sm:py-16 md:py-20">
                    {/* <div className="relative w-24 h-24 mx-auto mb-8">
                        <Image
                            src="/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png"
                            alt="GtCompass Logo"
                            fill
                            className="object-contain drop-shadow-xl"
                            priority
                        />
                    </div> */}

                    <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight text-gray-900 text-shadow-sm px-2">
                        Validate Your <br className="hidden sm:block" />
                        <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 animate-gradient">
                            Global Talent Potential
                        </span>
                    </h1>

                    <p className="text-lg sm:text-xl md:text-2xl text-gray-700 max-w-2xl mx-auto leading-relaxed font-medium px-2">
                        AI-powered assessment for the <span className="text-blue-600 font-semibold">UK Global Talent Visa</span>.
                        Get a detailed evidence gap analysis and strategic roadmap in minutes.
                    </p>

                    <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-center gap-3 sm:gap-4 pt-2 sm:pt-4 px-4">
                        <button
                            onClick={onStart}
                            className="w-full sm:w-auto px-8 sm:px-10 md:px-12 py-4 bg-blue-600 text-white text-base sm:text-lg font-bold rounded-full hover:bg-blue-700 transition-all shadow-lg shadow-blue-200 hover:shadow-blue-300 transform hover:-translate-y-1 cursor-pointer min-h-[48px]"
                        >
                            Check My Eligibility
                        </button>
                        {/* <button className="px-8 py-4 bg-white text-gray-700 text-lg font-bold rounded-full border-2 border-gray-100 hover:border-gray-200 hover:bg-gray-50 transition-all w-full sm:w-auto">
                            Learn More
                        </button> */}
                    </div>

                    <div className="pt-8 sm:pt-12 grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6 md:gap-8 text-left max-w-3xl mx-auto">
                        <div className="bg-white/50 backdrop-blur-sm p-5 sm:p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-3 sm:mb-4 text-blue-600">
                                <svg className="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                            </div>
                            <h3 className="font-bold text-base sm:text-lg text-gray-900 mb-2">Instant Analysis</h3>
                            <p className="text-sm text-gray-700 leading-relaxed">Get immediate feedback on your profile's strength against official visa criteria.</p>
                        </div>
                        <div className="bg-white/50 backdrop-blur-sm p-5 sm:p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-3 sm:mb-4 text-purple-600">
                                <svg className="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                                </svg>
                            </div>
                            <h3 className="font-bold text-base sm:text-lg text-gray-900 mb-2">Gap Identification</h3>
                            <p className="text-sm text-gray-700 leading-relaxed">Pinpoint exactly what evidence is missing or needs improvement in your application.</p>
                        </div>
                        <div className="bg-white/50 backdrop-blur-sm p-5 sm:p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-green-100 rounded-lg flex items-center justify-center mb-3 sm:mb-4 text-green-600">
                                <svg className="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 7m0 13V7" />
                                </svg>
                            </div>
                            <h3 className="font-bold text-base sm:text-lg text-gray-900 mb-2">Strategic Roadmap</h3>
                            <p className="text-sm text-gray-700 leading-relaxed">Receive a step-by-step action plan to build your case and increase success probability.</p>
                        </div>
                    </div>
                </div>

                {/* Legal Disclaimer */}
                <div className="-mt-5 mb-12 max-w-3xl mx-auto">
                    <div className="bg-amber-50 border-l-4 border-amber-400 p-4 sm:p-6 rounded-lg">
                        <div className="flex items-start">
                            <svg className="w-5 h-5 sm:w-6 sm:h-6 text-amber-600 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                            </svg>
                            <div>
                                <h4 className="text-sm sm:text-base font-bold text-amber-900 mb-1">Legal Disclaimer</h4>
                                <p className="text-xs sm:text-sm text-amber-800 leading-relaxed">
                                    This tool provides guidance and recommendations only. It is <strong>not legal advice</strong> and should not be relied upon as such. For official guidance on your visa application, please consult with a qualified immigration lawyer.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <PrivacyFooter />
        </div>
    );
}
