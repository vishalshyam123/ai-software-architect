import React, { useState } from 'react';
import { X, Download, FileText, FileCode, Check, Copy, Package } from 'lucide-react';
import { apiService } from '../services/api';

export default function ExportModal({ isOpen, onClose, blueprint }) {
  const [copiedType, setCopiedType] = useState(null);

  if (!isOpen || !blueprint) return null;

  const projectTitle = blueprint.project_title || 'Software_Blueprint';
  const slug = projectTitle.toLowerCase().replace(/\s+/g, '_');

  const downloadMarkdown = () => {
    const content = blueprint.srs?.markdown_content || '';
    apiService.downloadFile(content, `${slug}_srs_specification.md`, 'text/markdown');
  };

  const downloadSQL = () => {
    const content = blueprint.database_design?.sql_schema || '';
    apiService.downloadFile(content, `${slug}_schema.sql`, 'application/sql');
  };

  const downloadJSON = () => {
    const content = JSON.stringify(blueprint, null, 2);
    apiService.downloadFile(content, `${slug}_blueprint.json`, 'application/json');
  };

  const handleCopy = (content, type) => {
    navigator.clipboard.writeText(content);
    setCopiedType(type);
    setTimeout(() => setCopiedType(null), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fadeIn">
      <div className="glass-panel w-full max-w-lg rounded-2xl p-6 border border-slate-800 shadow-2xl space-y-6">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center space-x-2">
            <Package className="w-5 h-5 text-teal-400" />
            <h3 className="font-bold text-white text-base">Export Software Architecture</h3>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <p className="text-xs text-slate-400">
          Download implementation-ready architecture artifacts for development teams, stakeholders, and sprint planning.
        </p>

        <div className="space-y-3">
          {/* Markdown Specification */}
          <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <FileText className="w-5 h-5 text-teal-400" />
              <div>
                <h4 className="text-sm font-semibold text-white">SRS Document (.md)</h4>
                <p className="text-[11px] text-slate-400">Full IEEE 830 specification in Markdown</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => handleCopy(blueprint.srs?.markdown_content || '', 'md')}
                className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
                title="Copy markdown"
              >
                {copiedType === 'md' ? <Check className="w-4 h-4 text-teal-400" /> : <Copy className="w-4 h-4" />}
              </button>
              <button
                onClick={downloadMarkdown}
                className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-teal-500 hover:bg-teal-400 text-slate-950 transition flex items-center space-x-1"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download</span>
              </button>
            </div>
          </div>

          {/* PostgreSQL Schema */}
          <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <FileCode className="w-5 h-5 text-cyan-400" />
              <div>
                <h4 className="text-sm font-semibold text-white">PostgreSQL DDL (.sql)</h4>
                <p className="text-[11px] text-slate-400">Tables, keys, constraints & indexes script</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => handleCopy(blueprint.database_design?.sql_schema || '', 'sql')}
                className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
                title="Copy SQL"
              >
                {copiedType === 'sql' ? <Check className="w-4 h-4 text-teal-400" /> : <Copy className="w-4 h-4" />}
              </button>
              <button
                onClick={downloadSQL}
                className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-cyan-500 hover:bg-cyan-400 text-slate-950 transition flex items-center space-x-1"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download</span>
              </button>
            </div>
          </div>

          {/* Full JSON Blueprint */}
          <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Package className="w-5 h-5 text-emerald-400" />
              <div>
                <h4 className="text-sm font-semibold text-white">Complete Blueprint (.json)</h4>
                <p className="text-[11px] text-slate-400">Requirements, 5 diagrams, and schemas</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => handleCopy(JSON.stringify(blueprint, null, 2), 'json')}
                className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
                title="Copy JSON"
              >
                {copiedType === 'json' ? <Check className="w-4 h-4 text-teal-400" /> : <Copy className="w-4 h-4" />}
              </button>
              <button
                onClick={downloadJSON}
                className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition flex items-center space-x-1"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download</span>
              </button>
            </div>
          </div>
        </div>

        <div className="pt-2">
          <button
            onClick={onClose}
            className="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
