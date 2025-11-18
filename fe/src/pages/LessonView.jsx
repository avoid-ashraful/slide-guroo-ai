import { useState, useEffect, useRef } from 'react'
import { useLocation, useParams } from 'react-router-dom'
import {
  ChevronLeft,
  ChevronRight,
  MessageCircle,
  Send,
  Loader2,
  BookOpen,
  CheckCircle,
  Lightbulb,
  X,
} from 'lucide-react'
import MermaidDiagram from '../components/MermaidDiagram'
import { chatAPI } from '../services/api'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

function LessonView({ currentLanguage }) {
  const location = useLocation()
  const { lessonId } = useParams()
  const chatEndRef = useRef(null)

  const [lesson, setLesson] = useState(location.state?.lesson || null)
  const [currentSectionIndex, setCurrentSectionIndex] = useState(0)
  const [showChat, setShowChat] = useState(false)
  const [chatMessages, setChatMessages] = useState([])
  const [question, setQuestion] = useState('')
  const [loadingAnswer, setLoadingAnswer] = useState(false)

  const currentSection = lesson?.sections?.[currentSectionIndex]

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [chatMessages])

  const handleNextSection = () => {
    if (currentSectionIndex < lesson.sections.length - 1) {
      setCurrentSectionIndex(currentSectionIndex + 1)
    }
  }

  const handlePreviousSection = () => {
    if (currentSectionIndex > 0) {
      setCurrentSectionIndex(currentSectionIndex - 1)
    }
  }

  const handleAskQuestion = async () => {
    if (!question.trim()) return

    const userMessage = {
      role: 'user',
      content: question,
      timestamp: new Date().toISOString(),
    }

    setChatMessages(prev => [...prev, userMessage])
    setQuestion('')
    setLoadingAnswer(true)

    try {
      const context = `
Section: ${currentSection.title}
Content: ${currentSection.content}
      `.trim()

      const response = await chatAPI.askQuestion(
        lessonId,
        question,
        currentLanguage,
        context,
        chatMessages
      )

      const assistantMessage = {
        role: 'assistant',
        content: response.answer,
        timestamp: new Date().toISOString(),
        related_concepts: response.related_concepts,
        additional_examples: response.additional_examples,
      }

      setChatMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error asking question:', error)
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      }
      setChatMessages(prev => [...prev, errorMessage])
    } finally {
      setLoadingAnswer(false)
    }
  }

  if (!lesson) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <Loader2 className="animate-spin mx-auto mb-4 text-blue-600" size={48} />
          <p className="text-gray-600">Loading lesson...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-6 fade-in">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{lesson.title}</h1>
            <p className="text-gray-600 mb-4">{lesson.description}</p>
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                {lesson.subject}
              </span>
              <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">
                {lesson.difficulty_level}
              </span>
              <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
                {lesson.sections.length} Sections
              </span>
            </div>
          </div>

          <button
            onClick={() => setShowChat(!showChat)}
            className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:shadow-lg transition"
          >
            <MessageCircle size={20} />
            Ask Questions
          </button>
        </div>

        {/* Prerequisites */}
        {lesson.prerequisites && lesson.prerequisites.length > 0 && (
          <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <h3 className="font-semibold text-yellow-900 mb-2 flex items-center gap-2">
              <Lightbulb size={18} />
              Prerequisites
            </h3>
            <ul className="list-disc list-inside text-sm text-yellow-800">
              {lesson.prerequisites.map((prereq, idx) => (
                <li key={idx}>{prereq}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <div className="grid lg:grid-cols-12 gap-6">
        {/* Sidebar - Section Navigation */}
        <div className="lg:col-span-3">
          <div className="bg-white rounded-xl shadow-md p-4 sticky top-24 fade-in">
            <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <BookOpen size={18} />
              Lesson Sections
            </h3>
            <div className="space-y-2">
              {lesson.sections.map((section, idx) => (
                <button
                  key={section.id}
                  onClick={() => setCurrentSectionIndex(idx)}
                  className={`w-full text-left px-3 py-2 rounded-lg transition ${
                    idx === currentSectionIndex
                      ? 'bg-blue-100 text-blue-700 font-medium'
                      : 'hover:bg-gray-100 text-gray-700'
                  }`}
                >
                  <div className="flex items-start gap-2">
                    {idx < currentSectionIndex ? (
                      <CheckCircle size={18} className="text-green-500 flex-shrink-0 mt-0.5" />
                    ) : (
                      <div className="w-6 h-6 rounded-full border-2 border-gray-300 flex items-center justify-center flex-shrink-0 text-xs">
                        {idx + 1}
                      </div>
                    )}
                    <span className="text-sm">{section.title}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-9">
          <div className="bg-white rounded-xl shadow-md p-8 mb-6 fade-in">
            {/* Section Header */}
            <div className="mb-6">
              <div className="text-sm text-gray-500 mb-2">
                Section {currentSectionIndex + 1} of {lesson.sections.length}
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                {currentSection.title}
              </h2>
            </div>

            {/* Section Content */}
            <div className="lesson-content mb-8">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {currentSection.content}
              </ReactMarkdown>
            </div>

            {/* Diagram */}
            {currentSection.diagram && (
              <div className="mb-8">
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Visual Representation</h3>
                <MermaidDiagram code={currentSection.diagram} id={currentSection.id} />
              </div>
            )}

            {/* Examples */}
            {currentSection.examples && currentSection.examples.length > 0 && (
              <div className="mb-8 p-6 bg-blue-50 rounded-lg">
                <h3 className="text-lg font-semibold text-blue-900 mb-3 flex items-center gap-2">
                  <Lightbulb size={20} />
                  Examples
                </h3>
                <ul className="space-y-2">
                  {currentSection.examples.map((example, idx) => (
                    <li key={idx} className="text-blue-800">
                      <span className="font-medium">• </span>
                      {example}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Key Points */}
            {currentSection.key_points && currentSection.key_points.length > 0 && (
              <div className="mb-8 p-6 bg-green-50 rounded-lg">
                <h3 className="text-lg font-semibold text-green-900 mb-3 flex items-center gap-2">
                  <CheckCircle size={20} />
                  Key Points
                </h3>
                <ul className="space-y-2">
                  {currentSection.key_points.map((point, idx) => (
                    <li key={idx} className="text-green-800">
                      <span className="font-medium">✓ </span>
                      {point}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Navigation */}
            <div className="flex items-center justify-between pt-6 border-t">
              <button
                onClick={handlePreviousSection}
                disabled={currentSectionIndex === 0}
                className="flex items-center gap-2 px-4 py-2 border rounded-lg hover:bg-gray-50 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronLeft size={20} />
                Previous
              </button>

              <div className="text-sm text-gray-600">
                {currentSectionIndex + 1} / {lesson.sections.length}
              </div>

              <button
                onClick={handleNextSection}
                disabled={currentSectionIndex === lesson.sections.length - 1}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
                <ChevronRight size={20} />
              </button>
            </div>
          </div>

          {/* Summary (shown on last section) */}
          {currentSectionIndex === lesson.sections.length - 1 && lesson.summary && (
            <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl shadow-md p-8 fade-in">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Lesson Summary</h3>
              <div className="lesson-content">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {lesson.summary}
                </ReactMarkdown>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Chat Panel */}
      {showChat && (
        <div className="fixed bottom-6 right-6 w-96 bg-white rounded-xl shadow-2xl flex flex-col max-h-[600px] z-50 fade-in">
          {/* Chat Header */}
          <div className="flex items-center justify-between p-4 border-b bg-gradient-to-r from-blue-600 to-purple-600 rounded-t-xl">
            <h3 className="font-semibold text-white flex items-center gap-2">
              <MessageCircle size={20} />
              AI Tutor
            </h3>
            <button
              onClick={() => setShowChat(false)}
              className="text-white hover:bg-white/20 rounded p-1 transition"
            >
              <X size={20} />
            </button>
          </div>

          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {chatMessages.length === 0 ? (
              <div className="text-center text-gray-500 mt-8">
                <MessageCircle className="mx-auto mb-2 text-gray-400" size={32} />
                <p className="text-sm">Ask any question about this lesson!</p>
              </div>
            ) : (
              chatMessages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`${
                    msg.role === 'user' ? 'flex justify-end' : 'flex justify-start'
                  }`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-3 ${
                      msg.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-900'
                    }`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                    {msg.related_concepts && msg.related_concepts.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-gray-300">
                        <p className="text-xs font-semibold mb-1">Related Concepts:</p>
                        <ul className="text-xs space-y-1">
                          {msg.related_concepts.map((concept, i) => (
                            <li key={i}>• {concept}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
            {loadingAnswer && (
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-lg p-3">
                  <Loader2 className="animate-spin text-gray-600" size={20} />
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          {/* Chat Input */}
          <div className="p-4 border-t">
            <div className="flex gap-2">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !loadingAnswer) {
                    handleAskQuestion()
                  }
                }}
                placeholder="Ask a question..."
                className="flex-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loadingAnswer}
              />
              <button
                onClick={handleAskQuestion}
                disabled={!question.trim() || loadingAnswer}
                className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send size={20} />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default LessonView
