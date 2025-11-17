import { Link } from 'react-router-dom'
import { BookOpen, Globe } from 'lucide-react'

function Header({ currentLanguage, setCurrentLanguage }) {
  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3 hover:opacity-80 transition">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-lg">
              <BookOpen className="text-white" size={28} />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                SlideGuroo
              </h1>
              <p className="text-xs text-gray-600">AI Learning Assistant</p>
            </div>
          </Link>

          <nav className="flex items-center gap-6">
            <Link
              to="/"
              className="text-gray-700 hover:text-blue-600 transition font-medium"
            >
              Upload Slides
            </Link>
            <Link
              to="/topic"
              className="text-gray-700 hover:text-blue-600 transition font-medium"
            >
              Learn Topic
            </Link>

            <div className="flex items-center gap-2 ml-4 border-l pl-4">
              <Globe size={20} className="text-gray-600" />
              <select
                value={currentLanguage}
                onChange={(e) => setCurrentLanguage(e.target.value)}
                className="border rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="en">English</option>
                <option value="bn">বাংলা</option>
              </select>
            </div>
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header
