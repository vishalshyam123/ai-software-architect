import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ProjectInput from './components/ProjectInput';
import TabNavigation from './components/TabNavigation';
import RequirementAnalysisView from './components/RequirementAnalysisView';
import SRSView from './components/SRSView';
import UMLView from './components/UMLView';
import DatabaseDesignView from './components/DatabaseDesignView';
import ExportModal from './components/ExportModal';
import { apiService } from './services/api';
import { 
  Layers, 
  Sparkles, 
  Cpu, 
  Clock, 
  CheckCircle, 
  AlertTriangle,
  FolderTree,
  Terminal,
  Code2
} from 'lucide-react';

export default function App() {
  const [health, setHealth] = useState(null);
  const [samples, setSamples] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('requirements');
  const [isExportOpen, setIsExportOpen] = useState(false);

  const [formData, setFormData] = useState({
    title: 'Hospital Management System',
    domain: 'Healthcare',
    target_scale: 'Enterprise Scale',
    description: 'A comprehensive hospital management platform handling patient electronic health records (EHR), outpatient doctor appointment scheduling, clinical e-prescriptions, pharmacy inventory & drug dispensing, and billing with insurance claim management.'
  });

  const [blueprint, setBlueprint] = useState(null);

  useEffect(() => {
    // Initial fetch of health and sample projects
    apiService.getHealth()
      .then(setHealth)
      .catch(err => console.warn('Backend not ready yet:', err.message));

    apiService.getSamples()
      .then(res => {
        setSamples(res);
        if (res && res.length > 0) {
          // Pre-populate with Hospital Management System
          const hospitalSample = res.find(s => s.id === 'hospital-management') || res[0];
          setFormData({
            title: hospitalSample.title,
            domain: hospitalSample.domain,
            target_scale: hospitalSample.target_scale || 'Enterprise Scale',
            description: hospitalSample.description
          });
        }
      })
      .catch(err => console.warn('Could not load samples:', err.message));
  }, []);

  const handleSelectSample = (sample) => {
    setFormData({
      title: sample.title,
      domain: sample.domain,
      target_scale: sample.target_scale || 'Enterprise Scale',
      description: sample.description
    });
  };

  const handleGenerate = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiService.generateAll(formData);
      setBlueprint(data);
      setActiveTab('requirements');
    } catch (err) {
      console.error('Generation error:', err);
      setError(err.message || 'Failed to generate blueprint. Please verify backend service.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Header
        health={health}
        onOpenExport={() => setIsExportOpen(true)}
        onSelectSample={handleSelectSample}
        isExportDisabled={!blueprint}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Hero Section */}
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-400 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI-Powered Autonomous Software Architecture</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">
            Transform Simple Ideas Into <br className="hidden sm:inline" />
            <span className="bg-gradient-to-r from-teal-400 via-cyan-300 to-sky-400 bg-clip-text text-transparent">
              Production-Ready Engineering Blueprints
            </span>
          </h1>
          <p className="text-sm sm:text-base text-slate-400">
            Skip weeks of manual documentation. Automatically synthesize IEEE 830 SRS, 
            interactive Mermaid UML diagrams, and 3NF PostgreSQL database schemas in seconds.
          </p>
        </div>

        {/* Project Input Form */}
        <ProjectInput
          formData={formData}
          setFormData={setFormData}
          samples={samples}
          onSelectSample={handleSelectSample}
          onGenerate={handleGenerate}
          isLoading={isLoading}
        />

        {/* Error Notification */}
        {error && (
          <div className="p-4 rounded-xl bg-red-950/50 border border-red-800 text-red-200 text-sm flex items-center space-x-3">
            <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Blueprint Display Area */}
        {blueprint && (
          <div className="space-y-6">
            <TabNavigation
              activeTab={activeTab}
              setActiveTab={setActiveTab}
              hasData={!!blueprint}
            />

            <div className="min-h-[500px]">
              {activeTab === 'requirements' && (
                <RequirementAnalysisView analysis={blueprint.analysis} />
              )}

              {activeTab === 'srs' && (
                <SRSView srs={blueprint.srs} />
              )}

              {activeTab === 'uml' && (
                <UMLView
                  umlDiagrams={blueprint.uml_diagrams}
                  projectTitle={blueprint.project_title}
                />
              )}

              {activeTab === 'database' && (
                <DatabaseDesignView
                  databaseDesign={blueprint.database_design}
                  projectTitle={blueprint.project_title}
                />
              )}

              {activeTab === 'summary' && (
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="p-5 rounded-xl bg-slate-900 border border-slate-800">
                      <span className="text-xs text-slate-400 font-semibold uppercase">Actors Identified</span>
                      <p className="text-2xl font-bold text-teal-400 mt-1">
                        {blueprint.analysis?.actors?.length || 0}
                      </p>
                    </div>
                    <div className="p-5 rounded-xl bg-slate-900 border border-slate-800">
                      <span className="text-xs text-slate-400 font-semibold uppercase">Functional Reqs</span>
                      <p className="text-2xl font-bold text-cyan-400 mt-1">
                        {blueprint.analysis?.functional_requirements?.length || 0}
                      </p>
                    </div>
                    <div className="p-5 rounded-xl bg-slate-900 border border-slate-800">
                      <span className="text-xs text-slate-400 font-semibold uppercase">UML Diagrams</span>
                      <p className="text-2xl font-bold text-indigo-400 mt-1">5</p>
                      <span className="text-[10px] text-slate-500">Use Case, Class, Seq, Act, Comp</span>
                    </div>
                    <div className="p-5 rounded-xl bg-slate-900 border border-slate-800">
                      <span className="text-xs text-slate-400 font-semibold uppercase">Database Tables</span>
                      <p className="text-2xl font-bold text-emerald-400 mt-1">
                        {blueprint.database_design?.tables?.length || 0}
                      </p>
                    </div>
                  </div>

                  <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
                    <h3 className="text-base font-bold text-white flex items-center space-x-2">
                      <Code2 className="w-5 h-5 text-teal-400" />
                      <span>Recommended Implementation Roadmap</span>
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                      <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
                        <span className="font-bold text-teal-400">Phase 1: Persistence & Schema</span>
                        <p className="text-slate-400">
                          Deploy PostgreSQL database, run generated DDL schema, and seed initial lookup roles and permissions.
                        </p>
                      </div>
                      <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
                        <span className="font-bold text-cyan-400">Phase 2: API & Core Domain</span>
                        <p className="text-slate-400">
                          Implement FastAPI routers corresponding to identified Functional Requirements with JWT RBAC.
                        </p>
                      </div>
                      <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
                        <span className="font-bold text-indigo-400">Phase 3: SPA Frontend & CI/CD</span>
                        <p className="text-slate-400">
                          Construct React UI workflows matching Use Case flows, configure Docker multi-stage build and automated tests.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <span>AI Software Architect • Built with FastAPI, React, Mermaid & PostgreSQL</span>
          <span>Contributors: Vishal Shyam &amp; Pugazhandi Kannan</span>
        </div>
      </footer>

      {/* Export Modal */}
      <ExportModal
        isOpen={isExportOpen}
        onClose={() => setIsExportOpen(false)}
        blueprint={blueprint}
      />
    </div>
  );
}
