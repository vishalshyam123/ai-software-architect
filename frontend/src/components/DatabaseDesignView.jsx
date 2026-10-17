import React, { useState } from 'react';
import { Database, FileCode, Table, GitFork, Copy, Check, Download } from 'lucide-react';
import MermaidViewer from './MermaidViewer';
import { apiService } from '../services/api';

export default function DatabaseDesignView({ databaseDesign, projectTitle }) {
  const [subTab, setSubTab] = useState('erd');
  const [copied, setCopied] = useState(false);

  if (!databaseDesign) return null;

  const handleCopySql = () => {
    navigator.clipboard.writeText(databaseDesign.sql_schema || '');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadSql = () => {
    const slug = (projectTitle || 'database').toLowerCase().replace(/\s+/g, '_');
    apiService.downloadFile(databaseDesign.sql_schema || '', `${slug}_schema.sql`, 'application/sql');
  };

  return (
    <div className="space-y-6">
      {/* Sub Tabs */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-2 rounded-xl bg-slate-900 border border-slate-800">
        <div className="flex space-x-1">
          <button
            onClick={() => setSubTab('erd')}
            className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
              subTab === 'erd'
                ? 'bg-teal-500 text-slate-950 font-bold'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            <GitFork className="w-3.5 h-3.5" />
            <span>Mermaid ER Diagram</span>
          </button>

          <button
            onClick={() => setSubTab('sql')}
            className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
              subTab === 'sql'
                ? 'bg-teal-500 text-slate-950 font-bold'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            <FileCode className="w-3.5 h-3.5" />
            <span>PostgreSQL DDL</span>
          </button>

          <button
            onClick={() => setSubTab('tables')}
            className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
              subTab === 'tables'
                ? 'bg-teal-500 text-slate-950 font-bold'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            <Table className="w-3.5 h-3.5" />
            <span>Data Dictionary</span>
          </button>
        </div>

        {subTab === 'sql' && (
          <div className="flex items-center space-x-2">
            <button
              onClick={handleCopySql}
              className="inline-flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-200 bg-slate-800 hover:bg-slate-700 transition"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-teal-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Copy SQL'}</span>
            </button>
            <button
              onClick={handleDownloadSql}
              className="inline-flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-semibold text-teal-300 bg-teal-950/70 border border-teal-800/80 hover:bg-teal-900/60 transition"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Download .sql</span>
            </button>
          </div>
        )}
      </div>

      {/* Subtab Contents */}
      {subTab === 'erd' && (
        <div className="h-[650px]">
          <MermaidViewer
            chartCode={databaseDesign.er_diagram}
            title={`${projectTitle || 'System'} - Entity Relationship Diagram`}
          />
        </div>
      )}

      {subTab === 'sql' && (
        <div className="rounded-xl border border-slate-800 bg-slate-950 overflow-hidden shadow-xl">
          <div className="px-4 py-3 bg-slate-900 border-b border-slate-800 flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
              PostgreSQL 15+ Compatible DDL Schema
            </span>
            <span className="text-xs text-slate-500 font-mono">sql</span>
          </div>
          <pre className="p-6 overflow-x-auto max-h-[600px] overflow-y-auto font-mono text-xs text-teal-300/90 leading-relaxed bg-slate-950 selection:bg-teal-500 selection:text-white">
            {databaseDesign.sql_schema}
          </pre>
        </div>
      )}

      {subTab === 'tables' && (
        <div className="space-y-6">
          {/* Relationships summary */}
          {databaseDesign.relationships?.length > 0 && (
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
              <h4 className="text-xs font-bold text-teal-400 uppercase tracking-wider mb-3">
                Entity Relationships & Foreign Keys
              </h4>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead>
                    <tr className="border-b border-slate-800 text-slate-400">
                      <th className="pb-2 font-semibold">From Table</th>
                      <th className="pb-2 font-semibold">Relationship</th>
                      <th className="pb-2 font-semibold">To Table</th>
                      <th className="pb-2 font-semibold">Description</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60">
                    {databaseDesign.relationships.map((rel, idx) => (
                      <tr key={idx} className="text-slate-300">
                        <td className="py-2.5 font-mono text-teal-400 font-semibold">{rel.from_table}</td>
                        <td className="py-2.5 text-slate-400">{rel.relationship_type}</td>
                        <td className="py-2.5 font-mono text-cyan-400 font-semibold">{rel.to_table}</td>
                        <td className="py-2.5 text-slate-400">{rel.description}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Tables dictionary */}
          <div className="space-y-4">
            <h4 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
              Database Table Schemas ({databaseDesign.tables?.length || 0})
            </h4>

            {databaseDesign.tables?.map((tbl, tIdx) => (
              <div key={tIdx} className="p-5 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Database className="w-4 h-4 text-teal-400" />
                    <span className="font-mono font-bold text-sm text-white">{tbl.name}</span>
                  </div>
                  <span className="text-xs text-slate-400">{tbl.description}</span>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead>
                      <tr className="border-b border-slate-800 text-slate-400">
                        <th className="pb-2 font-semibold">Column</th>
                        <th className="pb-2 font-semibold">Type</th>
                        <th className="pb-2 font-semibold">Attributes</th>
                        <th className="pb-2 font-semibold">Description</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/50">
                      {tbl.columns?.map((col, cIdx) => (
                        <tr key={cIdx} className="text-slate-300">
                          <td className="py-2 font-mono font-medium text-slate-200">
                            {col.name}
                          </td>
                          <td className="py-2 font-mono text-teal-300">
                            {col.data_type}
                          </td>
                          <td className="py-2 space-x-1">
                            {col.is_primary_key && (
                              <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20">
                                PK
                              </span>
                            )}
                            {col.is_foreign_key && (
                              <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20" title={`References ${col.references}`}>
                                FK ({col.references})
                              </span>
                            )}
                            {!col.is_nullable && (
                              <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-400">
                                NOT NULL
                              </span>
                            )}
                          </td>
                          <td className="py-2 text-slate-400">
                            {col.description}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
