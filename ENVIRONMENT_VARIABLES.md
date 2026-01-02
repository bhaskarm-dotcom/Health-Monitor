# Environment Variables Guide

This document lists all environment variables required for the AI Project Health Monitor application.

## 🔑 Environment Variables

### Backend Environment Variables

Location: `backend/.env`

| Variable Name | Type | Required | Default Value | Description |
|--------------|------|----------|---------------|-------------|
| `OPENAI_API_KEY` | String | No* | `""` | Your OpenAI API key for AI-powered features. If not provided, the system uses fallback keyword-based sentiment analysis. |
| `OPENAI_MODEL` | String | No | `gpt-3.5-turbo` | OpenAI model to use. Options: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo-preview` |

*Required only if you want AI-powered sentiment analysis and recommendations. Without it, the system uses fallback methods.

### Frontend Environment Variables

Location: `frontend/.env.local`

| Variable Name | Type | Required | Default Value | Description |
|--------------|------|----------|---------------|-------------|
| `NEXT_PUBLIC_API_URL` | String | No | `http://localhost:8001` | Backend API URL. Update this for production deployment. |

## 📝 Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Copy the example environment file:
```bash
cp .env.example .env
```

3. Edit `.env` and add your values:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-3.5-turbo
```

4. Get your OpenAI API key:
   - Go to: https://platform.openai.com/api-keys
   - Sign in or create an account
   - Click "Create new secret key"
   - Copy the key (starts with `sk-`)

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Create `.env.local` file:
```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8001" > .env.local
```

3. For production, update the API URL:
```env
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

## 🔐 Security Best Practices

1. **Never commit `.env` files** - They are already in `.gitignore`
2. **Use different keys for development and production**
3. **Rotate API keys regularly**
4. **Use environment-specific values**:
   - Development: `http://localhost:8001`
   - Production: Your deployed backend URL

## 📋 Example Values

### Development Environment

**Backend (`backend/.env`):**
```env
OPENAI_API_KEY=sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
OPENAI_MODEL=gpt-3.5-turbo
```

**Frontend (`frontend/.env.local`):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Production Environment

**Backend (`backend/.env`):**
```env
OPENAI_API_KEY=sk-proj-production-key-here
OPENAI_MODEL=gpt-4
```

**Frontend (`frontend/.env.local`):**
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## 🚀 Deployment

### Vercel/Netlify (Frontend)
Add environment variables in your deployment platform's dashboard:
- `NEXT_PUBLIC_API_URL` = Your backend API URL

### Heroku/AWS/Railway (Backend)
Add environment variables in your platform's dashboard:
- `OPENAI_API_KEY` = Your OpenAI API key
- `OPENAI_MODEL` = gpt-3.5-turbo (or your preferred model)

## ❓ Troubleshooting

### Backend can't find OpenAI API key
- Check that `.env` file exists in `backend/` directory
- Verify the key starts with `sk-` or `sk-proj-`
- Ensure no extra spaces or quotes around the value

### Frontend can't connect to backend
- Verify `NEXT_PUBLIC_API_URL` matches your backend URL
- Check that backend server is running
- Ensure CORS is configured correctly in backend

### AI features not working
- Verify `OPENAI_API_KEY` is set correctly
- Check your OpenAI account has credits/quota
- System will use fallback methods if key is missing

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Next.js Environment Variables](https://nextjs.org/docs/basic-features/environment-variables)
- [FastAPI Configuration](https://fastapi.tiangolo.com/advanced/settings/)

