# Render Backend Deployment Guide - PropAI

## Quick Setup for Render

### 1. Connect Repository to Render

1. Go to **https://render.com/**
2. Sign up/Login with GitHub
3. Click **"New +"** → **"Web Service"**
4. Select **"Build and deploy from a Git repository"**
5. Authorize Render to access GitHub
6. Select repository: `debi910/propai`
7. Branch: `main`

### 2. Configure Build Settings

- **Name:** `propai-backend` (or your choice)
- **Environment:** `Docker`
- **Region:** Choose closest to your users
- **Plan:** (Start with "Free" or "Starter")

**Important:** Render will automatically detect the Dockerfile in the root directory

### 3. Set Environment Variables

Go to **Environment** tab and add:

```env
DATABASE_URL=postgresql://neondb_owner:npg_Bd9LNy2PutYe@ep-cool-lab-anobxnbc.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require
PORT=8000
PYTHONUNBUFFERED=1
```

### 4. Configure Health Check (Optional)

- **Health Check Path:** `/api/cities`
- **Health Check Protocol:** `HTTP`

### 5. Deploy

Click **"Create Web Service"** - Render will:
- Clone your repository
- Build Docker image
- Deploy the application
- Assign a URL like: `https://propai-backend-xyz.onrender.com`

---

## Environment Variables Reference

Add these to Render dashboard under **Environment**:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | Your Neon PostgreSQL connection string |
| `PORT` | `8000` |
| `PYTHONUNBUFFERED` | `1` |
| `CORS_ORIGINS` | Your Netlify frontend URL |

---

## After Backend is Deployed

Once Render gives you the backend URL (e.g., `https://propai-backend-xyz.onrender.com`):

1. **Update Frontend Environment on Netlify:**
   - Go to Netlify dashboard → Site settings → Build & Deploy → Environment
   - Update `VITE_API_URL` to your Render backend URL:
     ```
     VITE_API_URL=https://propai-backend-xyz.onrender.com/api
     ```
   - Trigger a redeploy

2. **Update Backend CORS (if needed):**
   - In Render environment variables, update:
     ```
     CORS_ORIGINS=https://your-netlify-site.netlify.app
     ```

---

## Verify Deployment

Test your backend is working:

```bash
# Test health check endpoint
curl https://propai-backend-xyz.onrender.com/api/cities

# Should return list of cities (if database has data)
```

---

## Troubleshooting

### Build Fails with "Dockerfile not found"
- ✅ Fixed - Root-level Dockerfile already in repo

### Application crashes on start
- Check logs in Render dashboard → Logs
- Verify `DATABASE_URL` is correct
- Ensure database is accessible from Render

### CORS Errors from Frontend
- Add frontend URL to `CORS_ORIGINS` environment variable
- Redeploy backend after updating

### Slow Initial Load
- Render free tier spins down after 15 min of inactivity
- Consider upgrading to "Starter" plan for always-on

---

## Monitoring

In Render Dashboard:
- **Logs** - Real-time application logs
- **Metrics** - CPU, Memory, Network usage
- **Events** - Deployment history

---

## Free Tier Limits (Render)

- Application spins down after 15 minutes of inactivity
- 100GB/month bandwidth
- Shared resources
- Sufficient for demos/testing

Upgrade to paid plan for:
- Always-on applications
- Better performance
- More resources

---

## Next Steps

1. ✅ GitHub repo ready
2. ✅ Docker image ready
3. ⏳ Deploy backend to Render
4. ⏳ Get Render backend URL
5. ⏳ Update Netlify with Render URL
6. ⏳ Test live deployment

---

## Useful Links

- Render Docs: https://render.com/docs
- Build Docker Services: https://render.com/docs/deploy-docker
- Environment Variables: https://render.com/docs/environment-variables
- PostgreSQL Connection: https://render.com/docs/databases
