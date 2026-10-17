import React from 'react';
import { Layers, Activity, Download, Github, Sparkles, Database } from 'lucide-react';

export default function Header({ health, onOpenExport, onSelectSample, isExportDisabled }) {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-teal-500/20">
            <Layers className="w-5 h-5 text-slate-950 font-bold" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-teal-300 bg-clip-text text-transparent">
                AI Software Architect
              </span>
              <span className="text-[10px] font-semibold uppercase tracking-widest px-2 py-0.5 rounded-full bg-teal-500/10 text-teal-400 border border-teal-500/20">
                v1.0
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              Intelligent Software Requirements, UML & Database Blueprint Generator
            </p>
          </div>
        </div>

        {/* Status and Action Buttons */}
        <div className="flex items-center space-x-3">
          {/* Health indicator */}
          <div className="hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs">
            <span className="relative flex h-2 w-2">
              <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${health?.status === 'healthy' ? 'bg-teal-400' : 'bg-amber-400'}`} />
              <span className={`relative inline-flex rounded-full h-2 w-2 ${health?.status === 'healthy' ? 'bg-teal-500' : 'bg-amber-500'}`} />
            </span>
            <span className="text-slate-400">Engine:</span>
            <span className="text-slate-200 font-medium">
              {health ? (health.ai_engine.includes('OpenAI') ? 'OpenAI GPT' : 'Heuristic Engine') : 'Connecting...'}
            </span>
          </div>

          {/* Export Blueprint button */}
          <button
            onClick={onOpenExport}
            disabled={isExportDisabled}
            className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-gradient-to-r from-teal-500 to-cyan-600 hover:from-teal-400 hover:to-cyan-500 shadow-md shadow-teal-500/20 transition disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Blueprint</span>
          </button>
        </div>
      </div>
    </header>
  );
}
