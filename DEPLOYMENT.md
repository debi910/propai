# Deployment Guide for PropAI

## Free-Tier Services Used

| Service | Component | Free Tier | Link |
|---------|-----------|-----------|------|
| **Neon** | PostgreSQL + PostGIS | 100 CU-hrs/mo, auto-scale to zero | neon.tech |
| **Railway** | Backend API | 30-day trial + $5 credits | railway.app |
| **Vercel** | Frontend React | 100GB bandwidth/mo | vercel.com |
| **Mapbox** | 3D Map | 50K map loads/mo | mapbox.com |

---

## Phase 5: Backend Deployment (Railway)

### 1. Create Railway Account
- Visit: railway.app
- Sign up with GitHub (simplest)
- Create new project

### 2. Connect GitHub Repository
```bash
# In Railway dashboard:
1. Select "Deploy from GitHub"
2. Authorize & select your propai repo
3. Select branch: main
```

### 3. Set Environment Variables
In Railway dashboard → Environment Variables:
```
DATABASE_URL=postgresql://user:pass@host/dbname  # From Neon
FRONTEND_URL=https://propai.vercel.app  # Updated after frontend deploy
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=8000
```

### 4. Configure Start Command
In Railway → Settings → Start Command:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 5. Deploy
- Push to GitHub: `git push origin main`
- Railway auto-deploys
- Get public URL from Railway dashboard (e.g., propai-prod.railway.app)

### 6. Health Check
```bash
curl https://propai-prod.railway.app/health
```

---

## Phase 6: Frontend Deployment (Vercel)

### 1. Create Vercel Account
- Visit: vercel.com
- Sign up with GitHub
- Import propai repository

### 2. Configure Build Settings
```
Framework: Vite
Build Command: npm run build
Output Directory: dist
```

### 3. Set Environment Variables
In Vercel dashboard → Settings → Environment Variables:
```
VITE_API_URL=https://propai-prod.railway.app/api  # From Railway deploy
VITE_MAPBOX_TOKEN=pk_xxxxx  # Optional, your mapbox token
```

### 4. Deploy
- Vercel auto-deploys on git push
- Get URL: propai.vercel.app (or your custom domain)

### 5. Configure CORS
Update backend's FRONTEND_URL in Railway:
```
FRONTEND_URL=https://propai.vercel.app
```

Restart backend service in Railway dashboard.

---

## Phase 7: Data Pipeline (Cron Job)

### Option A: GitHub Actions (Recommended - Free, 20K min/month)

1. Create `.github/workflows/scraper.yml`:
```yaml
name: Daily Data Pipeline

on:
  schedule:
    # Run daily at 02:00 UTC (minimal load)
    - cron: '0 2 * * *'
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r data-pipeline/requirements.txt
          python -m spacy download en_core_web_sm
      
      - name: Run pipeline
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          cd data-pipeline
          python orchestrator.py
```

2. Add secrets to GitHub:
   - Settings → Secrets → Add: `DATABASE_URL`

### Option B: Railway Cron Worker

1. Create cron job file: `data-pipeline/Dockerfile` ✅ (already created)

2. Deploy as Railway service:
   - Create new Railway service from same repo
   - Root directory: `data-pipeline`
   - Start command: `python orchestrator.py`
   - Schedule: Every day at 02:00 UTC

---

## Database Migrations (Neon)

### Initial Setup
```bash
# From backend directory
psql postgresql://user:pass@host/dbname < database.sql
```

### Adding New Columns (Post-MVP)
```sql
-- Connect to Neon database
psql $DATABASE_URL

-- Example: Add new column
ALTER TABLE zones ADD COLUMN amenity_score INTEGER DEFAULT 0;
```

---

## Monitoring & Logs

### Railway Logs
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# View logs
railway logs --environment production
```

### Vercel Analytics
- Dashboard at: vercel.com/dashboard
- Real User Monitoring (RUM) enabled on Vercel Pro
- Check: https://propai.vercel.app to confirm deployment

### Neon Metrics
- Neon console → Monitoring
- Track: Connections, queries, storage used
- Alert if exceeding free tier (100 CU-hrs)

---

## Cost Monitoring

### Monthly Bill (MVP)
```
Neon:      $0   (100 CU-hrs free)
Railway:   $0-5 (free trial + $5 credits)
Vercel:    $0   (100GB bandwidth free)
Mapbox:    $0   (50K loads free)
───────────────────
TOTAL:     ~$5-10/mo after trial
```

### Scaling Beyond Free Tier
If costs become high:
1. **Neon:** Upgrade to $15/mo Launch plan
2. **Railway:** Switch to $20/mo Pro plan
3. **Mapbox:** Implement pay-as-you-go cap or self-hosted tiles (GeoServer)

---

## Custom Domain Setup

### Vercel Custom Domain
1. Vercel dashboard → Domains
2. Add: yourdomain.com
3. Update DNS records (instructions in Vercel)

### Railway Custom Domain
1. Railway dashboard → Domain
2. Add: api.yourdomain.com
3. CNAME to Railway URL

---

## Security Best Practices

### Environment Secrets
✅ DATABASE_URL in Railway environment only (not in code)
✅ Mapbox token in Vercel environment only
✅ .env files in .gitignore

### HTTPS
✅ Vercel: Auto HTTPS on vercel.app domain
✅ Railway: Auto HTTPS on railway.app domain
✅ Custom domains: Add SSL via Vercel/Railway

### Rate Limiting (Post-MVP)
```python
# Example: Add rate limiting to FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

---

## Monitoring Checklist

- [ ] Backend health check: `GET /health` returns 200
- [ ] Frontend loads: http://yourfrontend.com
- [ ] API accessible: Frontend can reach backend
- [ ] Sample data loaded: `/cities` returns 3 cities
- [ ] No 500 errors in Railway logs
- [ ] Database connections stable (Neon monitor)
- [ ] Mapbox behaves (if token configured)

---

## Troubleshooting Deployment

### "502 Bad Gateway" on Railway
- Check start command in Railway settings
- Check environment variables exist
- View logs: `railway logs --environment production`
- Restart service

### "CORS error" on frontend
- Verify FRONTEND_URL in Railway backend
- Check browser console for specific origin error
- Restart backend service

### "Database connection refused"
- Verify DATABASE_URL format
- Check if IP allowlist enabled on Neon (should be off for public)
- Test connection: `psql $DATABASE_URL -c "SELECT 1"`

### Frontend not updating after deploy
- Clear Vercel cache: Dashboard → Deployments → Redeploy
- Hard refresh in browser: Ctrl+Shift+R
- Check build logs in Vercel

---

## Rollback Plan

### If deployment fails:

1. **Frontend:**
```bash
vercel rollback
# OR push previous version to GitHub
```

2. **Backend:**
- Railway: Dashboard → Settings → Environment → Deploy Previous
- OR: `git revert <commit-hash> && git push`

3. **Database:**
- Neon: Backup automatically available
- Manual backup: `pg_dump $DATABASE_URL > backup.sql`

---

## What's Next

After successful deployment:
1. Share public URL with users
2. Monitor logs & metrics for 1 week
3. Iterate on Phase 7 (automation improvements)
4. Plan Phase 8+ (features, scaling, monitoring)

---

## Reference URLs (After Deploy)

| Service | URL |
|---------|-----|
| **Frontend** | https://propai.vercel.app |
| **Backend API** | https://propai-prod.railway.app |
| **API Docs** | https://propai-prod.railway.app/docs |
| **Database** | neon.tech console |
| **Logs** | Railway dashboard |

---

**First deployment estimated time: 30-45 minutes**
