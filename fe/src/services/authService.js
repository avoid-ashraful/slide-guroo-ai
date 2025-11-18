import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const authAPI = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Token management
const TOKEN_KEY = 'slideguroo_token';
const USER_KEY = 'slideguroo_user';

export const tokenManager = {
  getToken: () => {
    return localStorage.getItem(TOKEN_KEY);
  },

  setToken: (token) => {
    localStorage.setItem(TOKEN_KEY, token);
  },

  removeToken: () => {
    localStorage.removeItem(TOKEN_KEY);
  },

  getUser: () => {
    const user = localStorage.getItem(USER_KEY);
    return user ? JSON.parse(user) : null;
  },

  setUser: (user) => {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  },

  removeUser: () => {
    localStorage.removeItem(USER_KEY);
  },

  clear: () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  },
};

// Authentication API
export const authService = {
  /**
   * Register a new user
   * @param {Object} userData - User registration data
   * @param {string} userData.email - User email
   * @param {string} userData.username - Username
   * @param {string} userData.password - Password
   * @param {string} userData.full_name - Full name
   */
  register: async (userData) => {
    const response = await authAPI.post('/auth/register', userData);
    return response.data;
  },

  /**
   * Login user
   * @param {Object} credentials
   * @param {string} credentials.email - User email
   * @param {string} credentials.password - Password
   */
  login: async (credentials) => {
    const response = await authAPI.post('/auth/login', credentials);
    const { access_token, token_type } = response.data;

    // Store token
    tokenManager.setToken(access_token);

    // Fetch and store user info
    const user = await authService.getCurrentUser(access_token);
    tokenManager.setUser(user);

    return { token: access_token, user };
  },

  /**
   * Logout user
   */
  logout: () => {
    tokenManager.clear();
  },

  /**
   * Get current user info
   * @param {string} token - Optional token (uses stored token if not provided)
   */
  getCurrentUser: async (token = null) => {
    const authToken = token || tokenManager.getToken();
    if (!authToken) {
      throw new Error('No authentication token found');
    }

    const response = await authAPI.get('/auth/me', {
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });
    return response.data;
  },

  /**
   * Verify email
   * @param {string} token - Verification token
   */
  verifyEmail: async (token) => {
    const response = await authAPI.post('/auth/verify-email', { token });
    return response.data;
  },

  /**
   * Resend verification email
   * @param {string} email - User email
   */
  resendVerification: async (email) => {
    const response = await authAPI.post('/auth/resend-verification', { email });
    return response.data;
  },

  /**
   * Request password reset
   * @param {string} email - User email
   */
  forgotPassword: async (email) => {
    const response = await authAPI.post('/auth/forgot-password', { email });
    return response.data;
  },

  /**
   * Reset password with token
   * @param {Object} data
   * @param {string} data.token - Reset token
   * @param {string} data.new_password - New password
   */
  resetPassword: async (data) => {
    const response = await authAPI.post('/auth/reset-password', data);
    return response.data;
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated: () => {
    const token = tokenManager.getToken();
    const user = tokenManager.getUser();
    return !!(token && user);
  },

  /**
   * Check if user email is verified
   */
  isEmailVerified: () => {
    const user = tokenManager.getUser();
    return user && user.is_verified;
  },
};

export default authService;
