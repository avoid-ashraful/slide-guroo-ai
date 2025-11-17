import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { BookOpen, Loader2, AlertCircle, Sparkles } from 'lucide-react'
import { topicAPI, chatAPI } from '../services/api'

function TopicGenerator({ currentLanguage }) {
  const navigate = useNavigate()
  const [topic, setTopic] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [difficultyLevel, setDifficultyLevel] = useState('intermediate')
  const [includeDiagrams, setIncludeDiagrams] = useState(true)

  const exampleTopics = [
    'Photosynthesis',
    'World War 2',
    'Quantum Physics',
    'Shakespeare\'s Macbeth',
    'Climate Change',
    'Algebra Basics',
    'Cell Biology',
    'French Revolution',
  ]

  const handleGenerate = async () => {
    if (!topic.trim()) {
      setError('Please enter a topic')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await topicAPI.generateLesson(
        topic,
        currentLanguage,
        difficultyLevel,
        includeDiagrams
      )

      // Store lesson for Q&A
      await chatAPI.storeLesson(response.lesson)

      // Navigate to lesson view
      navigate(`/lesson/${response.lesson_id}`, {
        state: { lesson: response.lesson }
      })
    } catch (err) {
      console.error('Generation error:', err)
      setError(err.response?.data?.detail || 'Failed to generate lesson. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleExampleClick = (exampleTopic) => {
    setTopic(exampleTopic)
    setError(null)
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12 fade-in">
        <div className="flex justify-center mb-4">
          <div className="bg-gradient-to-r from-purple-600 to-pink-600 p-3 rounded-2xl">
            <Sparkles className="text-white" size={40} />
          </div>
        </div>
        <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
          Learn Any Topic with AI
        </h2>
        <p className="text-xl text-gray-600">
          Enter any topic and AI will create a comprehensive lesson just for you
        </p>
      </div>

      {/* Input Section */}
      <div className="bg-white rounded-2xl shadow-xl p-8 mb-8 fade-in">
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            What would you like to learn about?
          </label>
          <div className="relative">
            <input
              type="text"
              value={topic}
              onChange={(e) => {
                setTopic(e.target.value)
                setError(null)
              }}
              placeholder="e.g., Photosynthesis, World War 2, Quantum Physics..."
              className="w-full border-2 border-gray-300 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-purple-500 transition"
              disabled={loading}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleGenerate()
                }
              }}
            />
            <BookOpen className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400" size={24} />
          </div>
        </div>

        {/* Example Topics */}
        <div className="mb-6">
          <p className="text-sm font-medium text-gray-700 mb-3">Popular topics:</p>
          <div className="flex flex-wrap gap-2">
            {exampleTopics.map((exampleTopic) => (
              <button
                key={exampleTopic}
                onClick={() => handleExampleClick(exampleTopic)}
                className="px-4 py-2 bg-gray-100 hover:bg-purple-100 text-gray-700 hover:text-purple-700 rounded-full text-sm font-medium transition"
                disabled={loading}
              >
                {exampleTopic}
              </button>
            ))}
          </div>
        </div>

        {/* Options */}
        <div className="space-y-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Difficulty Level
            </label>
            <select
              value={difficultyLevel}
              onChange={(e) => setDifficultyLevel(e.target.value)}
              className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
              disabled={loading}
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="include-diagrams-topic"
              checked={includeDiagrams}
              onChange={(e) => setIncludeDiagrams(e.target.checked)}
              className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
              disabled={loading}
            />
            <label htmlFor="include-diagrams-topic" className="ml-2 text-sm text-gray-700">
              Generate interactive diagrams (recommended)
            </label>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-2">
            <AlertCircle className="text-red-500 flex-shrink-0" size={20} />
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {/* Generate Button */}
        <button
          onClick={handleGenerate}
          disabled={!topic.trim() || loading}
          className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold py-3 px-6 rounded-lg hover:shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin" size={20} />
              Generating your lesson...
            </>
          ) : (
            <>
              <Sparkles size={20} />
              Generate Lesson
            </>
          )}
        </button>
      </div>

      {/* Features */}
      <div className="grid md:grid-cols-3 gap-6 fade-in">
        <div className="bg-white p-6 rounded-xl shadow-md">
          <div className="text-4xl mb-3">🔍</div>
          <h3 className="font-semibold text-lg mb-2">Web Research</h3>
          <p className="text-gray-600 text-sm">
            AI gathers information from multiple sources to create comprehensive content
          </p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-md">
          <div className="text-4xl mb-3">📊</div>
          <h3 className="font-semibold text-lg mb-2">Structured Learning</h3>
          <p className="text-gray-600 text-sm">
            Progressive lessons from fundamentals to advanced concepts
          </p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-md">
          <div className="text-4xl mb-3">🌍</div>
          <h3 className="font-semibold text-lg mb-2">Cultural Context</h3>
          <p className="text-gray-600 text-sm">
            Content adapted for Bangladeshi students with local examples
          </p>
        </div>
      </div>
    </div>
  )
}

export default TopicGenerator
