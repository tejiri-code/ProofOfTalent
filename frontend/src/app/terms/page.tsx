'use client';

export default function TermsOfService() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
                <div className="bg-white rounded-2xl shadow-xl p-6 sm:p-8 md:p-12 border border-gray-100">
                    {/* Header */}
                    <div className="mb-8 sm:mb-12">
                        <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-gray-900 mb-4">Terms of Service</h1>
                        <p className="text-sm sm:text-base text-gray-600">Last updated: {new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })}</p>
                    </div>

                    {/* Content */}
                    <div className="prose prose-sm sm:prose-base max-w-none space-y-6 sm:space-y-8">
                        {/* Acceptance */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">1. Acceptance of Terms</h2>
                            <p className="text-gray-700 leading-relaxed">
                                By accessing and using GtCompass ("the Service"), you accept and agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use the Service.
                            </p>
                        </section>

                        {/* Service Description */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">2. Service Description</h2>
                            <p className="text-gray-700 leading-relaxed mb-4">
                                GtCompass is an AI-powered assessment tool designed to help users evaluate their eligibility for the UK Global Talent Visa. The Service provides:
                            </p>
                            <ul className="list-disc pl-6 space-y-2 text-gray-700">
                                <li>Analysis of your professional profile and achievements</li>
                                <li>Assessment of visa eligibility likelihood</li>
                                <li>Personalized recommendations and roadmap</li>
                                <li>Downloadable assessment reports</li>
                            </ul>
                        </section>

                        {/* Not Legal Advice */}
                        <section>
                            <div className="bg-red-50 border-l-4 border-red-400 p-4 sm:p-6 rounded-lg">
                                <h2 className="text-xl sm:text-2xl font-bold text-red-900 mb-4">3. Not Legal Advice - Important Disclaimer</h2>
                                <div className="space-y-3 text-red-800">
                                    <p className="font-semibold">
                                        GtCompass is a guidance tool ONLY and does NOT provide legal advice.
                                    </p>
                                    <p>
                                        The assessments, recommendations, and reports provided by this Service are for informational and guidance purposes only. They should not be relied upon as legal advice or as a substitute for professional immigration counsel.
                                    </p>
                                    <p>
                                        <strong>You should always consult with a qualified immigration lawyer</strong> before making any decisions regarding your visa application.
                                    </p>
                                    <p className="text-sm">
                                        We make no guarantees about visa approval outcomes. Immigration decisions are made solely by UK Visas and Immigration (UKVI) and are subject to their criteria and discretion.
                                    </p>
                                </div>
                            </div>
                        </section>

                        {/* User Responsibilities */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">4. User Responsibilities</h2>
                            <p className="text-gray-700 leading-relaxed mb-4">By using the Service, you agree to:</p>
                            <ul className="list-disc pl-6 space-y-2 text-gray-700">
                                <li>Provide accurate and truthful information</li>
                                <li>Use the Service only for lawful purposes</li>
                                <li>Not attempt to circumvent security measures</li>
                                <li>Not upload malicious files or content</li>
                                <li>Respect intellectual property rights</li>
                                <li>Not misrepresent the Service's capabilities to others</li>
                            </ul>
                        </section>

                        {/* Accuracy and Limitations */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">5. Accuracy and Limitations</h2>
                            <p className="text-gray-700 leading-relaxed mb-4">
                                While we strive for accuracy, we cannot guarantee:
                            </p>
                            <ul className="list-disc pl-6 space-y-2 text-gray-700">
                                <li>100% accuracy of AI-generated assessments</li>
                                <li>That our analysis reflects the most current UKVI criteria</li>
                                <li>Visa approval or any specific outcome</li>
                                <li>Completeness of recommendations</li>
                            </ul>
                            <p className="text-gray-700 leading-relaxed mt-4">
                                Immigration rules and criteria change frequently. Always verify information with official UKVI sources and immigration professionals.
                            </p>
                        </section>

                        {/* Intellectual Property */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">6. Intellectual Property</h2>
                            <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3">6.1 Our Rights</h3>
                            <p className="text-gray-700 leading-relaxed mb-4">
                                All content, features, and functionality of the Service (including but not limited to software, text, displays, images, and design) are owned by GtCompass and are protected by copyright, trademark, and other intellectual property laws.
                            </p>

                            <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3">6.2 Your Rights</h3>
                            <p className="text-gray-700 leading-relaxed">
                                You retain all rights to the content you upload (CV, documents, etc.). By using the Service, you grant us a limited license to process your content solely for providing the assessment service.
                            </p>
                        </section>

                        {/* Liability */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">7. Limitation of Liability</h2>
                            <div className="bg-gray-50 p-4 sm:p-6 rounded-lg border border-gray-200">
                                <p className="text-gray-700 leading-relaxed mb-4">
                                    <strong>TO THE MAXIMUM EXTENT PERMITTED BY LAW:</strong>
                                </p>
                                <ul className="list-disc pl-6 space-y-2 text-gray-700">
                                    <li>The Service is provided "AS IS" without warranties of any kind</li>
                                    <li>We are not liable for any visa application outcomes</li>
                                    <li>We are not liable for decisions made based on our assessments</li>
                                    <li>We are not liable for any indirect, incidental, or consequential damages</li>
                                    <li>Our total liability shall not exceed the amount you paid for the Service (if applicable)</li>
                                </ul>
                            </div>
                        </section>

                        {/* Data and Privacy */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">8. Data and Privacy</h2>
                            <p className="text-gray-700 leading-relaxed">
                                Your use of the Service is also governed by our <a href="/privacy-policy" className="text-blue-600 hover:text-blue-700 underline">Privacy Policy</a>. By using the Service, you consent to our data practices as described in the Privacy Policy.
                            </p>
                        </section>

                        {/* Service Availability */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">9. Service Availability</h2>
                            <p className="text-gray-700 leading-relaxed">
                                We strive to maintain service availability but do not guarantee uninterrupted access. We reserve the right to modify, suspend, or discontinue the Service at any time without notice.
                            </p>
                        </section>

                        {/* Termination */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">10. Termination</h2>
                            <p className="text-gray-700 leading-relaxed">
                                We may terminate or suspend your access to the Service immediately, without prior notice, for any reason, including breach of these Terms. You may stop using the Service at any time.
                            </p>
                        </section>

                        {/* Indemnification */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">11. Indemnification</h2>
                            <p className="text-gray-700 leading-relaxed">
                                You agree to indemnify and hold harmless GtCompass from any claims, damages, or expenses arising from your use of the Service or violation of these Terms.
                            </p>
                        </section>

                        {/* Governing Law */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">12. Governing Law</h2>
                            <p className="text-gray-700 leading-relaxed">
                                These Terms shall be governed by and construed in accordance with the laws of England and Wales. Any disputes shall be subject to the exclusive jurisdiction of the courts of England and Wales.
                            </p>
                        </section>

                        {/* Changes to Terms */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">13. Changes to Terms</h2>
                            <p className="text-gray-700 leading-relaxed">
                                We reserve the right to modify these Terms at any time. We will notify users of material changes by posting the updated Terms on this page. Continued use of the Service after changes constitutes acceptance of the new Terms.
                            </p>
                        </section>

                        {/* Severability */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">14. Severability</h2>
                            <p className="text-gray-700 leading-relaxed">
                                If any provision of these Terms is found to be unenforceable, the remaining provisions will continue in full force and effect.
                            </p>
                        </section>

                        {/* Contact */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">15. Contact Information</h2>
                            <p className="text-gray-700 leading-relaxed mb-4">
                                If you have questions about these Terms, please contact us:
                            </p>
                            <div className="bg-gray-50 p-4 sm:p-6 rounded-lg border border-gray-200">
                                <p className="text-gray-700"><strong>Email:</strong> legal@gtcompass.com</p>
                                <p className="text-gray-700 mt-2"><strong>Support:</strong> support@gtcompass.com</p>
                            </div>
                        </section>
                    </div>

                    {/* Back Button */}
                    <div className="mt-8 sm:mt-12 pt-8 border-t border-gray-200">
                        <a
                            href="/"
                            className="inline-flex items-center text-blue-600 hover:text-blue-700 font-medium transition-colors"
                        >
                            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                            </svg>
                            Back to Home
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
}
