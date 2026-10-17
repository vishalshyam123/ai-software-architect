import React, { useState } from 'react';
import { GitFork, Network, Workflow, Layers, Box } from 'lucide-react';
import MermaidViewer from './MermaidViewer';

export default function UMLView({ umlDiagrams, projectTitle }) {
  const [activeDiagram, setActiveDiagram] = useState('use_case');

  if (!umlDiagrams) return null;

  const diagramTypes = [
    {
      id: 'use_case',
      label: 'Use Case Diagram',
      icon: GitFork,
      code: umlDiagrams.use_case_diagram,
      description: 'Illustrates system functional boundaries, actors, and their interactions with core capabilities.'
    },
    {
      id: 'class_diagram',
      label: 'Class Diagram',
      icon: Box,
      code: umlDiagrams.class_diagram,
      description: 'Defines object-oriented domain models, entity attributes, methods, and class inheritance/associations.'
    },
    {
      id: 'sequence_diagram',
      label: 'Sequence Diagram',
      icon: Workflow,
      code: umlDiagrams.sequence_diagram,
      description: 'Chronological timeline of messages passed between users, API gateways, database, and background workers.'
    },
    {
      id: 'activity_diagram',
      label: 'Activity / Flow Diagram',
      icon: Network,
      code: umlDiagrams.activity_diagram,
      description: 'Operational control flow depicting decision diamonds, concurrency, and validation checkpoints.'
    },
    {
      id: 'component_diagram',
      label: 'Component Architecture',
      icon: Layers,
      code: umlDiagrams.component_diagram,
      description: 'High-level deployment topology organizing presentation, API backend, database, and external integrations.'
    }
  ];

  const current = diagramTypes.find(d => d.id === activeDiagram) || diagramTypes[0];

  return (
    <div className="space-y-6">
      {/* Diagram Sub-tabs */}
      <div className="flex flex-wrap gap-2 p-1.5 rounded-xl bg-slate-900 border border-slate-800">
        {diagramTypes.map((diag) => {
          const Icon = diag.icon;
          const isSelected = activeDiagram === diag.id;
          return (
            <button
              key={diag.id}
              onClick={() => setActiveDiagram(diag.id)}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-xs font-semibold transition ${
                isSelected
                  ? 'bg-teal-500 text-slate-950 shadow-md font-bold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{diag.label}</span>
            </button>
          );
        })}
      </div>

      {/* Description Header */}
      <div className="px-4 py-2.5 rounded-lg bg-slate-900/50 border border-slate-800 text-xs text-slate-400">
        <strong className="text-slate-200">{current.label}: </strong>
        {current.description}
      </div>

      {/* Mermaid Canvas */}
      <div className="h-[650px]">
        <MermaidViewer
          chartCode={current.code}
          title={`${projectTitle || 'System'} - ${current.label}`}
        />
      </div>
    </div>
  );
}
