import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { generateReport } from './api';

function App() {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [reportData, setReportData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);
    setReportData(null);

    try {
      const data = await generateReport(query);
      setReportData(data);
    } catch (err) {
      setError('Failed to generate report. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-blue-200">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-xl shadow-inner">
              E
            </div>
            <h1 className="text-xl font-semibold tracking-tight text-slate-800">
              Equity Market Reports
            </h1>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Input Section */}
          <div className="lg:col-span-4 space-y-6">
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 transition-all hover:shadow-md">
              <h2 className="text-lg font-semibold text-slate-800 mb-2">Generate Report</h2>
              <p className="text-sm text-slate-500 mb-6">
                Enter a timeframe to generate an automated quarterly market report.
              </p>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="query" className="block text-sm font-medium text-slate-700 mb-1">
                    Temporal Query
                  </label>
                  <textarea
                    id="query"
                    rows={3}
                    className="w-full rounded-xl border-slate-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm p-3 bg-slate-50 transition-colors"
                    placeholder="e.g. Generate the Equity market report for Q4 2025"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    disabled={isLoading}
                  />
                </div>
                
                <button
                  type="submit"
                  disabled={isLoading || !query.trim()}
                  className="w-full flex justify-center items-center py-2.5 px-4 border border-transparent rounded-xl shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-[0.98]"
                >
                  {isLoading ? (
                    <span className="flex items-center gap-2">
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Generating...
                    </span>
                  ) : (
                    'Generate Report'
                  )}
                </button>
              </form>
            </div>

            {/* Diagnostic Data Panel */}
            {reportData?.parsed_query && (
              <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 animate-in fade-in slide-in-from-bottom-4 duration-500">
                <h3 className="text-sm font-semibold tracking-wider text-slate-500 uppercase mb-4">Diagnostics</h3>
                <dl className="space-y-3 text-sm">
                  <div className="flex justify-between">
                    <dt className="text-slate-500">Target Quarter:</dt>
                    <dd className="font-medium text-slate-900">{reportData.parsed_query.quarter}</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="text-slate-500">Target Year:</dt>
                    <dd className="font-medium text-slate-900">{reportData.parsed_query.year}</dd>
                  </div>
                  {reportData.parsed_query.style_instructions && reportData.parsed_query.style_instructions !== "None" && (
                    <div className="flex justify-between">
                      <dt className="text-slate-500">Style Rule:</dt>
                      <dd className="font-medium text-slate-900 truncate max-w-[150px]" title={reportData.parsed_query.style_instructions}>
                        {reportData.parsed_query.style_instructions}
                      </dd>
                    </div>
                  )}
                  <div className="flex justify-between pt-3 border-t border-slate-100">
                    <dt className="text-slate-500">Data Source (MVP):</dt>
                    <dd className="font-medium text-green-600 flex items-center gap-1">
                      <span className="w-2 h-2 rounded-full bg-green-500"></span>
                      Mocked API Connected
                    </dd>
                  </div>
                </dl>
              </div>
            )}
          </div>

          {/* Output Section */}
          <div className="lg:col-span-8">
            <div className="bg-white rounded-2xl p-8 shadow-sm border border-slate-200 min-h-[500px] flex flex-col relative overflow-hidden transition-all">
              
              {/* Glassmorphic overlay when loading */}
              {isLoading && (
                <div className="absolute inset-0 bg-white/60 backdrop-blur-sm z-10 flex flex-col items-center justify-center animate-in fade-in">
                  <div className="relative w-16 h-16">
                    <div className="absolute inset-0 rounded-full border-t-2 border-blue-600 animate-spin"></div>
                    <div className="absolute inset-2 rounded-full border-r-2 border-slate-300 animate-spin flex-reverse"></div>
                  </div>
                  <p className="mt-4 text-slate-600 font-medium animate-pulse">Synthesizing narrative...</p>
                </div>
              )}

              {error && (
                <div className="bg-red-50 text-red-700 p-4 rounded-xl border border-red-100 flex gap-3 text-sm flex-1 items-start">
                  <svg className="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  {error}
                </div>
              )}

              {!reportData && !isLoading && !error && (
                <div className="flex-1 flex flex-col items-center justify-center text-center opacity-60">
                  <div className="w-16 h-16 mb-4 rounded-xl bg-slate-100 flex items-center justify-center">
                    <svg className="w-8 h-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-medium text-slate-900">No Report Generated</h3>
                  <p className="max-w-xs mt-1 text-sm text-slate-500">
                    Submit a temporal query to generate an equity market report.
                  </p>
                </div>
              )}

              {reportData && (
                <div className="prose prose-slate prose-blue max-w-none prose-headings:font-semibold prose-a:text-blue-600 animate-in fade-in slide-in-from-bottom-8 duration-700 flex-1">
                  <div className="flex items-center justify-between mb-8 border-b border-slate-100 pb-4">
                    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700">
                      <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"></span>
                      AI Drafted
                    </span>
                    <button className="text-sm font-medium text-slate-500 hover:text-slate-800 transition-colors flex items-center gap-2">
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                         <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                      </svg>
                      Copy Report
                    </button>
                  </div>
                  <ReactMarkdown>{reportData.report}</ReactMarkdown>
                  
                  {/* Human in the loop review actions */}
                  <div className="mt-12 pt-6 border-t border-slate-200 flex items-center justify-end gap-3">
                     <button className="px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                       Flag Deviation
                     </button>
                     <button className="px-4 py-2 text-sm font-medium text-white bg-slate-800 hover:bg-slate-900 rounded-lg shadow-sm transition-colors">
                       Approve & Publish
                     </button>
                  </div>
                </div>
              )}

            </div>
          </div>
          
        </div>
      </main>
    </div>
  );
}

export default App;
