import React from 'react';
import { FileCheck, BookOpen, GitMerge, Database, BarChart3 } from 'lucide-react';

export default function TabNavigation({ activeTab, setActiveTab, hasData }) {
  const tabs = [
    { id: 'requirements', label: 'Requirement Analysis', icon: FileCheck },
    { id: 'srs', label: 'SRS Specification', icon: BookOpen },
    { id: 'uml', label: 'UML Diagrams', icon: GitMerge },
    { id: 'database', label: 'Database Design', icon: Database },
    { id: 'summary', label: 'Architecture Overview', icon: BarChart3 },
  ];

  return (
    <div className="flex border-b border-slate-800 space-x-1 sm:space-x-2 overflow-x-auto pb-px">
      {tabs.map((tab) => {
        const Icon = tab.icon;
        const isActive = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            disabled={!hasData}
            className={`flex items-center space-x-2 px-4 py-3 text-xs sm:text-sm font-semibold rounded-t-xl transition border-b-2 whitespace-nowrap ${
              isActive
                ? 'border-teal-400 text-teal-300 bg-slate-900/60'
                : hasData
                ? 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-900/30'
                : 'border-transparent text-slate-600 cursor-not-allowed opacity-50'
            }`}
          >
            <Icon className={`w-4 h-4 ${isActive ? 'text-teal-400' : ''}`} />
            <span>{tab.label}</span>
          </button>
        );
      })}
    </div>
  );
}
