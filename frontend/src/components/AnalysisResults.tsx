'use client';

import { useState, useEffect } from 'react';
import { apiClient, type AnalysisResult } from '@/lib/api';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

interface AnalysisResultsProps {
    sessionId: string;
    onNewStart: () => void;
}

export default function AnalysisResults({ sessionId, onNewStart }: AnalysisResultsProps) {
    const [results, setResults] = useState<AnalysisResult | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string>('');
    const [showDeleteDialog, setShowDeleteDialog] = useState(false);
    const [deleting, setDeleting] = useState(false);

    const [loadingStep, setLoadingStep] = useState(0);
    const [progress, setProgress] = useState(0);

    const ANALYSIS_STEPS = [
        "Analyzing CV content and structure...",
        "Extracting key skills and achievements...",
        "Matching against Global Talent Visa criteria...",
        "Identifying evidence gaps...",
        "Generating personalized roadmap..."
    ];

    useEffect(() => {
        if (!loading) return;

        // Simulate progress
        const interval = setInterval(() => {
            setProgress(prev => {
                if (prev >= 95) return prev;
                return prev + 1;
            });
        }, 100);

        // Simulate steps
        const stepInterval = setInterval(() => {
            setLoadingStep(prev => {
                if (prev >= ANALYSIS_STEPS.length - 1) return prev;
                return prev + 1;
            });
        }, 2000);

        return () => {
            clearInterval(interval);
            clearInterval(stepInterval);
        };
    }, [loading]);

    useEffect(() => {
        const runAnalysis = async () => {
            try {
                // Start analysis
                await apiClient.analyzeApplication(sessionId);

                // Poll for results
                const checkResults = async () => {
                    const data = await apiClient.getResults(sessionId);
                    if (data.status === 'completed' && data.results) {
                        setProgress(100);
                        setTimeout(() => {
                            setResults(data);
                            setLoading(false);
                        }, 500); // Small delay to show 100%
                    } else if (data.status === 'error') {
                        setError('Analysis failed. Please try again.');
                        setLoading(false);
                    } else {
                        // Still processing, check again in 2 seconds
                        setTimeout(checkResults, 2000);
                    }
                };

                checkResults();
            } catch (err) {
                setError('Failed to start analysis');
                setLoading(false);
            }
        };

        runAnalysis();
    }, [sessionId]);

    const generatePDF = () => {
        if (!results?.results) return;

        const doc = new jsPDF();
        const pageWidth = doc.internal.pageSize.width;
        const margin = 20;
        let yPos = 20;

        // Helper for centered text
        const centerText = (text: string, y: number, size: number = 12, font: string = 'helvetica', style: string = 'normal') => {
            doc.setFont(font, style);
            doc.setFontSize(size);
            const textWidth = doc.getTextWidth(text);
            doc.text(text, (pageWidth - textWidth) / 2, y);
        };

        // Header
        doc.setFillColor(37, 99, 235); // Blue-600
        doc.rect(0, 0, pageWidth, 40, 'F');
        doc.setTextColor(255, 255, 255);
        centerText('Global Talent Visa Assessment', 25, 22, 'helvetica', 'bold');

        yPos = 50;
        doc.setTextColor(0, 0, 0);

        // Overall Score
        doc.setFontSize(16);
        doc.setFont('helvetica', 'bold');
        doc.text('Overall Assessment', margin, yPos);
        yPos += 10;

        doc.setFontSize(12);
        doc.setFont('helvetica', 'normal');
        doc.text(`Likelihood of Success: ${(results.results.analysis.likelihood * 100).toFixed(0)}%`, margin, yPos);
        yPos += 7;
        doc.text(`Assessment Level: ${results.results.analysis.assessment_level}`, margin, yPos);
        yPos += 10;

        // Assessment Text
        const splitAssessment = doc.splitTextToSize(results.results.analysis.overall_assessment, pageWidth - (margin * 2));
        doc.text(splitAssessment, margin, yPos);
        yPos += (splitAssessment.length * 7) + 10;

        // Portfolio Analysis Section (if available)
        if (results.results.analysis.portfolio_summary && results.results.analysis.portfolio_summary.accessible) {
            // Check if we need a new page
            if (yPos > 240) {
                doc.addPage();
                yPos = 20;
            }

            doc.setFontSize(16);
            doc.setFont('helvetica', 'bold');
            doc.text('Portfolio Analysis', margin, yPos);
            yPos += 10;

            // Portfolio URL
            if (results.results.analysis.portfolio_summary.url) {
                doc.setFontSize(10);
                doc.setFont('helvetica', 'normal');
                doc.setTextColor(100, 100, 100);
                doc.text('Portfolio URL:', margin, yPos);
                yPos += 5;
                doc.setTextColor(0, 0, 255);
                doc.textWithLink(results.results.analysis.portfolio_summary.url, margin, yPos, { url: results.results.analysis.portfolio_summary.url });
                yPos += 10;
                doc.setTextColor(0, 0, 0);
            }

            // Key Findings
            if (results.results.analysis.portfolio_summary.key_findings && results.results.analysis.portfolio_summary.key_findings.length > 0) {
                doc.setFontSize(12);
                doc.setFont('helvetica', 'bold');
                doc.text('Key Findings:', margin, yPos);
                yPos += 7;

                doc.setFontSize(10);
                doc.setFont('helvetica', 'normal');
                results.results.analysis.portfolio_summary.key_findings.forEach((finding, idx) => {
                    const splitFinding = doc.splitTextToSize(`${idx + 1}. ${finding}`, pageWidth - (margin * 2 + 5));
                    doc.text(splitFinding, margin + 5, yPos);
                    yPos += (splitFinding.length * 5) + 3;
                });
                yPos += 5;
            }

            // Portfolio Strengths and Gaps Table
            const portfolioData: string[][] = [];
            if (results.results.analysis.portfolio_summary.strengths_from_portfolio || results.results.analysis.portfolio_summary.gaps_from_portfolio) {
                portfolioData.push([
                    results.results.analysis.portfolio_summary.strengths_from_portfolio || 'N/A',
                    results.results.analysis.portfolio_summary.gaps_from_portfolio || 'N/A'
                ]);

                autoTable(doc, {
                    startY: yPos,
                    head: [['Portfolio Strengths', 'Portfolio Improvements']],
                    body: portfolioData,
                    headStyles: { fillColor: [147, 51, 234] }, // Purple color
                    theme: 'grid',
                    styles: { cellPadding: 5, fontSize: 9 }
                });

                // @ts-ignore
                yPos = doc.lastAutoTable.finalY + 15;
            }
        }

        // CV Analysis (New Section)
        if (results.results.analysis.cv_feedback) {
            doc.setFontSize(16);
            doc.setFont('helvetica', 'bold');
            doc.text('CV Specific Analysis', margin, yPos);
            yPos += 10;

            doc.setFontSize(12);
            doc.setFont('helvetica', 'normal');
            doc.text(`CV Quality Score: ${results.results.analysis.cv_feedback.score}/10`, margin, yPos);
            yPos += 10;

            autoTable(doc, {
                startY: yPos,
                head: [['CV Strengths', 'Areas for Improvement']],
                body: [
                    [
                        results.results.analysis.cv_feedback.strengths.map(s => `• ${s}`).join('\n'),
                        results.results.analysis.cv_feedback.weaknesses.map(w => `• ${w}`).join('\n')
                    ]
                ],
                headStyles: { fillColor: [37, 99, 235] },
                theme: 'grid',
                styles: { cellPadding: 5 }
            });

            // @ts-ignore
            yPos = doc.lastAutoTable.finalY + 15;
        }

        // Strengths & Gaps
        doc.setFontSize(16);
        doc.setFont('helvetica', 'bold');
        doc.text('Key Strengths & Gaps', margin, yPos);
        yPos += 10;

        const gapsData = results.results.analysis.gaps.map(g => [g.type.replace(/_/g, ' '), g.severity, g.recommendation]);

        autoTable(doc, {
            startY: yPos,
            head: [['Gap Type', 'Severity', 'Recommendation']],
            body: gapsData,
            headStyles: { fillColor: [220, 38, 38] }, // Red header for gaps
            theme: 'grid',
            styles: { cellPadding: 5 }
        });

        // @ts-ignore
        yPos = doc.lastAutoTable.finalY + 15;

        // Roadmap
        doc.addPage();
        yPos = 20;

        doc.setFontSize(16);
        doc.setFont('helvetica', 'bold');
        doc.text('Strategic Roadmap', margin, yPos);
        yPos += 10;

        const roadmapData = results.results.roadmap.milestones.map(m => [
            m.title,
            `${m.duration_weeks} weeks`,
            m.priority,
            m.description
        ]);

        autoTable(doc, {
            startY: yPos,
            head: [['Milestone', 'Duration', 'Priority', 'Action Items']],
            body: roadmapData,
            headStyles: { fillColor: [5, 150, 105] }, // Green header for roadmap
            theme: 'grid',
            styles: { cellPadding: 5 },
            columnStyles: { 3: { cellWidth: 80 } }
        });

        doc.save(`global-talent-visa-assessment-${new Date().toISOString().split('T')[0]}.pdf`);
    };

    const handleDeleteData = async () => {
        setDeleting(true);
        try {
            // Use the existing session delete endpoint which already works
            const response = await fetch(
                `https://proofoftalent.onrender.com/api/session/${sessionId}`,
                { method: 'DELETE' }
            );

            if (!response.ok) {
                throw new Error('Failed to delete data');
            }

            const result = await response.json();

            // Clear local storage
            localStorage.clear();

            // Show success message
            alert(`✅ Data Deleted Successfully\n\nAll your data has been permanently deleted.\n\n${result.message}`);

            // Redirect to home
            onNewStart();

        } catch (err) {
            console.error('Error deleting data:', err);
            alert('❌ Failed to delete data. Please try again or contact support.');
        } finally {
            setDeleting(false);
            setShowDeleteDialog(false);
        }
    };

    if (loading) {
        return (
            <div className="max-w-2xl mx-auto">
                <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 md:p-12 border border-white/20">
                    <div className="text-center mb-8">
                        <div className="relative w-20 h-20 mx-auto mb-6">
                            <div className="absolute inset-0 border-4 border-blue-100 rounded-full"></div>
                            <div className="absolute inset-0 border-4 border-blue-600 rounded-full border-t-transparent animate-spin"></div>
                        </div>
                        <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-3">Analyzing Your Profile</h2>
                        <p className="text-gray-600 text-lg">Please wait while we process your documents</p>
                    </div>

                    <div className="space-y-8">
                        {/* Progress Bar */}
                        <div className="w-full bg-gray-100 rounded-full h-3 overflow-hidden">
                            <div
                                className="bg-gradient-to-r from-blue-600 to-indigo-600 h-full rounded-full transition-all duration-500 ease-out shadow-[0_0_10px_rgba(37,99,235,0.3)]"
                                style={{ width: `${progress}%` }}
                            ></div>
                        </div>

                        {/* Steps */}
                        <div className="space-y-4">
                            {ANALYSIS_STEPS.map((step, index) => (
                                <div key={index} className="flex items-center space-x-4 transition-all duration-300">
                                    <div className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center transition-colors duration-300 ${index < loadingStep ? 'bg-green-500 text-white shadow-green-200 shadow-md' :
                                        index === loadingStep ? 'bg-blue-500 text-white animate-pulse shadow-blue-200 shadow-md' :
                                            'bg-gray-100 border border-gray-200'
                                        }`}>
                                        {index < loadingStep && (
                                            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                                            </svg>
                                        )}
                                    </div>
                                    <span className={`text-sm md:text-base transition-colors duration-300 ${index <= loadingStep ? 'text-gray-900 font-medium' : 'text-gray-400'
                                        }`}>
                                        {step}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    if (error || !results?.results) {
        return (
            <div className="max-w-2xl mx-auto">
                <div className="bg-white rounded-2xl shadow-xl p-8 md:p-12 text-center">
                    <div className="w-20 h-20 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-6">
                        <svg className="w-10 h-10 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-4">Analysis Failed</h2>
                    <p className="text-gray-600 mb-8">{error}</p>
                    <button
                        onClick={onNewStart}
                        className="w-full md:w-auto px-8 py-3 bg-blue-600 text-white font-medium rounded-xl hover:bg-blue-700 transition-all shadow-lg shadow-blue-200 hover:shadow-blue-300 transform hover:-translate-y-0.5"
                    >
                        Start New Analysis
                    </button>
                </div>
            </div>
        );
    }

    const { analysis, roadmap } = results.results;
    const likelihoodPercent = (analysis.likelihood * 100).toFixed(1);

    return (
        <div className="max-w-5xl mx-auto space-y-6 sm:space-y-8">
            {/* Header Section */}
            <div className="bg-white rounded-2xl shadow-xl p-6 sm:p-8 md:p-10 border border-gray-100 overflow-hidden relative">
                <div className="absolute top-0 right-0 w-48 h-48 sm:w-64 sm:h-64 bg-gradient-to-br from-blue-50 to-purple-50 rounded-bl-full -mr-16 -mt-16 opacity-50"></div>

                <div className="relative flex flex-col items-center gap-6 sm:gap-8">
                    <div className="flex-1 text-center w-full">
                        <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 mb-2">Analysis Complete</h2>
                        <p className="text-sm sm:text-base text-gray-600 mb-4 sm:mb-6">Here's your personalized assessment for the Global Talent Visa</p>

                        <div className="inline-flex items-center px-4 py-2 bg-blue-50 rounded-lg border border-blue-100 mb-4 sm:mb-6">
                            <span className="text-sm sm:text-base text-blue-700 font-medium mr-2">Assessment Level:</span>
                            <span className="text-sm sm:text-base text-blue-900 font-bold">{analysis.assessment_level}</span>
                        </div>

                        <p className="text-sm sm:text-base text-gray-700 leading-relaxed bg-gray-50 p-4 sm:p-6 rounded-xl border border-gray-100">
                            {analysis.overall_assessment}
                        </p>
                    </div>

                    <div className="flex flex-col items-center justify-center bg-white p-4 sm:p-6 rounded-2xl shadow-[0_0_20px_rgba(0,0,0,0.05)] border border-gray-100">
                        <div className="relative w-32 h-32 sm:w-40 sm:h-40 mb-3 sm:mb-4">
                            <svg className="transform -rotate-90 w-full h-full" viewBox="0 0 120 120">
                                <circle cx="60" cy="60" r="54" fill="none" stroke="#f3f4f6" strokeWidth="8" />
                                <circle
                                    cx="60"
                                    cy="60"
                                    r="54"
                                    fill="none"
                                    stroke="#2563eb"
                                    strokeWidth="8"
                                    strokeDasharray={`${analysis.likelihood * 339.292} 339.292`}
                                    strokeLinecap="round"
                                    className="transition-all duration-1000 ease-out"
                                />
                            </svg>
                            <div className="absolute inset-0 flex flex-col items-center justify-center">
                                <span className="text-3xl sm:text-4xl font-bold text-gray-900">{likelihoodPercent}%</span>
                                <span className="text-[10px] sm:text-xs text-gray-500 font-medium uppercase tracking-wide mt-1">Success Rate</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Portfolio Summary Section */}
            {analysis.portfolio_summary && analysis.portfolio_summary.accessible && (
                <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-2xl shadow-xl p-6 sm:p-8 md:p-10 border border-purple-100">
                    <div className="flex items-center mb-4 sm:mb-6">
                        <div className="w-10 h-10 sm:w-12 sm:h-12 bg-purple-600 rounded-xl flex items-center justify-center mr-3 sm:mr-4">
                            <svg className="w-6 h-6 sm:w-7 sm:h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                            </svg>
                        </div>
                        <div>
                            <h3 className="text-xl sm:text-2xl font-bold text-gray-900">Portfolio Analysis</h3>
                            <p className="text-xs sm:text-sm text-gray-600 mt-1">Insights from your online portfolio</p>
                        </div>
                    </div>

                    {analysis.portfolio_summary.url && (
                        <div className="mb-6 bg-white/70 backdrop-blur-sm p-4 rounded-xl border border-purple-200">
                            <span className="text-xs font-bold text-purple-700 uppercase tracking-wide block mb-2">Portfolio URL</span>
                            <a
                                href={analysis.portfolio_summary.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-600 hover:text-blue-700 font-medium break-all flex items-center group"
                            >
                                {analysis.portfolio_summary.url}
                                <svg className="w-4 h-4 ml-1 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                </svg>
                            </a>
                        </div>
                    )}

                    {analysis.portfolio_summary.key_findings && analysis.portfolio_summary.key_findings.length > 0 && (
                        <div className="mb-6 bg-white/70 backdrop-blur-sm p-5 rounded-xl border border-purple-200">
                            <h4 className="text-sm font-bold text-purple-900 uppercase tracking-wide mb-4 flex items-center">
                                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                                Key Findings
                            </h4>
                            <ul className="space-y-3">
                                {analysis.portfolio_summary.key_findings.map((finding, idx) => (
                                    <li key={idx} className="flex items-start">
                                        <span className="w-6 h-6 bg-purple-100 text-purple-700 rounded-full flex items-center justify-center mr-3 mt-0.5 flex-shrink-0 text-xs font-bold">
                                            {idx + 1}
                                        </span>
                                        <span className="text-gray-700 leading-relaxed">{finding}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}

                    <div className="grid md:grid-cols-2 gap-6">
                        {analysis.portfolio_summary.strengths_from_portfolio && (
                            <div className="bg-white/70 backdrop-blur-sm p-5 rounded-xl border border-green-200">
                                <h4 className="text-sm font-bold text-green-800 uppercase tracking-wide mb-3 flex items-center">
                                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                                    </svg>
                                    Portfolio Strengths
                                </h4>
                                <p className="text-gray-700 leading-relaxed text-sm">{analysis.portfolio_summary.strengths_from_portfolio}</p>
                            </div>
                        )}

                        {analysis.portfolio_summary.gaps_from_portfolio && (
                            <div className="bg-white/70 backdrop-blur-sm p-5 rounded-xl border border-amber-200">
                                <h4 className="text-sm font-bold text-amber-800 uppercase tracking-wide mb-3 flex items-center">
                                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    Portfolio Improvements
                                </h4>
                                <p className="text-gray-700 leading-relaxed text-sm">{analysis.portfolio_summary.gaps_from_portfolio}</p>
                            </div>
                        )}
                    </div>
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 md:gap-8">
                {/* Strengths */}
                {analysis.cv_feedback && analysis.cv_feedback.strengths?.length > 0 && (
                    <div className="bg-white rounded-2xl shadow-xl p-6 sm:p-8 border-l-4 border-green-500 h-full">
                        <div className="flex items-center mb-4 sm:mb-6">
                            <div className="w-9 h-9 sm:w-10 sm:h-10 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                                <svg className="w-5 h-5 sm:w-6 sm:h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                            <h3 className="text-lg sm:text-xl font-bold text-gray-900">Key Strengths</h3>
                        </div>
                        <ul className="space-y-3 sm:space-y-4">
                            {analysis.cv_feedback.strengths.map((strength, idx) => (
                                <li key={idx} className="flex items-start p-3 bg-green-50/50 rounded-lg">
                                    <span className="w-1.5 h-1.5 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                                    <span className="text-gray-700 leading-relaxed">{strength}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}

                {/* Gaps */}
                {analysis.cv_feedback && analysis.cv_feedback.weaknesses?.length > 0 && (
                    <div className="bg-white rounded-2xl shadow-xl p-6 sm:p-8 border-l-4 border-amber-500 h-full">
                        <div className="flex items-center mb-4 sm:mb-6">
                            <div className="w-9 h-9 sm:w-10 sm:h-10 bg-amber-100 rounded-lg flex items-center justify-center mr-3">
                                <svg className="w-5 h-5 sm:w-6 sm:h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                            </div>
                            <h3 className="text-lg sm:text-xl font-bold text-gray-900">Areas for Improvement</h3>
                        </div>
                        <ul className="space-y-3 sm:space-y-4">
                            {analysis.cv_feedback.weaknesses.map((weakness, idx) => (
                                <li key={idx} className="flex items-start p-3 bg-amber-50/50 rounded-lg">
                                    <span className="w-1.5 h-1.5 bg-amber-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                                    <span className="text-gray-700 leading-relaxed">{weakness}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>

            {/* Roadmap */}
            <div className="bg-white rounded-2xl shadow-xl p-6 sm:p-8 md:p-10 border border-gray-100">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-6 sm:mb-8 gap-3 sm:gap-4">
                    <div>
                        <h3 className="text-xl sm:text-2xl font-bold text-gray-900 mb-2">Personalized Roadmap</h3>
                        <p className="text-sm sm:text-base text-gray-600">Estimated Timeline: <span className="font-semibold text-blue-600">{roadmap.total_weeks} weeks</span></p>
                    </div>
                    <div className="bg-blue-50 px-3 sm:px-4 py-2 rounded-lg border border-blue-100">
                        <span className="text-xs sm:text-sm text-blue-800 font-medium">{roadmap.feasibility_assessment}</span>
                    </div>
                </div>

                <div className="relative space-y-6 sm:space-y-8 before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-300 before:to-transparent">
                    {roadmap.milestones.map((milestone, idx) => (
                        <div key={idx} className="relative flex items-start md:items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                            <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-white bg-slate-300 group-[.is-active]:bg-blue-500 text-slate-500 group-[.is-active]:text-white shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                                <span className="font-bold text-sm">{idx + 1}</span>
                            </div>

                            <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-white p-4 sm:p-5 md:p-6 rounded-xl shadow-md border border-gray-100 hover:shadow-lg transition-shadow">
                                <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-2 gap-2">
                                    <h4 className="font-bold text-base sm:text-lg text-gray-900">{milestone.title}</h4>
                                    <span className="text-xs font-semibold text-gray-500 bg-gray-100 px-2 py-1 rounded self-start sm:self-auto">{milestone.duration_weeks} weeks</span>
                                </div>
                                <p className="text-gray-600 mb-3 sm:mb-4 text-sm">{milestone.description}</p>

                                {milestone.evidence_to_collect.length > 0 && (
                                    <div className="bg-gray-50 p-3 rounded-lg">
                                        <span className="text-xs font-bold text-gray-500 uppercase tracking-wide block mb-2">Evidence to Collect</span>
                                        <ul className="space-y-1">
                                            {milestone.evidence_to_collect.map((evidence, i) => (
                                                <li key={i} className="text-sm text-gray-700 flex items-start">
                                                    <span className="mr-2 text-blue-500">•</span>
                                                    {evidence}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Legal Disclaimer */}
            <div className="bg-amber-50 border-l-4 border-amber-400 p-4 sm:p-6 rounded-lg">
                <div className="flex items-start">
                    <svg className="w-5 h-5 sm:w-6 sm:h-6 text-amber-600 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    <div>
                        <h4 className="text-sm sm:text-base font-bold text-amber-900 mb-1">Legal Disclaimer</h4>
                        <p className="text-xs sm:text-sm text-amber-800 leading-relaxed">
                            This analysis provides guidance and recommendations only. It is <strong>not legal advice</strong> and should not be relied upon as such. For official guidance on your visa application, please consult with a qualified immigration lawyer.
                        </p>
                    </div>
                </div>
            </div>

            {/* <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 pt-2 sm:pt-4">
                <button
                    onClick={onNewStart}
                    className="w-full sm:flex-1 py-3.5 sm:py-4 px-6 bg-white border-2 border-gray-200 text-gray-700 font-bold rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all min-h-[48px]"
                >
                    Start New Analysis
                </button>
                <button
                    onClick={generatePDF}
                    className="w-full sm:flex-1 py-3.5 sm:py-4 px-6 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 shadow-lg shadow-blue-200 hover:shadow-blue-300 transition-all transform hover:-translate-y-0.5 flex items-center justify-center min-h-[48px]"
                >
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    Download Full PDF Report
                </button>
            </div> */}

            {/* Delete Data Dialog */}
            {showDeleteDialog && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-in fade-in duration-200">
                    <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6 sm:p-8 animate-in slide-in-from-bottom duration-300">
                        <div className="flex items-start mb-4">
                            <div className="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center mr-4 flex-shrink-0">
                                <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                            </div>
                            <div className="flex-1">
                                <h3 className="text-xl font-bold text-gray-900 mb-2">Delete All Data?</h3>
                                <p className="text-sm text-gray-700 leading-relaxed">
                                    This will permanently delete:
                                </p>
                                <ul className="mt-3 space-y-1 text-sm text-gray-700">
                                    <li>• All uploaded documents</li>
                                    <li>• Your analysis results</li>
                                    <li>• All session data</li>
                                </ul>
                                <p className="mt-3 text-xs text-red-600 font-semibold">
                                    ⚠️ This action cannot be undone.
                                </p>
                            </div>
                        </div>

                        <div className="flex flex-col sm:flex-row gap-3 mt-6">
                            <button
                                onClick={() => setShowDeleteDialog(false)}
                                disabled={deleting}
                                className="flex-1 py-3 px-6 bg-white border-2 border-gray-200 text-gray-700 font-bold rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all disabled:opacity-50 disabled:cursor-not-allowed min-h-[48px]"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleDeleteData}
                                disabled={deleting}
                                className="flex-1 py-3 px-6 bg-red-600 text-white font-bold rounded-xl hover:bg-red-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-h-[48px]"
                            >
                                {deleting ? (
                                    <>
                                        <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                        Deleting...
                                    </>
                                ) : (
                                    'Delete My Data'
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            )}

            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 pt-2 sm:pt-4">
                <button
                    onClick={onNewStart}
                    className="w-full sm:flex-1 py-3.5 sm:py-4 px-6 bg-white border-2 border-gray-200 text-gray-700 font-bold rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all min-h-[48px]"
                >
                    Start New Analysis
                </button>
                <button
                    onClick={generatePDF}
                    className="w-full sm:flex-1 py-3.5 sm:py-4 px-6 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 shadow-lg shadow-blue-200 hover:shadow-blue-300 transition-all transform hover:-translate-y-0.5 flex items-center justify-center min-h-[48px]"
                >
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    Download Full PDF Report
                </button>
            </div>

            {/* GDPR Data Deletion Button */}
            <div className="mt-6 pt-6 border-t border-gray-200">
                <button
                    onClick={() => setShowDeleteDialog(true)}
                    className="w-full py-3 px-6 bg-white border-2 border-red-200 text-red-600 font-medium rounded-xl hover:bg-red-50 hover:border-red-300 transition-all flex items-center justify-center min-h-[48px] group"
                >
                    <svg className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    <span>Request Data Deletion (GDPR)</span>
                </button>
                <p className="text-xs text-gray-500 text-center mt-2">
                    Permanently delete all your data from our systems
                </p>
            </div>
        </div>
    );
}
