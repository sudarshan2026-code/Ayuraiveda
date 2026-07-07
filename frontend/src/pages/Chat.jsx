import { useState, useEffect, useRef } from 'react'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../hooks/useAuth.jsx'
import { API_BASE_URL } from '../config'

// Simple Markdown to HTML parser
function renderMarkdown(text) {
  if (!text) return ''
  let html = text
    // Escaping HTML characters
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    // Horizontal lines
    .replace(/---/g, '<hr class="my-4 border-cream-200" />')
    // Bold text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // Headings
    .replace(/#### (.*?)\n/g, '<h5 class="text-sm font-bold text-olive-800 mt-3 mb-1">$1</h5>')
    .replace(/### (.*?)\n/g, '<h4 class="text-base font-bold text-olive-800 mt-4 mb-2">$1</h4>')
    .replace(/## (.*?)\n/g, '<h3 class="font-serif text-lg font-bold text-olive-800 mt-5 mb-2">$1</h3>')
    // Bullet lists
    .replace(/^\*\s+(.*?)$/gm, '<li class="list-disc ml-5 text-sm text-olive-700 my-1">$1</li>')
    // Line breaks
    .replace(/\n/g, '<br />')

  return <div className="space-y-1 text-sm md:text-base leading-relaxed" dangerouslySetInnerHTML={{ __html: html }} />
}

export default function Chat() {
  const { t, i18n } = useTranslation()
  const { user } = useAuth()
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Namaste! I am AyurVaani, your Ayurvedic AI physician. How can I help you today? Please tell me about any symptoms, food habits, sleep, or stress you are experiencing."
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [isListening, setIsListening] = useState(false)
  const [prakritiState, setPrakritiState] = useState('Checking baseline...')
  const [vikritiState, setVikritiState] = useState('Neutral')
  const [agniState, setAgniState] = useState('Balanced')
  const [amaState, setAmaState] = useState('None')
  const messagesEndRef = useRef(null)

  // Speech Recognition Setup (Web Speech API)
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  const recognition = SpeechRecognition ? new SpeechRecognition() : null

  if (recognition) {
    recognition.continuous = false
    recognition.lang = i18n.language === 'hi' ? 'hi-IN' : i18n.language === 'gu' ? 'gu-IN' : 'en-US'
    recognition.interimResults = false

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript
      setInput(prev => (prev + ' ' + transcript).trim())
      setIsListening(false)
    }

    recognition.onerror = () => {
      setIsListening(false)
    }

    recognition.onend = () => {
      setIsListening(false)
    }
  }

  const toggleVoiceInput = () => {
    if (!recognition) {
      alert("Speech recognition is not supported in this browser. Try Chrome or Safari.")
      return
    }

    if (isListening) {
      recognition.stop()
    } else {
      setIsListening(true)
      recognition.start()
    }
  }

  // Text-To-Speech (audio playback)
  const speakText = (text) => {
    if (!window.speechSynthesis) return
    window.speechSynthesis.cancel() // Stop any current speech
    
    // Strip markdown formatting for cleaner speech
    const cleanText = text
      .replace(/\*\*/g, '')
      .replace(/#/g, '')
      .replace(/[-*•]/g, '')
      .slice(0, 500) // Limit speech length

    const utterance = new SpeechSynthesisUtterance(cleanText)
    utterance.rate = 1.0
    utterance.pitch = 1.0
    window.speechSynthesis.speak(utterance)
  }

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Initial user Prakriti load
  useEffect(() => {
    if (user) {
      // Look up past local reports to populate initial values
      const local = JSON.parse(localStorage.getItem('ayur_reports') || '[]')
      if (local.length > 0) {
        const latest = local[0].result
        setPrakritiState(latest.dominant)
        setVikritiState(latest.vikriti)
        setAgniState(latest.agni_state)
        setAmaState(latest.ama_status)
      } else if (user.prakriti) {
        setPrakritiState(user.prakriti)
      } else {
        setPrakritiState('None (Take Assessment first)')
      }
    } else {
      setPrakritiState('Guest Session')
    }
  }, [user])

  const handleSend = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setLoading(true)

    // Construct user profile context
    const userProfile = {
      name: user?.name || 'Guest User',
      age: user?.age || 'N/A',
      gender: user?.gender || 'N/A',
      weight: user?.weight || 'N/A',
      height: user?.height || 'N/A',
      prakriti: user?.prakriti || 'Unknown',
      prakriti_scores: user?.prakriti_scores || { vata: 33.3, pitta: 33.3, kapha: 33.3 }
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: json_payload(userMessage, userProfile)
      })

      if (!response.ok) throw new Error('Failed to fetch chat response')
      
      const data = await response.json()
      
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
      
      // Update running diagnostic metadata sidebar
      if (data.prakriti) setPrakritiState(data.prakriti)
      if (data.vikriti) setVikritiState(data.vikriti)
      if (data.agni) setAgniState(data.agni)
      if (data.ama) setAmaState(data.ama)
      
    } catch (err) {
      console.error(err)
      setMessages(prev => [...prev, { role: 'assistant', content: 'Apologies, I encountered an issue in the Ayurvedic reasoning pipeline. Please try rephrasing.' }])
    } finally {
      setLoading(false)
    }
  }

  // Helper helper payload
  const json_payload = (message, profile) => {
    return JSON.stringify({
      message: message,
      session_id: user?.id || 'guest_session',
      user_profile: profile,
      language: i18n.language
    })
  }

  return (
    <div className="max-w-6xl mx-auto px-4 md:px-8 py-6">
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        {/* ── Diagnostic Sidebar ── */}
        <div className="lg:col-span-1 space-y-4">
          <div className="card border border-cream-200">
            <h2 className="font-serif text-lg font-bold text-olive-800 mb-4 flex items-center gap-2">
              <span>🩺</span> {t('chat.diagnostic_title')}
            </h2>
            
            <div className="space-y-4">
              <div>
                <p className="text-[10px] text-olive-400 uppercase tracking-wider font-semibold">{t('chat.prakriti_label')}</p>
                <p className="text-sm font-semibold text-olive-800 mt-1">{prakritiState}</p>
              </div>
              <div>
                <p className="text-[10px] text-olive-400 uppercase tracking-wider font-semibold">{t('chat.vikriti_label')}</p>
                <p className="text-sm font-semibold text-amber-700 mt-1">{vikritiState}</p>
              </div>
              <div>
                <p className="text-[10px] text-olive-400 uppercase tracking-wider font-semibold">{t('chat.agni_label')}</p>
                <p className="text-sm font-semibold text-olive-700 mt-1">{agniState}</p>
              </div>
              <div>
                <p className="text-[10px] text-olive-400 uppercase tracking-wider font-semibold">{t('chat.ama_label')}</p>
                <p className="text-sm font-semibold text-red-600 mt-1">{amaState}</p>
              </div>
            </div>
            
            <div className="border-t border-cream-100 mt-5 pt-4">
              <p className="text-[10px] text-olive-400 leading-relaxed">
                {t('chat.disclaimer')}
              </p>
            </div>
          </div>
        </div>

        {/* ── Main Chat Stream ── */}
        <div className="lg:col-span-3 flex flex-col h-[70vh] card border border-cream-200 bg-white p-0 overflow-hidden">
          {/* Header */}
          <div className="px-5 py-4 border-b border-cream-100 bg-olive-50/30 flex justify-between items-center shrink-0">
            <div className="flex items-center gap-3">
              <span className="text-2xl">🌬️</span>
              <div>
                <h1 className="font-semibold text-olive-800 text-sm md:text-base">{t('chat.title')}</h1>
                <p className="text-[10px] text-emerald-600 font-medium">{t('chat.status_active')}</p>
              </div>
            </div>
          </div>

          {/* Messages Stream */}
          <div className="flex-1 overflow-y-auto p-5 space-y-4 scrollbar-hide">
            {messages.map((m, idx) => {
              const isUser = m.role === 'user'
              const isWelcome = idx === 0 && m.role === 'assistant'
              const content = isWelcome ? t('chat.welcome_msg') : m.content
              return (
                <div key={idx} className={`flex ${isUser ? 'justify-end' : 'justify-start'} page-enter`}>
                  <div className={`max-w-[85%] rounded-2xl px-4 py-3 shadow-soft relative group
                    ${isUser 
                      ? 'bg-olive-600 text-white rounded-tr-none' 
                      : 'bg-cream-50 text-olive-800 border border-cream-100 rounded-tl-none'}`}
                  >
                    {isUser ? (
                      <p className="text-sm md:text-base leading-relaxed whitespace-pre-wrap">{content}</p>
                    ) : (
                      <>
                        {renderMarkdown(content)}
                        <div className="absolute right-2 bottom-1 hidden group-hover:block transition-all">
                          <button
                            onClick={() => speakText(content)}
                            title={t('chat.listen_tooltip')}
                            className="w-6 h-6 rounded-full bg-olive-100 hover:bg-olive-200 text-olive-700 flex items-center justify-center text-xs active:scale-95 shadow-soft"
                          >
                            🔊
                          </button>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              )
            })}

            {loading && (
              <div className="flex justify-start page-enter">
                <div className="bg-cream-50 text-olive-800 border border-cream-100 rounded-2xl rounded-tl-none px-4 py-3 flex items-center gap-1.5 shadow-soft">
                  <div className="w-2 h-2 rounded-full bg-olive-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 rounded-full bg-olive-400 animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 rounded-full bg-olive-400 animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Form Input */}
          <form onSubmit={handleSend} className="p-4 border-t border-cream-100 bg-olive-50/10 flex gap-3 items-center shrink-0">
            <button
              type="button"
              onClick={toggleVoiceInput}
              title={isListening ? t('chat.placeholder_listening') : t('chat.speak_tooltip')}
              className={`w-11 h-11 rounded-xl flex items-center justify-center font-bold text-lg active:scale-95 transition-all
                ${isListening 
                  ? 'bg-red-500 text-white animate-pulse shadow-glow' 
                  : 'bg-cream-100 text-olive-800 hover:bg-cream-200 border border-cream-200'}`}
            >
              🎤
            </button>
            
            <input
              type="text"
              placeholder={isListening ? t('chat.placeholder_listening') : t('chat.placeholder')}
              value={input}
              onChange={e => setInput(e.target.value)}
              disabled={loading}
              className="flex-1 border border-cream-200 rounded-xl px-4 py-2.5 text-sm md:text-base text-olive-800 bg-white focus:outline-none focus:border-olive-400"
            />
            
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="btn-primary py-2.5 px-5 text-sm shrink-0 flex items-center justify-center gap-1 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {t('chat.send')}
            </button>
          </form>
        </div>

      </div>
    </div>
  )
}
