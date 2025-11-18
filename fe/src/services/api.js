import axios from 'axios';
import { tokenManager } from './authService';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add authentication token
api.interceptors.request.use(
  (config) => {
    const token = tokenManager.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle authentication errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Token expired or invalid - clear auth data
      tokenManager.clear();

      // Redirect to login page
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

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

export const dashboardAPI = {
  getLessons: async (skip = 0, limit = 20, sourceType = null) => {
    const params = new URLSearchParams({ skip, limit });
    if (sourceType) params.append('source_type', sourceType);

    const response = await api.get(`/dashboard/lessons?${params.toString()}`);
    return response.data;
  },

  getLessonDetail: async (lessonId) => {
    const response = await api.get(`/dashboard/lessons/${lessonId}`);
    return response.data;
  },

  deleteLesson: async (lessonId) => {
    const response = await api.delete(`/dashboard/lessons/${lessonId}`);
    return response.data;
  },

  getStats: async () => {
    const response = await api.get('/dashboard/stats');
    return response.data;
  },

  getRecentActivity: async (limit = 10) => {
    const response = await api.get(`/dashboard/recent-activity?limit=${limit}`);
    return response.data;
  },
};

export default api;
