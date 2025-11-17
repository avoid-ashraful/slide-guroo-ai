# SlideGuroo - Deployment Guide

Complete guide for deploying SlideGuroo to various cloud platforms.

## Quick Deploy Options

### Option 1: Render.com (Recommended - Free Tier Available)

**Benefits:**
- Free tier available
- Easy deployment from GitHub
- Automatic HTTPS
- Docker support
- Good for both frontend and backend

**Steps:**

1. **Push your code to GitHub** (if not already done)

2. **Deploy Backend:**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - Name: `slideguroo-backend`
     - Environment: `Docker`
     - Dockerfile Path: `be/Dockerfile`
     - Instance Type: Free
   - Add Environment Variables:
     ```
     LLM_PROVIDER=gemini
     GOOGLE_API_KEY=AIzaSyB8b-F2FDwA9hAd39RZP-GoSRGo5k-t0xk
     GEMINI_MODEL=gemini-2.0-flash
     PORT=8000
     ```
   - Click "Create Web Service"

3. **Deploy Frontend:**
   - Click "New +" → "Static Site"
   - Connect your GitHub repository
   - Configure:
     - Name: `slideguroo-frontend`
     - Build Command: `cd fe && npm install && npm run build`
     - Publish Directory: `fe/dist`
   - Add Environment Variable:
     ```
     VITE_API_URL=https://slideguroo-backend.onrender.com/api
     ```
   - Click "Create Static Site"

4. **Access your app:**
   - Frontend: `https://slideguroo-frontend.onrender.com`
   - Backend: `https://slideguroo-backend.onrender.com`

### Option 2: Railway.app (Easy & Fast)

**Benefits:**
- $5 free credit per month
- One-click deploy
- Automatic HTTPS
- Great developer experience

**Steps:**

