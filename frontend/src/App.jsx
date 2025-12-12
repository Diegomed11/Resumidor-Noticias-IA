import React, { useState } from 'react';
import { Newspaper, Link as LinkIcon, FileText, Cpu, Activity, AlertCircle, CheckCircle2 } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('url'); // 'url' or 'text'
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!inputValue.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Petición al Backend (Flask)
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          type: activeTab,
          content: inputValue,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Error al conectar con el servidor');
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (label) => {
    if (label === 'POS') return 'text-green-500 bg-green-100 border-green-200';
    if (label === 'NEG') return 'text-red-500 bg-red-100 border-red-200';
    return 'text-blue-500 bg-blue-100 border-blue-200';
  };

  const getSentimentLabel = (label) => {
    if (label === 'POS') return 'Positivo';
    if (label === 'NEG') return 'Negativo';
    return 'Neutral';
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 font-sans selection:bg-blue-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Newspaper className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900 leading-none">NewsAI</h1>
              <span className="text-xs text-blue-600 font-medium">Analista Inteligente</span>
            </div>
          </div>
          <div className="hidden sm:flex items-center gap-2 text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
            <Cpu className="w-4 h-4" />
            <span>Powered by Transformers</span>
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-8">
        
        {/* Input Section */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden mb-8">
          {/* Tabs */}
          <div className="flex border-b border-gray-100">
            <button
              onClick={() => setActiveTab('url')}
              className={`flex-1 py-4 text-sm font-medium flex items-center justify-center gap-2 transition-colors ${
                activeTab === 'url' ? 'bg-blue-50 text-blue-700 border-b-2 border-blue-600' : 'text-gray-500 hover:bg-gray-50'
              }`}
            >
              <LinkIcon className="w-4 h-4" /> Analizar URL
            </button>
            <button
              onClick={() => setActiveTab('text')}
              className={`flex-1 py-4 text-sm font-medium flex items-center justify-center gap-2 transition-colors ${
                activeTab === 'text' ? 'bg-blue-50 text-blue-700 border-b-2 border-blue-600' : 'text-gray-500 hover:bg-gray-50'
              }`}
            >
              <FileText className="w-4 h-4" /> Texto Manual
            </button>
          </div>

          <div className="p-6">
            {activeTab === 'url' ? (
              <input
                type="url"
                placeholder="https://elpais.com/tecnologia/..."
                className="w-full p-4 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
              />
            ) : (
              <textarea
                placeholder="Pega aquí el contenido completo de la noticia..."
                className="w-full p-4 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all h-40 resize-none"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
              />
            )}

            <button
              onClick={handleSubmit}
              disabled={loading || !inputValue}
              className={`w-full mt-4 py-3 px-6 rounded-xl font-semibold text-white flex items-center justify-center gap-2 transition-all ${
                loading || !inputValue 
                  ? 'bg-gray-300 cursor-not-allowed' 
                  : 'bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-200 hover:shadow-blue-300 transform hover:-translate-y-0.5'
              }`}
            >
              {loading ? (
                <>
                  <Activity className="w-5 h-5 animate-spin" /> Procesando con IA...
                </>
              ) : (
                <>
                  <Cpu className="w-5 h-5" /> Analizar Noticia
                </>
              )}
            </button>
          </div>
        </div>

        {/* Error State */}
        {error && (
          <div className="mb-8 p-4 bg-red-50 text-red-600 rounded-xl border border-red-100 flex items-center gap-3 animate-in fade-in slide-in-from-top-4">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <p>{error}</p>
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-8 duration-500">
            
            {/* Sentiment Card */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-gray-100 rounded-lg">
                  <Activity className="w-6 h-6 text-gray-600" />
                </div>
                <div>
                  <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wider">Análisis de Sentimiento</h3>
                  <p className="text-2xl font-bold text-gray-800">
                    {Math.round(result.confidence * 100)}% <span className="text-sm font-normal text-gray-400">Confianza</span>
                  </p>
                </div>
              </div>
              
              <div className={`px-6 py-2 rounded-full border-2 text-lg font-bold flex items-center gap-2 ${getSentimentColor(result.sentiment)}`}>
                {getSentimentLabel(result.sentiment)}
                {result.sentiment === 'POS' ? '😊' : result.sentiment === 'NEG' ? '😔' : '😐'}
              </div>
            </div>

            {/* Summary Card */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
              <div className="bg-gray-50 px-6 py-4 border-b border-gray-100 flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-green-500" />
                <h3 className="font-semibold text-gray-700">Resumen Abstractivo</h3>
              </div>
              <div className="p-8">
                <p className="text-lg leading-relaxed text-gray-700">
                  {result.summary}
                </p>
                <div className="mt-6 pt-6 border-t border-gray-100 text-xs text-gray-400 flex justify-between">
                  <span>Generado por modelo mT5 (Google)</span>
                  <span>Longitud original: {result.original_length} caracteres</span>
                </div>
              </div>
            </div>

          </div>
        )}
      </main>
    </div>
  );
}

export default App;