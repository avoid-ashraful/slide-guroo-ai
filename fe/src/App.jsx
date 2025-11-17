import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Home from './pages/Home'
import LessonView from './pages/LessonView'
import TopicGenerator from './pages/TopicGenerator'

function App() {
  const [currentLanguage, setCurrentLanguage] = useState('en')

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Header currentLanguage={currentLanguage} setCurrentLanguage={setCurrentLanguage} />

      <main className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Home currentLanguage={currentLanguage} />} />
          <Route path="/topic" element={<TopicGenerator currentLanguage={currentLanguage} />} />
          <Route path="/lesson/:lessonId" element={<LessonView currentLanguage={currentLanguage} />} />
        </Routes>
      </main>

      <footer className="bg-white border-t mt-16 py-8">
        <div className="container mx-auto px-4 text-center text-gray-600">
          <p className="mb-2">SlideGuroo - AI-Powered Student Learning Assistant</p>
          <p className="text-sm">Transforming education for students (Class 6-12 & University)</p>
        </div>
      </footer>
    </div>
  )
}

export default App
