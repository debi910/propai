# Deployment Guide - PropAI

## GitHub Repository
✅ **All code pushed to:** https://github.com/debi910/propai

---

## Frontend Deployment - Netlify

### Option 1: Automatic Deployment (Recommended)

1. **Go to Netlify Dashboard**
   - Visit https://app.netlify.com/
   - Sign in with GitHub

2. **Create New Site**
   - Click "New site from Git"
   - Select GitHub as deployment method
   - Authorize Netlify to access your GitHub

3. **Select Repository**
   - Search for and select `debi910/propai`

4. **Configure Build Settings**
   - Build command: `cd frontend && npm run build`
   - Publish directory: `frontend/dist`
   - Environment variables:
     - `VITE_API_URL`: `https://propai-backend.railway.app/api`

5. **Deploy**
   - Click "Deploy site"
   - Netlify will automatically build and deploy on every push to main

### Option 2: Manual Deployment via Netlify CLI

```bash
# Install Netlify CLI globally
npm install -g netlify-cli

# Login to Netlify
netlify login

# Navigate to frontend directory
cd frontend

# Build the frontend
npm run build

# Deploy to Netlify
netlify deploy --prod --dir=dist
```

### Option 3: Direct Push to Deploy (Git-based)

1. Netlify watches your GitHub repository
2. Every push to `main` branch automatically triggers deployment
3. All configuration is in `netlify.toml`

---

## Backend Deployment - Railway

### Setup Backend on Railway

1. **Go to Railway Dashboard**
   - Visit https://railway.app/
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Click "Deploy from GitHub repo"
   - Select `debi910/propai`

3. **Configure Service**
   - Plugin: PostgreSQL (for Neon, skip - you already have it)
   - Environment Variables:
     ```
     DATABASE_URL=postgresql://neondb_owner:npg_Bd9LNy2PutYe@ep-cool-lab-anobxnbc.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require
     PORT=8000
     CORS_ORIGINS=https://your-netlify-domain.netlify.app
     ```

4. **Deploy**
   - Railway will automatically build from `Dockerfile` in backend/
   - Get your Railway URL once deployed

---

## Environment Variables

### Frontend (.env.local)
```
VITE_API_URL=https://propai-backend-railway.railway.app/api
```

### Backend (.env)
```
DATABASE_URL=postgresql://neondb_owner:npg_Bd9LNy2PutYe@ep-cool-lab-anobxnbc.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require
PORT=8000
CORS_ORIGINS=https://your-netlify-frontend.netlify.app
```

---

## Testing Deployments

### Test Frontend
```bash
# Build locally
cd frontend
npm run build

# Preview build
npm run preview
```

### Test Backend
```bash
# Run locally
cd backend
python -m uvicorn main:app --reload
```

---

## Live URLs (After Deployment)

- **Frontend (Netlify):** `https://propai.netlify.app` (or your custom domain)
- **Backend (Railway):** `https://propai-backend.railway.app`
- **GitHub:** https://github.com/debi910/propai

---

## Next Steps

1. ✅ Code pushed to GitHub
2. ⏳ Connect Netlify to GitHub repo
3. ⏳ Set up Railway backend
4. ⏳ Configure environment variables
5. ⏳ Verify API connectivity
6. ⏳ Test all features live

---

## Troubleshooting

### Build Fails on Netlify
- Check logs: Dashboard → Deploys → View logs
- Verify Node version (18.16.0)
- Ensure `npm run build` works locally

### CORS Errors
- Update backend `CORS_ORIGINS` with your Netlify URL
- Verify API_URL in frontend .env matches backend

### Missing Environment Variables
- Go to Netlify/Railway dashboard
- Set all required env vars before deploying
- Redeploy after adding env vars

---

## Support

For issues, check:
- GitHub Issues: https://github.com/debi910/propai/issues
- Netlify Docs: https://docs.netlify.com/
- Railway Docs: https://docs.railway.app/
