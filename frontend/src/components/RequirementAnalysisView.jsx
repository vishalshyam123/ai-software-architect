import React from 'react';
import { Users, Shield, Target, CheckCircle2, XCircle, ArrowUpRight, Zap } from 'lucide-react';

export default function RequirementAnalysisView({ analysis }) {
  if (!analysis) return null;

  const getPriorityBadge = (priority) => {
    const p = priority?.toLowerCase() || '';
    if (p.includes('must')) {
      return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
    } else if (p.includes('should')) {
      return 'bg-blue-500/10 text-blue-400 border-blue-500/20';
    }
    return 'bg-slate-500/10 text-slate-400 border-slate-500/20';
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Executive Summary */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-teal-950/40 border border-slate-800">
        <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
          <span className="text-xs font-bold uppercase tracking-wider text-teal-400">
            Architectural Executive Summary
          </span>
          <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-teal-500/10 text-teal-300 border border-teal-500/20">
            {analysis.domain}
          </span>
        </div>
        <h2 className="text-xl font-bold text-white mb-2">{analysis.project_title}</h2>
        <p className="text-slate-300 text-sm leading-relaxed">{analysis.summary}</p>
      </div>

      {/* Scope: In Scope vs Out of Scope */}
      {analysis.scope && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-5 rounded-xl bg-slate-900/80 border border-slate-800 shadow-md">
            <div className="flex items-center space-x-2 text-emerald-400 text-sm font-bold mb-3">
              <CheckCircle2 className="w-4 h-4" />
              <span>In Scope (Planned Architecture)</span>
            </div>
            <ul className="space-y-2">
              {analysis.scope.in_scope?.map((item, idx) => (
                <li key={idx} className="text-xs text-slate-300 flex items-start space-x-2">
                  <span className="text-emerald-500 font-bold">•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="p-5 rounded-xl bg-slate-900/80 border border-slate-800 shadow-md">
            <div className="flex items-center space-x-2 text-amber-400 text-sm font-bold mb-3">
              <XCircle className="w-4 h-4" />
              <span>Out of Scope (Explicit Boundaries)</span>
            </div>
            <ul className="space-y-2">
              {analysis.scope.out_of_scope?.map((item, idx) => (
                <li key={idx} className="text-xs text-slate-400 flex items-start space-x-2">
                  <span className="text-amber-500 font-bold">•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Actors & Stakeholders Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Actors */}
        <div>
          <div className="flex items-center space-x-2 mb-3">
            <Users className="w-4 h-4 text-teal-400" />
            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
              Identified System Actors
            </h3>
          </div>
          <div className="space-y-3">
            {analysis.actors?.map((actor, idx) => (
              <div key={idx} className="p-4 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-sm font-bold text-white">{actor.name}</span>
                  <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                    {actor.type}
                  </span>
                </div>
                <p className="text-xs text-slate-400">{actor.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Stakeholders */}
        <div>
          <div className="flex items-center space-x-2 mb-3">
            <Target className="w-4 h-4 text-cyan-400" />
            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
              Project Stakeholders
            </h3>
          </div>
          <div className="space-y-3">
            {analysis.stakeholders?.map((stk, idx) => (
              <div key={idx} className="p-4 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-sm font-bold text-white">{stk.name}</span>
                  <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full bg-cyan-950/60 text-cyan-400 border border-cyan-800/60">
                    Impact: {stk.impact}
                  </span>
                </div>
                <p className="text-xs text-slate-400">{stk.interest}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Functional Requirements */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <Zap className="w-4 h-4 text-teal-400" />
            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
              Functional Requirements ({analysis.functional_requirements?.length || 0})
            </h3>
          </div>
        </div>

        <div className="space-y-3">
          {analysis.functional_requirements?.map((fr, idx) => (
            <div key={idx} className="p-5 rounded-xl bg-slate-900 border border-slate-800 hover:border-teal-500/30 transition">
              <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-mono font-bold text-teal-400 bg-teal-950/60 px-2 py-0.5 rounded border border-teal-800/60">
                    {fr.id}
                  </span>
                  <span className="text-sm font-bold text-white">{fr.title}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-[10px] font-semibold text-slate-400 bg-slate-800 px-2 py-0.5 rounded">
                    {fr.category}
                  </span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${getPriorityBadge(fr.priority)}`}>
                    {fr.priority}
                  </span>
                </div>
              </div>
              <p className="text-xs text-slate-300 mb-3">{fr.description}</p>

              {fr.acceptance_criteria?.length > 0 && (
                <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800/80">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1.5">
                    Acceptance Criteria:
                  </span>
                  <ul className="space-y-1">
                    {fr.acceptance_criteria.map((ac, cIdx) => (
                      <li key={cIdx} className="text-xs text-slate-400 flex items-start space-x-2">
                        <CheckCircle2 className="w-3.5 h-3.5 text-teal-500 mt-0.5 flex-shrink-0" />
                        <span>{ac}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Non-Functional Requirements */}
      <div>
        <div className="flex items-center space-x-2 mb-3">
          <Shield className="w-4 h-4 text-teal-400" />
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
            Non-Functional Quality Attributes
          </h3>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {analysis.non_functional_requirements?.map((nfr, idx) => (
            <div key={idx} className="p-4 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-xs font-semibold text-teal-400 uppercase tracking-wider">
                {nfr.category}
              </span>
              <p className="text-sm font-bold text-white mt-1">{nfr.metric}</p>
              <div className="mt-2 pt-2 border-t border-slate-800 text-xs text-slate-400">
                <span className="font-semibold text-slate-300">Target: </span>
                {nfr.target}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
