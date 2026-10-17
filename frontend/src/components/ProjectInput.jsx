import React from 'react';
import { Sparkles, Play, BookOpen, Database, GitMerge, FileText, CheckCircle2 } from 'lucide-react';

export default function ProjectInput({
  formData,
  setFormData,
  samples,
  onSelectSample,
  onGenerate,
  isLoading
}) {
  const domains = [
    'Healthcare',
    'E-Commerce & Retail',
    'FinTech & Banking',
    'Transportation & Logistics',
    'EdTech',
    'Real Estate & PropTech',
    'Enterprise SaaS'
  ];

  const scales = ['MVP / Prototype', 'Startup / Medium', 'Enterprise Scale'];

  return (
    <div className="glass-panel rounded-2xl p-6 shadow-2xl border border-slate-800">
      {/* Sample Quick Selector */}
      <div className="mb-6 flex flex-wrap items-center gap-2">
        <span className="text-xs font-semibold text-slate-400 flex items-center gap-1.5 mr-1">
          <Sparkles className="w-3.5 h-3.5 text-teal-400" />
          Quick Load Sample:
        </span>
        {samples.map((sample) => (
          <button
            key={sample.id}
            type="button"
            onClick={() => onSelectSample(sample)}
            className="text-xs px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700/80 hover:border-teal-500/60 hover:bg-slate-800 text-slate-300 hover:text-white transition flex items-center space-x-1.5"
          >
            <span>{sample.title}</span>
          </button>
        ))}
      </div>

      <form onSubmit={(e) => { e.preventDefault(); onGenerate(); }} className="space-y-4">
        {/* Row: Title, Domain, Scale */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="md:col-span-1">
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Project Title *
            </label>
            <input
              type="text"
              required
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="e.g., Hospital Management System"
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500 text-sm transition"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Industry Domain
            </label>
            <select
              value={formData.domain}
              onChange={(e) => setFormData({ ...formData, domain: e.target.value })}
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-100 focus:outline-none focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500 text-sm transition"
            >
              {domains.map((d) => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Target Scale
            </label>
            <select
              value={formData.target_scale}
              onChange={(e) => setFormData({ ...formData, target_scale: e.target.value })}
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-100 focus:outline-none focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500 text-sm transition"
            >
              {scales.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Project Description */}
        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
            Project Description & Requirements *
          </label>
          <textarea
            required
            rows={3}
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            placeholder="Describe the system goals, key entities, primary user actions, and any business constraints..."
            className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500 text-sm transition resize-y"
          />
        </div>

        {/* Action Row */}
        <div className="pt-2 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400">
            <span className="flex items-center gap-1 text-slate-300">
              <CheckCircle2 className="w-3.5 h-3.5 text-teal-400" />
              Requirements Analysis
            </span>
            <span className="flex items-center gap-1 text-slate-300">
              <CheckCircle2 className="w-3.5 h-3.5 text-teal-400" />
              IEEE 830 SRS
            </span>
            <span className="flex items-center gap-1 text-slate-300">
              <CheckCircle2 className="w-3.5 h-3.5 text-teal-400" />
              5 UML Diagrams
            </span>
            <span className="flex items-center gap-1 text-slate-300">
              <CheckCircle2 className="w-3.5 h-3.5 text-teal-400" />
              PostgreSQL Schema & ERD
            </span>
          </div>

          <button
            type="submit"
            disabled={isLoading || !formData.title || !formData.description}
            className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-6 py-3 rounded-xl font-bold text-sm text-slate-950 bg-gradient-to-r from-teal-400 to-cyan-400 hover:from-teal-300 hover:to-cyan-300 shadow-lg shadow-teal-500/25 transition disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {isLoading ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-slate-950" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                <span>Architecting System...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-slate-950" />
                <span>Generate Architecture Blueprint</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
