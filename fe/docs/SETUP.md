# Frontend Setup Guide

This guide will help you set up the SlideGuroo frontend application locally.

## Prerequisites

- Node.js 18.x or higher
- npm 9.x or higher (comes with Node.js)
- Backend API running (see [Backend Setup](../../be/docs/SETUP.md))

## Installation Steps

### 1. Navigate to Frontend Directory

```bash
cd slide-guroo-ai/fe
```

### 2. Install Dependencies

```bash
npm install
```

This will install all required packages including:
- React 18
- React Router DOM
- Axios
- Tailwind CSS
- Lucide React (icons)
- Mermaid (diagram rendering)

### 3. Configure Environment Variables

Create a `.env` file in the `fe/` directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
VITE_API_URL=http://localhost:8000/api
```

### 4. Start Development Server

```bash
npm run dev
```

The application will be available at: **http://localhost:5173**

### 5. Verify Installation

Open your browser and navigate to http://localhost:5173

You should see the SlideGuroo login page.

## Build for Production

### Create Production Build

```bash
npm run build
```

This creates an optimized production build in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

### Deploy Production Build

The `dist/` directory can be deployed to any static hosting service:

- **Vercel**: `vercel deploy`
- **Netlify**: Drag & drop `dist/` folder
- **AWS S3**: Upload `dist/` contents
- **GitHub Pages**: Push `dist/` to gh-pages branch

## Project Structure

```
fe/
├── public/                # Static assets
├── src/
│   ├── components/       # Reusable components
│   │   ├── Header.jsx
│   │   ├── MermaidDiagram.jsx
│   │   └── ProtectedRoute.jsx
│   ├── context/          # React Context providers
│   │   └── AuthContext.jsx
│   ├── pages/            # Page components
│   │   ├── Dashboard.jsx
│   │   ├── ForgotPassword.jsx
│   │   ├── Home.jsx
│   │   ├── LessonView.jsx
│   │   ├── Login.jsx
│   │   ├── ResetPassword.jsx
│   │   ├── Signup.jsx
│   │   ├── TopicGenerator.jsx
│   │   └── VerifyEmail.jsx
│   ├── services/         # API services
│   │   ├── api.js       # Main API client
│   │   └── authService.js
│   ├── App.jsx          # Root component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── docs/                # Documentation
│   ├── SETUP.md
│   └── USER_GUIDE.md
├── .env.example         # Environment template
├── .env                 # Your environment (gitignored)
├── package.json         # Dependencies
├── vite.config.js       # Vite configuration
├── tailwind.config.js   # Tailwind CSS config
└── index.html           # HTML template
```

## Available Scripts

| Script | Command | Description |
|--------|---------|-------------|
| `dev` | `npm run dev` | Start development server |
| `build` | `npm run build` | Create production build |
| `preview` | `npm run preview` | Preview production build |
| `lint` | `npm run lint` | Run ESLint |

## Development Workflow

### Hot Module Replacement (HMR)

Vite provides instant HMR. Changes to your code will be reflected immediately without full page reload.

### Code Formatting

The project uses ESLint for code quality. Run linting:

```bash
npm run lint
```

### Component Development

1. Create new components in `src/components/`
2. Create new pages in `src/pages/`
3. Add routes in `src/App.jsx`
4. Use Tailwind CSS for styling

Example component:

```jsx
function MyComponent() {
  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h2 className="text-xl font-bold">My Component</h2>
    </div>
  );
}

export default MyComponent;
```

## Environment Variables

### Available Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VITE_API_URL` | Yes | http://localhost:8000/api | Backend API URL |

### Accessing Environment Variables

In your code, access environment variables with `import.meta.env`:

```javascript
const apiUrl = import.meta.env.VITE_API_URL;
```

**Important**: Only variables prefixed with `VITE_` are exposed to your app.

## Styling with Tailwind CSS

### Tailwind Configuration

The project uses Tailwind CSS for styling. Configuration is in `tailwind.config.js`.

### Common Utility Classes

```jsx
// Layout
<div className="container mx-auto px-4">

// Flexbox
<div className="flex items-center justify-between">

// Grid
<div className="grid grid-cols-3 gap-4">

// Typography
<h1 className="text-3xl font-bold text-gray-900">

// Colors
<div className="bg-blue-600 text-white">

// Spacing
<div className="p-4 m-2">  // padding and margin

// Responsive
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
```

### Custom Colors

The theme uses custom colors defined in `tailwind.config.js`:

```javascript
colors: {
  blue: {
    600: '#2563eb',
    700: '#1d4ed8',
  },
  purple: {
    600: '#9333ea',
  }
}
```

## Routing

The app uses React Router v6 for client-side routing.

### Available Routes

