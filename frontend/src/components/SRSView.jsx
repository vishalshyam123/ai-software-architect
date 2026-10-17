import React, { useState } from 'react';
import { BookOpen, Download, Copy, Check, FileText, CheckCircle, ShieldAlert } from 'lucide-react';
import { apiService } from '../services/api';

export default function SRSView({ srs }) {
  const [copied, setCopied] = useState(false);

  if (!srs) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(srs.markdown_content || '');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const slug = (srs.project_title || 'srs').toLowerCase().replace(/\s+/g, '_');
    apiService.downloadFile(srs.markdown_content || '', `${slug}_SRS_specification.md`, 'text/markdown');
  };

  return (
    <div className="space-y-6">
      {/* Top Banner & Actions */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-5 rounded-xl bg-slate-900 border border-slate-800">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold uppercase tracking-wider text-teal-400">
              IEEE Std 830-1998 Compliant Specification
            </span>
            <span className="text-slate-500">•</span>
            <span className="text-xs text-slate-400">Version {srs.version}</span>
          </div>
          <h2 className="text-lg font-bold text-white mt-1">{srs.project_title} - SRS</h2>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={handleCopy}
            className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-200 bg-slate-800 hover:bg-slate-700 transition"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-teal-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy Markdown'}</span>
          </button>
          <button
            onClick={handleDownload}
            className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold text-teal-300 bg-teal-950/70 border border-teal-800/80 hover:bg-teal-900/60 transition"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download .md</span>
          </button>
        </div>
      </div>

      {/* Objectives, Constraints, Assumptions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Objectives */}
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
          <h4 className="text-xs font-bold text-teal-400 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
            <CheckCircle className="w-3.5 h-3.5" />
            <span>System Objectives</span>
          </h4>
          <ul className="space-y-1.5">
            {srs.objectives?.map((obj, i) => (
              <li key={i} className="text-xs text-slate-300 flex items-start space-x-1.5">
                <span className="text-teal-400">•</span>
                <span>{obj}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Constraints */}
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
          <h4 className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
            <ShieldAlert className="w-3.5 h-3.5" />
            <span>Design Constraints</span>
          </h4>
          <ul className="space-y-1.5">
            {srs.constraints?.map((con, i) => (
              <li key={i} className="text-xs text-slate-300 flex items-start space-x-1.5">
                <span className="text-amber-400">•</span>
                <span>{con}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Assumptions */}
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
          <h4 className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
            <FileText className="w-3.5 h-3.5" />
            <span>Assumptions</span>
          </h4>
          <ul className="space-y-1.5">
            {srs.assumptions?.map((assm, i) => (
              <li key={i} className="text-xs text-slate-300 flex items-start space-x-1.5">
                <span className="text-cyan-400">•</span>
                <span>{assm}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Detailed Use Cases */}
      {srs.use_cases?.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
            Detailed Use Case Specifications
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {srs.use_cases.map((uc, i) => (
              <div key={i} className="p-5 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono font-bold text-teal-400">{uc.id}</span>
                  <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                    Actor: {uc.actor}
                  </span>
                </div>
                <h4 className="text-sm font-bold text-white">{uc.title}</h4>
                <p className="text-xs text-slate-400"><strong className="text-slate-300">Trigger:</strong> {uc.trigger}</p>
                <p className="text-xs text-slate-400"><strong className="text-slate-300">Preconditions:</strong> {uc.preconditions}</p>

                <div className="pt-2">
                  <span className="text-[10px] font-bold text-slate-400 uppercase">Main Flow:</span>
                  <ol className="mt-1 space-y-1">
                    {uc.main_flow?.map((step, sIdx) => (
                      <li key={sIdx} className="text-xs text-slate-300 flex items-start space-x-1.5">
                        <span className="text-teal-500 font-mono text-[10px]">{sIdx + 1}.</span>
                        <span>{step}</span>
                      </li>
                    ))}
                  </ol>
                </div>

                <div className="pt-2 text-xs text-slate-400">
                  <strong className="text-slate-300">Postconditions:</strong> {uc.postconditions}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Raw Markdown Document Viewer */}
      <div className="rounded-xl border border-slate-800 bg-slate-950 overflow-hidden shadow-xl">
        <div className="px-4 py-3 bg-slate-900 border-b border-slate-800 flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
            Rendered SRS Document Preview
          </span>
          <span className="text-xs text-slate-500 font-mono">markdown</span>
        </div>
        <div className="p-6 overflow-x-auto max-h-[500px] overflow-y-auto font-mono text-xs text-slate-300 leading-relaxed whitespace-pre-wrap selection:bg-teal-500">
          {srs.markdown_content}
        </div>
      </div>
    </div>
  );
}
