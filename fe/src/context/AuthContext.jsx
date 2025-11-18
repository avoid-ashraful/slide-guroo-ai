import { createContext, useState, useEffect, useContext } from 'react';
import { authService, tokenManager } from '../services/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Initialize auth state on mount
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const token = tokenManager.getToken();
        const storedUser = tokenManager.getUser();

        if (token && storedUser) {
          // Verify token is still valid by fetching current user
          try {
            const currentUser = await authService.getCurrentUser(token);
            setUser(currentUser);
            setIsAuthenticated(true);
          } catch (error) {
            // Token is invalid - clear storage
            tokenManager.clear();
            setUser(null);
            setIsAuthenticated(false);
          }
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (email, password) => {
    try {
      const { token, user } = await authService.login({ email, password });
      setUser(user);
      setIsAuthenticated(true);
      return { success: true, user };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Login failed. Please try again.';
      return { success: false, error: errorMessage };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authService.register(userData);
      return { success: true, data: response };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Registration failed. Please try again.';
      return { success: false, error: errorMessage };
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  const verifyEmail = async (token) => {
    try {
      const response = await authService.verifyEmail(token);

      // Update user state if currently logged in
      if (user) {
        const updatedUser = { ...user, is_verified: true };
        setUser(updatedUser);
        tokenManager.setUser(updatedUser);
      }

      return { success: true, data: response };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Email verification failed.';
      return { success: false, error: errorMessage };
    }
  };

  const resendVerification = async (email) => {
    try {
      const response = await authService.resendVerification(email);
      return { success: true, data: response };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to resend verification email.';
      return { success: false, error: errorMessage };
    }
  };

  const forgotPassword = async (email) => {
    try {
      const response = await authService.forgotPassword(email);
      return { success: true, data: response };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to send reset email.';
      return { success: false, error: errorMessage };
    }
  };

  const resetPassword = async (token, newPassword) => {
    try {
      const response = await authService.resetPassword({ token, new_password: newPassword });
      return { success: true, data: response };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Password reset failed.';
      return { success: false, error: errorMessage };
    }
  };

  const refreshUser = async () => {
    try {
      const currentUser = await authService.getCurrentUser();
      setUser(currentUser);
      tokenManager.setUser(currentUser);
      return { success: true, user: currentUser };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to refresh user data.';
      return { success: false, error: errorMessage };
    }
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    register,
    logout,
    verifyEmail,
    resendVerification,
    forgotPassword,
    resetPassword,
    refreshUser,
    isEmailVerified: user?.is_verified || false,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
