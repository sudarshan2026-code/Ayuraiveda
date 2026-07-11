import { useState, useRef } from 'react'
import { analyzeClinicalImage } from '../services/api'
import { useTranslation } from 'react-i18next'

export default function VisualScan() {
  const [image, setImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [scanning, setScanning] = useState(false)
  const [scanStep, setScanStep] = useState(0)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const fileInputRef = useRef(null)

  const scanSteps = [
    "🔍 Initializing Tridosha Vision Engine™...",
    "📐 Mapping body frame and aspect ratios...",
    "📊 Calibrating shoulder-to-hip width matrices...",
    "💡 Performing skin texture and redness detection...",
    "🧠 Running clinical Guna → Dosha classification..."
  ]

  const handleImageChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setError(null)
      setImage(file)
      
      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const triggerFileSelect = () => {
    fileInputRef.current.click()
  }

  const runSimulation = () => {
    setScanning(true)
    setScanStep(0)
    setError(null)
    setResult(null)

    // Cycle through steps
    const interval = setInterval(() => {
      setScanStep(prev => {
        if (prev < scanSteps.length - 1) {
          return prev + 1
        } else {
          clearInterval(interval)
          return prev
        }
      })
    }, 1200)

    return interval
  }

  const handleStartScan = async () => {
    if (!imagePreview) return

    const interval = runSimulation()

    try {
      // Send base64 data to backend
      const res = await analyzeClinicalImage(imagePreview)
      
      // Give the scanning animation a moment to finish smoothly
      setTimeout(() => {
        clearInterval(interval)
        if (res.success) {
          setResult(res)
        } else {
          setError(res.error || 'Failed to analyze the body structure.')
        }
        setScanning(false)
      }, 6000)

    } catch (err) {
      clearInterval(interval)
      setError('Connection error. Please check if the Flask server is running.')
      setScanning(false)
    }
  }

  const resetScan = () => {
    setImage(null)
    setImagePreview(null)
    setResult(null)
    setError(null)
    setScanning(false)
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-10 page-enter">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-olive-800 mb-2">🌿 Akriti Pariksha</h1>
        <p className="text-olive-600 text-sm max-w-xl mx-auto">
          Digital Ayurvedic Body & Face Inspection. Upload a photo to map your physical frame, proportions, and skin attributes to estimate your Prakriti dosha balance.
        </p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600 flex items-center justify-between">
          <span>{error}</span>
          <button onClick={() => setError(null)} className="text-red-800 font-bold ml-2">×</button>
        </div>
      )}

      {/* ── STEP 1: Upload or Capture ── */}
      {!imagePreview && !result && (
        <div 
          onClick={triggerFileSelect}
          className="border-2 border-dashed border-olive-300 rounded-3xl p-12 text-center bg-cream-50 hover:bg-cream-100/50 hover:border-olive-500 cursor-pointer transition-all duration-300 flex flex-col items-center justify-center min-h-[350px] shadow-sm"
        >
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleImageChange} 
            accept="image/*" 
            capture="user" 
            className="hidden" 
          />
          <div className="w-16 h-16 bg-olive-100 rounded-2xl flex items-center justify-center mb-4 text-olive-600 text-2xl shadow-inner">
            📷
          </div>
          <h3 className="text-lg font-semibold text-olive-800 mb-1">Take Photo or Upload Image</h3>
          <p className="text-olive-500 text-xs max-w-xs mx-auto mb-4">
            For best results, ensure your full upper body or face is clearly visible in a well-lit environment.
          </p>
          <button className="btn-primary py-2 px-6 text-sm">
            Open Camera / Upload
          </button>
        </div>
      )}

      {/* ── STEP 2: Selected Image & Scan Process ── */}
      {imagePreview && !result && (
        <div className="card max-w-lg mx-auto overflow-hidden relative">
          <div className="relative aspect-[4/3] bg-black flex items-center justify-center overflow-hidden rounded-2xl">
            <img 
              src={imagePreview} 
              alt="Scan Preview" 
              className="max-h-full max-w-full object-contain"
            />
            
            {/* Holographic scanning laser line */}
            {scanning && (
              <>
                <div className="absolute left-0 right-0 h-1 bg-gradient-to-r from-transparent via-olive-400 to-transparent shadow-[0_0_15px_#a0ad5a] animate-sweep z-10" />
                <div className="absolute inset-0 bg-olive-500/10 backdrop-blur-[0.5px] pointer-events-none" />
                
                {/* Simulated scan grid overlay */}
                <div className="absolute inset-0 grid grid-cols-4 grid-rows-4 opacity-25 border border-olive-500 pointer-events-none">
                  {[...Array(16)].map((_, i) => (
                    <div key={i} className="border-t border-l border-olive-500" />
                  ))}
                </div>
              </>
            )}
          </div>

          <div className="p-6">
            {scanning ? (
              <div className="text-center py-4">
                <div className="animate-spin text-2xl mb-3">🌀</div>
                <h4 className="text-sm font-semibold text-olive-800 transition-all duration-300">
                  {scanSteps[scanStep]}
                </h4>
                <div className="h-1.5 w-full bg-cream-200 rounded-full overflow-hidden mt-4">
                  <div 
                    className="h-full bg-olive-500 rounded-full transition-all duration-300"
                    style={{ width: `${((scanStep + 1) / scanSteps.length) * 100}%` }}
                  />
                </div>
              </div>
            ) : (
              <div className="flex gap-3">
                <button onClick={resetScan} className="btn-secondary flex-1 py-3 text-sm">
                  Cancel
                </button>
                <button onClick={handleStartScan} className="btn-primary flex-1 py-3 text-sm">
                  Matrix Scan Now →
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ── STEP 3: Scan Results & Doshic Breakdown ── */}
      {result && (
        <div className="space-y-6">
          <div className="card p-6">
            <h2 className="text-xl font-bold text-olive-800 mb-6 text-center">📊 Physical Anthropometric Report</h2>
            
            {/* Visual Dosha Chart */}
            <div className="grid grid-cols-3 gap-4 mb-8 text-center">
              <div className="bg-orange-50 border border-orange-200 rounded-2xl p-4 shadow-sm">
                <div className="text-xs font-semibold text-orange-700 uppercase tracking-wider">Vata</div>
                <div className="text-3xl font-extrabold text-orange-800 my-1">{Math.round(result.vata_percentage || 0)}%</div>
                <div className="text-[10px] text-orange-600">Air & Ether</div>
              </div>
              <div className="bg-red-50 border border-red-200 rounded-2xl p-4 shadow-sm">
                <div className="text-xs font-semibold text-red-700 uppercase tracking-wider">Pitta</div>
                <div className="text-3xl font-extrabold text-red-800 my-1">{Math.round(result.pitta_percentage || 0)}%</div>
                <div className="text-[10px] text-red-600">Fire & Water</div>
              </div>
              <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-4 shadow-sm">
                <div className="text-xs font-semibold text-emerald-700 uppercase tracking-wider">Kapha</div>
                <div className="text-3xl font-extrabold text-emerald-800 my-1">{Math.round(result.kapha_percentage || 0)}%</div>
                <div className="text-[10px] text-emerald-600">Water & Earth</div>
              </div>
            </div>

            {/* Extracted Metrics Table */}
            <div className="border border-cream-200 rounded-2xl overflow-hidden mb-6">
              <div className="bg-cream-100 px-4 py-3 text-xs font-semibold text-olive-800 border-b border-cream-200">
                🧬 Extracted Structural Matrices
              </div>
              <div className="divide-y divide-cream-100 text-sm">
                {result.features && Object.entries(result.features).map(([key, val]) => (
                  <div key={key} className="flex justify-between px-4 py-2.5">
                    <span className="text-olive-700 font-medium capitalize">{key.replace('_', ' ')}</span>
                    <span className="text-olive-900 font-bold">{(val * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Assessment Details */}
            {result.analysis && (
              <div className="bg-cream-50 border border-olive-200 rounded-2xl p-5 mb-6 text-sm text-olive-800 space-y-4">
                <h3 className="font-bold text-olive-900 border-b border-olive-200 pb-2">📋 Clinical Diagnostics</h3>
                <div>
                  <span className="font-semibold text-olive-900">Gunas Detected:</span>{" "}
                  {result.analysis.gunas ? result.analysis.gunas.join(', ') : 'N/A'}
                </div>
                <div>
                  <span className="font-semibold text-olive-900">Dominant Imbalance:</span>{" "}
                  {result.analysis.imbalance || 'N/A'}
                </div>
                <p className="leading-relaxed whitespace-pre-line text-xs bg-white p-3 border border-cream-200 rounded-xl mt-2 text-olive-700">
                  {result.analysis.description || 'Scan completed successfully. Your physical structure shows balanced ratios with stable Guna measurements.'}
                </p>
              </div>
            )}

            <div className="flex gap-3">
              <button onClick={resetScan} className="btn-primary w-full py-3 text-sm">
                Scan Another Photo
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Sweep laser line animation styles */}
      <style>{`
        @keyframes sweep {
          0% { top: 0%; }
          50% { top: 100%; }
          100% { top: 0%; }
        }
        .animate-sweep {
          animation: sweep 3s infinite linear;
        }
      `}</style>
    </div>
  )
}
