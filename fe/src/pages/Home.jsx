import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload, FileText, Loader2, CheckCircle, AlertCircle } from 'lucide-react'
import { slideAPI, chatAPI } from '../services/api'

function Home({ currentLanguage }) {
  const navigate = useNavigate()
  const [file, setFile] = useState(null)
  const [dragActive, setDragActive] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [difficultyLevel, setDifficultyLevel] = useState('intermediate')
  const [includeDiagrams, setIncludeDiagrams] = useState(true)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
      setError(null)
    }
  }

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setError(null)
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file to upload')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await slideAPI.uploadSlide(
        file,
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
      console.error('Upload error:', err)
      setError(err.response?.data?.detail || 'Failed to process file. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12 fade-in">
        <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          Transform Your Slides into Interactive Lessons
        </h2>
        <p className="text-xl text-gray-600">
          Upload your PowerPoint or PDF slides and let AI create comprehensive, interactive lessons
        </p>
      </div>

      {/* Upload Section */}
      <div className="bg-white rounded-2xl shadow-xl p-8 mb-8 fade-in">
        <div
          className={`border-2 border-dashed rounded-xl p-12 text-center transition ${
            dragActive
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-300 hover:border-blue-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="file-upload"
            className="hidden"
            accept=".ppt,.pptx,.pdf,.docx,.doc"
            onChange={handleFileChange}
            disabled={loading}
          />

          {file ? (
            <div className="flex flex-col items-center gap-4">
              <CheckCircle className="text-green-500" size={48} />
              <div className="flex items-center gap-2 text-gray-700">
                <FileText size={20} />
                <span className="font-medium">{file.name}</span>
              </div>
              <button
                onClick={() => setFile(null)}
                className="text-sm text-blue-600 hover:underline"
                disabled={loading}
              >
                Choose different file
              </button>
            </div>
          ) : (
            <label htmlFor="file-upload" className="cursor-pointer">
              <Upload className="mx-auto mb-4 text-gray-400" size={48} />
              <p className="text-lg font-medium text-gray-700 mb-2">
                Drop your file here or click to browse
              </p>
              <p className="text-sm text-gray-500">
                Supports PPT, PPTX, PDF, DOCX (Max 10MB)
              </p>
            </label>
          )}
        </div>

        {/* Options */}
        <div className="mt-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Difficulty Level
            </label>
            <select
              value={difficultyLevel}
              onChange={(e) => setDifficultyLevel(e.target.value)}
              className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
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
              id="include-diagrams"
              checked={includeDiagrams}
              onChange={(e) => setIncludeDiagrams(e.target.checked)}
              className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              disabled={loading}
            />
            <label htmlFor="include-diagrams" className="ml-2 text-sm text-gray-700">
              Generate interactive diagrams (recommended)
            </label>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-2">
            <AlertCircle className="text-red-500 flex-shrink-0" size={20} />
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {/* Upload Button */}
        <button
          onClick={handleUpload}
          disabled={!file || loading}
          className="w-full mt-6 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-3 px-6 rounded-lg hover:shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin" size={20} />
              Processing your slides...
            </>
          ) : (
            <>
              <Upload size={20} />
              Generate Lesson
            </>
          )}
        </button>
      </div>

      {/* Features */}
      <div className="grid md:grid-cols-3 gap-6 fade-in">
        <div className="bg-white p-6 rounded-xl shadow-md">
          <div className="bg-blue-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
            <FileText className="text-blue-600" size={24} />
          </div>
          <h3 className="font-semibold text-lg mb-2">Comprehensive Lessons</h3>
          <p className="text-gray-600 text-sm">
            AI analyzes your slides and creates detailed, step-by-step explanations
          </p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-md">
          <div className="bg-purple-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
            <svg className="text-purple-600" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
              <line x1="9" y1="9" x2="15" y2="9"/>
              <line x1="9" y1="15" x2="15" y2="15"/>
            </svg>
          </div>
          <h3 className="font-semibold text-lg mb-2">Interactive Diagrams</h3>
          <p className="text-gray-600 text-sm">
            Visual representations for complex concepts to enhance understanding
          </p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-md">
          <div className="bg-green-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
            <svg className="text-green-600" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <h3 className="font-semibold text-lg mb-2">AI Q&A Assistant</h3>
          <p className="text-gray-600 text-sm">
            Ask questions anytime and get instant, detailed explanations
          </p>
        </div>
      </div>
    </div>
  )
}

export default Home
