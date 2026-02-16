# Render Deployment Guide

## Quick Start

### 1. Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:

**Build & Deploy:**
- **Name:** `tickora-backend`
- **Region:** Choose closest to your users
- **Branch:** `main` (or your default branch)
- **Root Directory:** `backend`
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `./start.sh`

### 2. Environment Variables

Add these in Render's Environment section:

```bash
# Database (Render will provide this if using Render PostgreSQL)
DATABASE_URL=<your-postgres-connection-string>

# JWT Secret (generate a secure random string)
SECRET_KEY=<generate-a-secure-random-key>

# Optional: Override defaults
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Database Setup

**Option A: Use Render PostgreSQL**
1. Create a PostgreSQL database in Render
2. Copy the "Internal Database URL"
3. Add it as `DATABASE_URL` environment variable

**Option B: Use Neon (Current)**
- Use your existing Neon connection string as `DATABASE_URL`

### 4. Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Install dependencies
   - Run migrations (`alembic upgrade head`)
   - Start the server on the assigned PORT

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `SECRET_KEY` | Yes | - | JWT secret key (use a strong random string) |
| `PORT` | No | 10000 | Server port (Render sets this automatically) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | 30 | JWT token expiration time |

## Startup Command

The `start.sh` script handles:
- Reading PORT from environment
- Running database migrations
- Starting uvicorn with proper host/port configuration

```bash
./start.sh
```

## CORS Configuration

Already configured for:
- `https://tickora-ai-story-flow.lovable.app`

To add more origins, update `app/main.py`:
```python
allow_origins=[
    "https://tickora-ai-story-flow.lovable.app",
    "https://your-other-domain.com"
]
```

## Health Check

Render will automatically check: `https://your-app.onrender.com/`

Returns: `{"message": "Welcome to Tickora API"}`

## API Documentation

Once deployed, access Swagger UI at:
`https://your-app.onrender.com/docs`

## Troubleshooting

### Build fails
- Check `requirements.txt` is in `backend/` directory
- Verify Python version compatibility

### App crashes on startup
- Check environment variables are set
- Verify `DATABASE_URL` is correct
- Check logs in Render dashboard

### Database connection fails
- Ensure `DATABASE_URL` is set
- Verify database is accessible from Render
- Check SSL mode if required

## Local Testing (Production Mode)

Test without `.env` file:

```bash
export DATABASE_URL="your-connection-string"
export SECRET_KEY="test-secret-key"
export PORT=10000
./start.sh
```
