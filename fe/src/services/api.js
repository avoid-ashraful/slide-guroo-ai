import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const slideAPI = {
  uploadSlide: async (file, language = 'en', difficultyLevel = 'intermediate', includeDiagrams = true) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', language);
    formData.append('difficulty_level', difficultyLevel);
    formData.append('include_diagrams', includeDiagrams);

    const response = await api.post('/slides/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export const topicAPI = {
  generateLesson: async (topic, language = 'en', difficultyLevel = 'intermediate', includeDiagrams = true) => {
    const response = await api.post('/topics/generate', {
      topic,
      language,
      difficulty_level: difficultyLevel,
      include_diagrams: includeDiagrams,
    });
    return response.data;
  },
};

export const chatAPI = {
  askQuestion: async (lessonId, question, language = 'en', context = null, conversationHistory = []) => {
    const response = await api.post('/chat/ask', {
      lesson_id: lessonId,
      question,
      language,
      context,
      conversation_history: conversationHistory,
    });
    return response.data;
  },

  storeLesson: async (lesson) => {
    const response = await api.post('/chat/store-lesson', lesson);
    return response.data;
  },
};

export const diagramAPI = {
  generateDiagram: async (concept, diagramType = null, context = null) => {
    const response = await api.post('/diagrams/generate', {
      concept,
      diagram_type: diagramType,
      context,
    });
    return response.data;
  },
};

export default api;
