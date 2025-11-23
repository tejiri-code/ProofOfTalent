'use client';

export default function PrivacyPolicy() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
                <div className="bg-white rounded-2xl shadow-xl p-6 sm:p-8 md:p-12 border border-gray-100">
                    {/* Header */}
                    <div className="mb-8 sm:mb-12">
                        <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-gray-900 mb-4">Privacy Policy</h1>
                        <p className="text-sm sm:text-base text-gray-600">Last updated: {new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })}</p>
                    </div>

                    {/* Content */}
                    <div className="prose prose-sm sm:prose-base max-w-none space-y-6 sm:space-y-8">
                        {/* Introduction */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">1. Introduction</h2>
                            <p className="text-gray-700 leading-relaxed">
                                GtCompass ("we", "our", or "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our UK Global Talent Visa assessment tool.
                            </p>
                            <div className="bg-amber-50 border-l-4 border-amber-400 p-4 rounded-lg mt-4">
                                <p className="text-sm text-amber-800">
                                    <strong>Important:</strong> GtCompass is a guidance tool and does not provide legal advice. For official immigration guidance, please consult a qualified immigration lawyer.
                                </p>
                            </div>
                        </section>

                        {/* Data Controller */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">2. Data Controller</h2>
                            <p className="text-gray-700 leading-relaxed">
                                GtCompass is the data controller responsible for your personal data. We are committed to complying with the General Data Protection Regulation (GDPR) and UK data protection laws.
                            </p>
                        </section>

                        {/* Information We Collect */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">3. Information We Collect</h2>
                            <p className="text-gray-700 leading-relaxed mb-4">We collect the following types of information:</p>

                            <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3">3.1 Information You Provide</h3>
                            <ul className="list-disc pl-6 space-y-2 text-gray-700">
                                <li><strong>Field Selection:</strong> Your chosen professional field</li>
                                <li><strong>Questionnaire Responses:</strong> Information about your professional achievements, publications, awards, and experience</li>
                                <li><strong>Documents:</strong> CV, recommendation letters, portfolio items (PDF or DOCX format)</li>
                                <li><strong>Portfolio URLs:</strong> Links to your online portfolio or professional profiles</li>
                            </ul>

                            <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3 mt-6">3.2 Automatically Collected Information</h3>
                            <ul className="list-disc pl-6 space-y-2 text-gray-700">
                                <li><strong>Session Data:</strong> Temporary session identifiers to maintain your progress</li>
                                <li><strong>Technical Data:</strong> Browser type, device information, IP address (anonymized)</li>
                            </ul>
                        </section>

                        {/* How We Use Your Information */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">4. How We Use Your Information</h2>
                            <p className="text-gray-700 leading-relaxed mb-4">We use your information solely for the following purposes:</p>
                            <ul className="list-disc pl-6 space-y-2 text-gray-700">
                                <li><strong>Visa Assessment:</strong> To analyze your eligibility for the UK Global Talent Visa</li>
                                <li><strong>AI Analysis:</strong> To process your data using GPT-4 for personalized recommendations</li>
                                <li><strong>Report Generation:</strong> To create your personalized assessment report and roadmap</li>
                                <li><strong>Service Improvement:</strong> To improve our analysis algorithms (anonymized data only)</li>
                            </ul>
                        </section>

                        {/* Legal Basis for Processing */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">5. Legal Basis for Processing</h2>
                            <p className="text-gray-700 leading-relaxed mb-4">Under GDPR, we process your data based on:</p>
                            <ul className="list-disc pl-6 space-y-2 text-gray-700">
                                <li><strong>Consent:</strong> You explicitly consent to data processing when you check the privacy consent box</li>
                                <li><strong>Legitimate Interest:</strong> To provide and improve our assessment service</li>
                            </ul>
                        </section>

                        {/* Data Security */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">6. Data Security</h2>
                            <p className="text-gray-700 leading-relaxed mb-4">We implement industry-standard security measures:</p>
                            <ul className="list-disc pl-6 space-y-2 text-gray-700">
                                <li><strong>Encryption:</strong> All data is encrypted in transit (HTTPS) and at rest</li>
                                <li><strong>Access Control:</strong> Strict access controls limit who can view your data</li>
                                <li><strong>Secure Storage:</strong> Documents are stored in secure, encrypted cloud storage</li>
                                <li><strong>Regular Audits:</strong> We conduct regular security audits and updates</li>
                            </ul>
                        </section>

                        {/* Data Sharing */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">7. Data Sharing and Third Parties</h2>
                            <div className="bg-green-50 border-l-4 border-green-400 p-4 rounded-lg mb-4">
                                <p className="text-sm text-green-800">
                                    <strong>We do not sell, rent, or share your personal data with third parties for marketing purposes.</strong>
                                </p>
                            </div>
                            <p className="text-gray-700 leading-relaxed mb-4">We only share data with:</p>
                            <ul className="list-disc pl-6 space-y-2 text-gray-700">
                                <li><strong>OpenAI:</strong> For AI-powered analysis (subject to their privacy policy and data processing agreement)</li>
                                <li><strong>Cloud Providers:</strong> For secure data storage (AWS/GCP, subject to data processing agreements)</li>
                                <li><strong>Legal Authorities:</strong> Only if required by law or to protect our legal rights</li>
                            </ul>
                        </section>

                        {/* Your Rights */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">8. Your Rights Under GDPR</h2>
                            <p className="text-gray-700 leading-relaxed mb-4">You have the following rights:</p>
                            <div className="grid sm:grid-cols-2 gap-4">
                                <div className="bg-blue-50 p-4 rounded-lg">
                                    <h4 className="font-semibold text-gray-900 mb-2">Right to Access</h4>
                                    <p className="text-sm text-gray-700">Request a copy of your personal data</p>
                                </div>
                                <div className="bg-blue-50 p-4 rounded-lg">
                                    <h4 className="font-semibold text-gray-900 mb-2">Right to Rectification</h4>
                                    <p className="text-sm text-gray-700">Correct inaccurate or incomplete data</p>
                                </div>
                                <div className="bg-blue-50 p-4 rounded-lg">
                                    <h4 className="font-semibold text-gray-900 mb-2">Right to Erasure</h4>
                                    <p className="text-sm text-gray-700">Request deletion of your data</p>
                                </div>
                                <div className="bg-blue-50 p-4 rounded-lg">
                                    <h4 className="font-semibold text-gray-900 mb-2">Right to Data Portability</h4>
                                    <p className="text-sm text-gray-700">Receive your data in a portable format</p>
                                </div>
                                <div className="bg-blue-50 p-4 rounded-lg">
                                    <h4 className="font-semibold text-gray-900 mb-2">Right to Object</h4>
                                    <p className="text-sm text-gray-700">Object to certain types of processing</p>
                                </div>
                                <div className="bg-blue-50 p-4 rounded-lg">
                                    <h4 className="font-semibold text-gray-900 mb-2">Right to Withdraw Consent</h4>
                                    <p className="text-sm text-gray-700">Withdraw consent at any time</p>
                                </div>
                            </div>
                        </section>

                        {/* Data Retention */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">9. Data Retention</h2>
                            <p className="text-gray-700 leading-relaxed">
                                We retain your data for as long as necessary to provide our services. Session data is automatically deleted after 30 days of inactivity. You can request immediate deletion of your data at any time by contacting us or using the data deletion feature in your account.
                            </p>
                        </section>

                        {/* Cookies */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">10. Cookies and Tracking</h2>
                            <p className="text-gray-700 leading-relaxed mb-4">
                                We use essential cookies to maintain your session and provide our services. We do not use advertising or tracking cookies. You can manage cookie preferences through our cookie consent banner.
                            </p>
                        </section>

                        {/* International Transfers */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">11. International Data Transfers</h2>
                            <p className="text-gray-700 leading-relaxed">
                                Your data may be processed in countries outside the UK/EEA. We ensure appropriate safeguards are in place, including Standard Contractual Clauses (SCCs) and adequacy decisions.
                            </p>
                        </section>

                        {/* Children's Privacy */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">12. Children's Privacy</h2>
                            <p className="text-gray-700 leading-relaxed">
                                Our service is not intended for individuals under 18 years of age. We do not knowingly collect data from children.
                            </p>
                        </section>

                        {/* Changes to Policy */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">13. Changes to This Policy</h2>
                            <p className="text-gray-700 leading-relaxed">
                                We may update this Privacy Policy from time to time. We will notify you of any material changes by posting the new policy on this page and updating the "Last updated" date.
                            </p>
                        </section>

                        {/* Contact */}
                        <section>
                            <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">14. Contact Us</h2>
                            <p className="text-gray-700 leading-relaxed mb-4">
                                If you have questions about this Privacy Policy or wish to exercise your rights, please contact us:
                            </p>
                            <div className="bg-gray-50 p-4 sm:p-6 rounded-lg border border-gray-200">
                                <p className="text-gray-700"><strong>Email:</strong> privacy@gtcompass.com</p>
                                <p className="text-gray-700 mt-2"><strong>Data Protection Officer:</strong> dpo@gtcompass.com</p>
                                <p className="text-gray-700 mt-4 text-sm">
                                    You also have the right to lodge a complaint with the Information Commissioner's Office (ICO) if you believe your data protection rights have been violated.
                                </p>
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