1. **Deploy via Railway:**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli

   # Login
   railway login

   # Initialize project
   railway init

   # Deploy backend
   cd be
   railway up

   # Deploy frontend
   cd ../fe
   railway up
   ```

2. **Configure Environment Variables:**
   - Go to Railway dashboard
   - Select your backend service
   - Add environment variables:
     ```
     LLM_PROVIDER=gemini
     GOOGLE_API_KEY=AIzaSyB8b-F2FDwA9hAd39RZP-GoSRGo5k-t0xk
     GEMINI_MODEL=gemini-2.0-flash
     ```

3. **Get your URLs:**
   - Railway will provide URLs for both services
   - Update frontend VITE_API_URL to point to backend URL

### Option 3: Vercel (Frontend) + Render (Backend)

**Best for:**
- Maximum performance for frontend
- Free tier for both

**Frontend (Vercel):**

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Deploy:
   ```bash
   cd fe
   vercel
   ```

3. Set environment variable:
   ```bash
   vercel env add VITE_API_URL
   # Enter your backend URL
   ```

**Backend (Render):**
- Follow Render backend steps from Option 1

### Option 4: Google Cloud Run

**Benefits:**
- Serverless
- Pay per use
- Scales automatically
- Good integration with Gemini API

**Steps:**

1. **Install Google Cloud SDK:**
   ```bash
   # Install gcloud CLI
   # Visit: https://cloud.google.com/sdk/docs/install
   ```

2. **Authenticate:**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Deploy Backend:**
   ```bash
   cd be
   gcloud run deploy slideguroo-backend \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars="LLM_PROVIDER=gemini,GOOGLE_API_KEY=AIzaSyB8b-F2FDwA9hAd39RZP-GoSRGo5k-t0xk,GEMINI_MODEL=gemini-2.0-flash"
   ```

4. **Deploy Frontend:**
   ```bash
   cd ../fe
   # Update VITE_API_URL in .env to point to Cloud Run backend URL
   npm run build

   # Deploy to Cloud Storage + Cloud CDN
   gsutil mb gs://slideguroo-frontend
   gsutil -m cp -r dist/* gs://slideguroo-frontend
   gsutil web set -m index.html gs://slideguroo-frontend
   ```

### Option 5: AWS (Production Grade)

**Components:**
- Backend: ECS Fargate or App Runner
- Frontend: S3 + CloudFront
- Or use AWS Amplify for full stack

**Using AWS App Runner (Easiest):**

1. **Install AWS CLI:**
   ```bash
   # Visit: https://aws.amazon.com/cli/
   ```

2. **Deploy Backend:**
   ```bash
   aws apprunner create-service \
     --service-name slideguroo-backend \
     --source-configuration file://apprunner-source.json \
     --instance-configuration Cpu=1024,Memory=2048
   ```

3. **Deploy Frontend to S3:**
   ```bash
   cd fe
   npm run build
   aws s3 sync dist/ s3://slideguroo-frontend
   aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
   ```

### Option 6: Docker Compose on VPS

**For any VPS (DigitalOcean, Linode, etc.):**

1. **Setup VPS:**
   ```bash
   # SSH into your VPS
   ssh root@your-vps-ip

   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh

   # Install Docker Compose
   apt-get install docker-compose-plugin
   ```

2. **Deploy Application:**
   ```bash
   # Clone repository
   git clone https://github.com/your-username/slide-guroo-ai.git
   cd slide-guroo-ai

   # Configure environment
   cd be
   cp .env.example .env
   nano .env  # Add your API keys

   # Start services
   cd ..
   docker-compose up -d
   ```

3. **Setup Nginx (Reverse Proxy):**
   ```nginx
   # /etc/nginx/sites-available/slideguroo

   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }

       location /api {
           proxy_pass http://localhost:8000;
           proxy_http_version 1.1;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. **Setup SSL with Let's Encrypt:**
   ```bash
   apt-get install certbot python3-certbot-nginx
   certbot --nginx -d yourdomain.com
   ```

## Environment Variables

Required for all deployments:

```env
# Backend
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.0-flash
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=https://your-frontend-url.com
MAX_UPLOAD_SIZE=10485760
UPLOAD_DIR=./uploads

# Frontend
VITE_API_URL=https://your-backend-url.com/api
```

## Post-Deployment Checklist

- [ ] Backend health check works: `https://your-backend-url.com/health`
- [ ] Frontend loads correctly
- [ ] API documentation accessible: `https://your-backend-url.com/docs`
- [ ] File upload works (test with small PPT/PDF)
- [ ] Topic generation works
- [ ] Q&A chat works
- [ ] Diagrams render correctly
- [ ] CORS configured correctly
- [ ] HTTPS enabled
- [ ] Environment variables secured
- [ ] Monitoring/logging setup (optional)

## Monitoring & Logs

### Render.com
- View logs in Render dashboard
- Automatic metrics provided

### Railway
```bash
railway logs
```

### Google Cloud Run
```bash
gcloud logging read "resource.type=cloud_run_revision"
```

### Docker on VPS
```bash
docker-compose logs -f
```

## Scaling

### Render.com
- Upgrade to paid plan for better resources
- Enable auto-scaling

### Railway
- Adjust resources in dashboard
- Automatic scaling available

### Google Cloud Run
- Automatic scaling built-in
- Set min/max instances:
```bash
gcloud run services update slideguroo-backend \
  --min-instances=1 \
  --max-instances=10
```

## Cost Estimates

### Free Tier
- **Render.com**: Free (with limitations)
- **Railway**: $5/month free credit
- **Vercel**: Free for personal projects
- **Google Cloud**: Free tier + pay per use

### Production (Expected monthly costs)
- **Render.com**: $7-14/month
- **Railway**: $10-20/month
- **Google Cloud Run**: $5-15/month (pay per use)
- **AWS**: $20-50/month
- **VPS**: $5-12/month (DigitalOcean, Linode)

## Troubleshooting

### Common Issues

**1. CORS Errors**
- Ensure CORS_ORIGINS includes your frontend URL
- Check protocol (http vs https)

**2. API Key Not Working**
- Verify environment variable is set correctly
- Check spelling: `GOOGLE_API_KEY` not `GEMINI_API_KEY`

**3. File Uploads Failing**
- Check MAX_UPLOAD_SIZE
- Ensure upload directory is writable
- Verify cloud storage permissions (if using)

**4. Frontend Can't Connect to Backend**
- Verify VITE_API_URL is correct
- Must rebuild frontend after changing env vars
- Check backend is actually running

**5. Docker Build Fails**
- Clear Docker cache: `docker system prune -a`
- Check Dockerfile syntax
- Verify all files are committed to Git

## Security Best Practices

1. **Never commit `.env` files**
2. **Use environment variables for secrets**
3. **Enable HTTPS in production**
4. **Set appropriate CORS origins**
5. **Limit file upload sizes**
6. **Keep dependencies updated**
7. **Use read-only file systems where possible**
8. **Enable rate limiting for API endpoints**

## Backup & Disaster Recovery

### Backup User Uploads

**Docker Volume:**
```bash
docker run --rm \
  -v slideguroo_backend-uploads:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/uploads-backup-$(date +%Y%m%d).tar.gz -C /data .
```

**Cloud Storage:**
- Use managed object storage (S3, GCS, etc.)
- Enable versioning
- Set up automated backups

### Database (if added in future)
- Use managed database services
- Enable automated backups
- Set retention period
- Test restore procedures

## Updates & Maintenance

### Rolling Updates

**Render:**
- Push to GitHub
- Auto-deploys on commit

**Railway:**
```bash
railway up
```

**Docker on VPS:**
```bash
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Support

For deployment issues:
1. Check service-specific documentation
2. Review logs
3. Verify environment variables
4. Check DEPLOYMENT.md
5. Open GitHub issue

## License

MIT License - See LICENSE file for details

---

**Happy Deploying! 🚀**
