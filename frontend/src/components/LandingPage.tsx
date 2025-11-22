import Image from 'next/image';

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
                    <div className="absolute top-20 left-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
                    <div className="absolute top-20 right-10 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
                    <div className="absolute -bottom-8 left-1/2 w-72 h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
                </div>

                <div className="relative z-10 max-w-4xl mx-auto space-y-8 py-20">
                    {/* <div className="relative w-24 h-24 mx-auto mb-8">
                        <Image
                            src="/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png"
                            alt="Proof of Talent Logo"
                            fill
                            className="object-contain drop-shadow-xl"
                            priority
                        />
                    </div> */}

                    <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-gray-900">
                        Validate Your <br />
                        <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                            Global Talent Potential
                        </span>
                    </h1>

                    <p className="text-xl md:text-2xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
                        AI-powered assessment for the UK Global Talent Visa.
                        Get a detailed evidence gap analysis and strategic roadmap in minutes.
                    </p>

                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
                        <button
                            onClick={onStart}
                            className="px-8 py-4 bg-blue-600 text-white text-lg font-bold rounded-full hover:bg-blue-700 transition-all shadow-lg shadow-blue-200 hover:shadow-blue-300 transform hover:-translate-y-1 w-full sm:w-auto"
                        >
                            Check My Eligibility
                        </button>
                        {/* <button className="px-8 py-4 bg-white text-gray-700 text-lg font-bold rounded-full border-2 border-gray-100 hover:border-gray-200 hover:bg-gray-50 transition-all w-full sm:w-auto">
                            Learn More
                        </button> */}
                    </div>

                    <div className="pt-12 grid grid-cols-1 md:grid-cols-3 gap-8 text-left max-w-3xl mx-auto">
                        <div className="bg-white/50 backdrop-blur-sm p-6 rounded-2xl border border-gray-100 shadow-sm">
                            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-4 text-blue-600">
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                            </div>
                            <h3 className="font-bold text-gray-900 mb-2">Instant Analysis</h3>
                            <p className="text-sm text-gray-600">Get immediate feedback on your profile's strength against official visa criteria.</p>
                        </div>
                        <div className="bg-white/50 backdrop-blur-sm p-6 rounded-2xl border border-gray-100 shadow-sm">
                            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mb-4 text-purple-600">
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                                </svg>
                            </div>
                            <h3 className="font-bold text-gray-900 mb-2">Gap Identification</h3>
                            <p className="text-sm text-gray-600">Pinpoint exactly what evidence is missing or needs improvement in your application.</p>
                        </div>
                        <div className="bg-white/50 backdrop-blur-sm p-6 rounded-2xl border border-gray-100 shadow-sm">
                            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mb-4 text-green-600">
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 7m0 13V7" />
                                </svg>
                            </div>
                            <h3 className="font-bold text-gray-900 mb-2">Strategic Roadmap</h3>
                            <p className="text-sm text-gray-600">Receive a step-by-step action plan to build your case and increase success probability.</p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
