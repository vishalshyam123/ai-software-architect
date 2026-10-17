import React, { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';
import { ZoomIn, ZoomOut, RotateCcw, Copy, Check, Download, AlertCircle } from 'lucide-react';

mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  securityLevel: 'loose',
  themeVariables: {
    darkMode: true,
    background: '#0f172a',
    primaryColor: '#0d9488',
    primaryTextColor: '#f8fafc',
    primaryBorderColor: '#14b8a6',
    lineColor: '#38bdf8',
    secondaryColor: '#1e293b',
    tertiaryColor: '#1e1b4b',
    edgeLabelBackground: '#090d16',
    clusterBkg: '#131b2e',
    clusterBorder: '#334155',
  },
  fontFamily: 'Inter, sans-serif'
});

export default function MermaidViewer({ chartCode, title = "Diagram" }) {
  const containerRef = useRef(null);
  const [svgContent, setSvgContent] = useState('');
  const [error, setError] = useState(null);
  const [scale, setScale] = useState(1);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    let isMounted = true;
    setError(null);

    const renderChart = async () => {
      if (!chartCode || !chartCode.trim()) return;
      try {
        const id = `mermaid-${Math.random().toString(36).substring(2, 9)}`;
        const { svg } = await mermaid.render(id, chartCode.trim());
        if (isMounted) {
          setSvgContent(svg);
          setError(null);
        }
      } catch (err) {
        console.error("Mermaid Render Error:", err);
        if (isMounted) {
          setError(err.message || "Failed to render Mermaid diagram. Check syntax.");
        }
      }
    };

    renderChart();
    return () => {
      isMounted = false;
    };
  }, [chartCode]);

  const handleCopy = () => {
    navigator.clipboard.writeText(chartCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    if (!svgContent) return;
    const blob = new Blob([svgContent], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${title.toLowerCase().replace(/\s+/g, '_')}.svg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const zoomIn = () => setScale(prev => Math.min(prev + 0.15, 2.5));
  const zoomOut = () => setScale(prev => Math.max(prev - 0.15, 0.5));
  const resetZoom = () => setScale(1);

  return (
    <div className="flex flex-col h-full bg-slate-900/90 rounded-xl border border-slate-800 overflow-hidden shadow-xl">
      {/* Top Toolbar */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-slate-900 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-teal-400">
            Mermaid Diagram
          </span>
          <span className="text-slate-500">|</span>
          <span className="text-sm font-medium text-slate-300">{title}</span>
        </div>

        <div className="flex items-center space-x-1.5">
          <button
            onClick={zoomIn}
            title="Zoom In"
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <button
            onClick={zoomOut}
            title="Zoom Out"
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <button
            onClick={resetZoom}
            title="Reset Zoom"
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition text-xs font-mono"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
          <div className="h-4 w-px bg-slate-800 mx-1" />
          <button
            onClick={handleCopy}
            title="Copy Mermaid Code"
            className="inline-flex items-center space-x-1 px-2.5 py-1.5 rounded-lg text-xs font-medium text-slate-300 bg-slate-800 hover:bg-slate-700 transition"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-teal-400" />
                <span className="text-teal-400">Copied</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                <span>Copy Code</span>
              </>
            )}
          </button>
          <button
            onClick={handleDownload}
            disabled={!svgContent}
            title="Download SVG"
            className="inline-flex items-center space-x-1 px-2.5 py-1.5 rounded-lg text-xs font-medium text-teal-300 bg-teal-950/60 border border-teal-800/60 hover:bg-teal-900/60 transition disabled:opacity-40"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export SVG</span>
          </button>
        </div>
      </div>

      {/* Diagram Canvas */}
      <div 
        ref={containerRef}
        className="flex-1 relative overflow-auto p-8 flex items-center justify-center min-h-[420px] bg-slate-950/60"
      >
        {error ? (
          <div className="max-w-md p-4 rounded-lg bg-red-950/40 border border-red-800/60 text-red-300 text-sm flex flex-col space-y-2">
            <div className="flex items-center space-x-2 font-semibold text-red-200">
              <AlertCircle className="w-5 h-5 text-red-400" />
              <span>Diagram Rendering Notice</span>
            </div>
            <p className="text-xs text-red-300/80">{error}</p>
            <pre className="mt-2 p-2 bg-slate-950 rounded text-xs font-mono text-slate-400 overflow-x-auto max-h-40">
              {chartCode}
            </pre>
          </div>
        ) : svgContent ? (
          <div
            style={{ transform: `scale(${scale})`, transformOrigin: 'center center', transition: 'transform 0.15s ease' }}
            className="transition-transform duration-100 ease-out select-none"
            dangerouslySetInnerHTML={{ __html: svgContent }}
          />
        ) : (
          <div className="text-slate-500 text-sm animate-pulse flex items-center space-x-2">
            <span>Rendering Architecture Diagram...</span>
          </div>
        )}
      </div>
    </div>
  );
}