| Path | Component | Authentication | Description |
|------|-----------|----------------|-------------|
| `/` | Home | Required (verified) | Upload slides page |
| `/topic` | TopicGenerator | Required (verified) | Generate topic lesson |
| `/lesson/:id` | LessonView | Required (verified) | View lesson details |
| `/dashboard` | Dashboard | Required | User dashboard |
| `/login` | Login | Public | Login page |
| `/signup` | Signup | Public | Registration page |
| `/verify-email` | VerifyEmail | Public | Email verification |
| `/forgot-password` | ForgotPassword | Public | Password reset request |
| `/reset-password` | ResetPassword | Public | Password reset form |

### Adding New Routes

Edit `src/App.jsx`:

```jsx
<Route path="/new-page" element={
  <ProtectedRoute>
    <NewPage />
  </ProtectedRoute>
} />
```

## Authentication

### AuthContext

The app uses React Context for authentication state management.

```jsx
import { useAuth } from '../context/AuthContext';

function MyComponent() {
  const { user, isAuthenticated, login, logout } = useAuth();

  // Access user info
  console.log(user.email);

  // Check if authenticated
  if (!isAuthenticated) {
    return <div>Please login</div>;
  }

  return <div>Welcome, {user.username}!</div>;
}
```

### Protected Routes

Use the `ProtectedRoute` component to protect routes:

```jsx
import ProtectedRoute from './components/ProtectedRoute';

<Route path="/protected" element={
  <ProtectedRoute requireVerified={true}>
    <ProtectedPage />
  </ProtectedRoute>
} />
```

Parameters:
- `requireVerified`: Require email verification (default: false)

### Token Management

Authentication tokens are stored in localStorage:

```javascript
import { tokenManager } from './services/authService';

// Get token
const token = tokenManager.getToken();

// Get user
const user = tokenManager.getUser();

// Clear auth data
tokenManager.clear();
```

## API Integration

### Making API Calls

Use the centralized API service:

```javascript
import { slideAPI, topicAPI, chatAPI, dashboardAPI } from './services/api';

// Upload slide
const response = await slideAPI.uploadSlide(file, 'en', 'intermediate', true);

// Generate topic lesson
const lesson = await topicAPI.generateLesson('Photosynthesis', 'en');

// Ask question
const answer = await chatAPI.askQuestion(lessonId, 'What is photosynthesis?');

// Get user lessons
const lessons = await dashboardAPI.getLessons(0, 10);
```

### Authentication Headers

The API client automatically adds authentication headers to all requests:

```javascript
// Configured in src/services/api.js
api.interceptors.request.use((config) => {
  const token = tokenManager.getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Error Handling

401 errors automatically redirect to login:

```javascript
// Configured in src/services/api.js
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      tokenManager.clear();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

## Common Issues

### Port Already in Use

**Error**: `Port 5173 is already in use`

**Solution**:
```bash
# Kill process on port 5173
lsof -i :5173
kill -9 <PID>

# Or use a different port
npm run dev -- --port 3000
```

### API Connection Error

**Error**: `Network Error` or CORS issues

**Solution**:
- Ensure backend is running at `http://localhost:8000`
- Check `VITE_API_URL` in `.env`
- Verify backend CORS configuration allows frontend origin

### Module Not Found

**Error**: `Cannot find module 'X'`

**Solution**:
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Build Fails

**Error**: Build errors in production

**Solution**:
```bash
# Clear Vite cache
rm -rf node_modules/.vite

# Rebuild
npm run build
```

### Authentication Issues

**Problem**: Login successful but immediately logged out

**Solution**:
- Check browser console for errors
- Verify token is being stored in localStorage
- Check `VITE_API_URL` matches backend URL
- Ensure backend `/auth/me` endpoint returns user data

## Browser Support

SlideGuroo supports modern browsers:

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Performance Optimization

### Code Splitting

Routes are automatically code-split by Vite for optimal loading.

### Image Optimization

For optimal performance:
- Use WebP format for images
- Compress images before uploading
- Use appropriate image sizes

### Bundle Size

Check bundle size:

```bash
npm run build
```

The build output will show chunk sizes.

## Accessibility

The application follows accessibility best practices:

- Semantic HTML elements
- ARIA labels where needed
- Keyboard navigation support
- Focus management
- Screen reader compatible

## Testing (Future)

Testing setup recommendations:

```bash
# Install testing libraries (not yet configured)
npm install -D @testing-library/react @testing-library/jest-dom vitest
```

## Next Steps

- Read the [User Guide](USER_GUIDE.md)
- Check [Backend API Documentation](../../be/docs/API.md)
- Review [Docker Setup](../../docs/DOCKER.md)

## Support

For issues or questions:
- Check documentation in `fe/docs/`
- Open an issue on GitHub
- Review code comments in source files
