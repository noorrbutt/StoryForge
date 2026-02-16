# 🎮 PathEdPlay - Interactive Story Generator

A full-stack choose-your-own-adventure story generator powered by **FREE AI** (Groq). Create engaging, branching narratives with multiple paths and endings.

> **Note:** This project was inspired by [Tech With Tim's Choose-Your-Own-Adventure-AI](https://github.com/techwithtim/Choose-Your-Own-Adventure-AI). This version uses Groq (free) instead of OpenAI and includes enhanced features like balanced difficulty and improved story generation.

![Story Generator Demo](https://img.shields.io/badge/Status-Live-success)
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![React](https://img.shields.io/badge/React-18+-61dafb)
![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black)

## 🌐 Live Demo

**Try it now:** [https://pathedplay.vercel.app](https://pathedplay.vercel.app)

No installation required! Start generating stories instantly.

---

## ✨ Features

- 🤖 **FREE AI-powered story generation** using Groq (Llama 3.1)
- 🎯 **Balanced gameplay** - 1 winning path, 3 losing paths per story
- 🌳 **Multi-level decision trees** - 2 choice points with 4 possible endings
- 🎨 **Custom themes** - Generate stories for any genre (fantasy, sci-fi, horror, etc.)
- ⚡ **Lightning fast** - Stories ready in 8-12 seconds
- 💾 **Persistent stories** - PostgreSQL database with full story history
- 🌍 **Deployed on Vercel** - Serverless, auto-scaling, globally distributed
- 🔒 **Secure database** - Powered by Neon Postgres

---

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Groq** - FREE LLM API (Llama 3.1-8B-Instant)
- **SQLAlchemy** - Database ORM
- **Neon Postgres** - Serverless PostgreSQL database
- **Pydantic** - Data validation
- **Vercel Serverless Functions** - Auto-scaling backend

### Frontend
- **React** - UI library
- **React Router** - Navigation
- **Axios** - HTTP client
- **Vite** - Build tool
- **Vercel Edge Network** - Global CDN

### Infrastructure
- **Vercel** - Deployment platform
- **Neon** - PostgreSQL hosting
- **GitHub Actions** - CI/CD (auto-deploy on push)

---

## 🚀 Deploy Your Own

Want to deploy your own version? Follow these steps:

### Prerequisites

- GitHub account
- Vercel account (free)
- Groq API key ([Get one free here](https://console.groq.com))

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/PathEdPlay.git
cd PathEdPlay
```

### 2. Deploy to Vercel

#### Option A: Using Vercel Dashboard (Easiest)

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel auto-detects the configuration
5. Click "Deploy"

#### Option B: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

### 3. Add Neon Postgres Database

1. In your Vercel project dashboard, go to **Storage** tab
2. Click **"Create Database"**
3. Select **"Neon"** (Serverless Postgres)
4. Click **"Create"**
5. Vercel automatically adds `POSTGRES_URL` to your environment variables

### 4. Add Groq API Key

1. Get your free API key from [console.groq.com](https://console.groq.com)
2. In Vercel dashboard, go to **Settings** → **Environment Variables**
3. Add:
   - **Key:** `GROQ_API_KEY`
   - **Value:** `gsk_your_key_here`
   - **Environments:** Select all (Production, Preview, Development)
4. Click **"Save"**

### 5. Redeploy

After adding environment variables:
1. Go to **Deployments** tab
2. Click the **three dots** on latest deployment
3. Click **"Redeploy"**

**Done!** Your app is now live at `https://your-project.vercel.app` 🎉

---

## 💻 Local Development

Want to run it locally for development?

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
GROQ_API_KEY=your_groq_api_key_here
DEBUG=True
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### Run Locally

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Visit `http://localhost:5173` to use the application!

---

## 📁 Project Structure

```
├── api/
│   └── index.py                # Vercel serverless entry point
│
├── backend/
│   ├── core/
│   │   ├── config.py           # Configuration (Neon Postgres setup)
│   │   ├── models.py           # Pydantic models
│   │   ├── prompts.py          # AI prompts
│   │   └── story_generator.py  # Story generation logic (Groq)
│   ├── db/
│   │   └── database.py         # Database connection
│   ├── models/
│   │   ├── story.py            # Story & StoryNode models
│   │   └── job.py              # StoryJob model
│   ├── routers/
│   │   ├── story.py            # Story endpoints
│   │   └── job.py              # Job endpoints
│   ├── schemas/
│   │   ├── story.py            # Story schemas
│   │   └── job.py              # Job schemas
│   └── main.py                 # FastAPI app
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── StoryGenerator.jsx  # Main generator
│   │   │   ├── StoryLoader.jsx     # Story loader
│   │   │   ├── StoryGame.jsx       # Interactive UI
│   │   │   ├── ThemeInput.jsx      # Theme input
│   │   │   └── LoadingStatus.jsx   # Loading indicator
│   │   ├── App.jsx
│   │   └── util.js             # API configuration
│   └── package.json
│
├── vercel.json                 # Vercel deployment config
├── requirements.txt            # Python dependencies
└── README.md
```

---

## 🎮 How It Works

### Story Generation Flow

1. **User enters a theme** (e.g., "murder mystery", "space adventure")
2. **Frontend sends request** to `/api/stories/create`
3. **Backend creates a job** and starts generation in background
4. **Groq AI generates story** (7-node decision tree in ~10 seconds)
5. **Frontend polls job status** every second
6. **Story is saved to Neon Postgres** with unique `story_id`
7. **User plays the interactive story** making choices at each node

### Story Structure

```
Root Node
├─ Choice A (Wrong Path) ❌
│  ├─ Sub-choice 1 → Failure Ending ❌
│  └─ Sub-choice 2 → Failure Ending ❌
│
└─ Choice B (Right Path) ✓
   ├─ Smart Move → Success Ending ✓
   └─ Mistake → Failure Ending ❌
```

**Result:** 1 winning path out of 4 possible endings (25% success rate)

---

## 🔧 Configuration

### Environment Variables

**Required for Vercel Deployment:**
```env
GROQ_API_KEY=your_groq_api_key_here
POSTGRES_URL=auto_added_by_neon
```

**Optional (for local development):**
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
DEBUG=True
API_PREFIX=/api
```

---

## 📡 API Endpoints

### Stories
- `POST /api/stories/create` - Create new story generation job
- `GET /api/stories/jobs/{job_id}` - Check job status
- `GET /api/stories/{story_id}/complete` - Get complete story

### Health
- `GET /` - API info
- `GET /api/health` - Health check

---

## 🎨 Customization


### Changing Difficulty

Edit the prompt in `story_generator.py` to adjust win/loss ratio:

```python
# Current: 1 win, 3 losses (25% success)
# Easy mode: 2 wins, 2 losses (50% success)
# Hard mode: 1 win, 7 losses (12.5% success)
```

---

## 🐛 Troubleshooting

### Stories Not Generating

**Check Groq API key:**
1. Go to Vercel Dashboard → Settings → Environment Variables
2. Verify `GROQ_API_KEY` is set correctly
3. Test at [console.groq.com](https://console.groq.com)

**Check Vercel logs:**
1. Go to your project on Vercel
2. Click "Logs" tab
3. Look for errors during story generation

### Database Errors

**Check Neon connection:**
1. Go to Vercel Dashboard → Storage
2. Verify Neon database is connected
3. Check `POSTGRES_URL` is in environment variables

### Frontend Not Loading

**Check deployment status:**
1. Go to Vercel Dashboard → Deployments
2. Verify latest deployment succeeded
3. Check build logs for errors

### Timeout Errors (504)

**Groq generation takes too long:**
- Vercel free tier has 10-second timeout
- Groq usually responds in 8-12 seconds
- If hitting timeout, upgrade to Vercel Pro ($20/month for 50s timeout)

---

## 💰 Cost Breakdown

### Current Setup (100% FREE!)

| Service | Plan | Cost | Limits |
|---------|------|------|--------|
| **Vercel** | Hobby | FREE | 100 GB bandwidth, 100 serverless functions |
| **Neon** | Free | FREE | 0.5 GB storage, 5 GB monthly transfer |
| **Groq** | Free | FREE | 30 req/min, 14,400 tokens/min |

**Total monthly cost: $0** 🎉

## 🚀 Performance

- **Story Generation:** 8-12 seconds (Groq Llama 3.1-8B-Instant)
- **Cold Start:** ~1-2 seconds (Vercel serverless)
- **Database Queries:** <100ms (Neon Postgres)
- **Global CDN:** <50ms (Vercel Edge Network)

---

## 🔒 Security

- ✅ API keys stored securely in Vercel environment variables
- ✅ CORS configured for your domain only
- ✅ Database connection pooling via Neon
- ✅ HTTPS enforced (Vercel automatic SSL)
- ✅ No API keys in code or client-side

---

## 💡 Future Enhancements

- [ ] User accounts and authentication (Clerk/Auth0)
- [ ] Story sharing with unique URLs
- [ ] Save game progress
- [ ] Custom story templates
- [ ] AI image generation for scenes (DALL-E/Stable Diffusion)
- [ ] Voice narration (ElevenLabs)
- [ ] Multiplayer collaborative stories
- [ ] Story analytics dashboard
- [ ] Rate limiting and abuse prevention
- [ ] Story bookmarking and favorites

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🙏 Acknowledgments

- **[Tech With Tim](https://github.com/techwithtim)** - Project inspiration from [Choose-Your-Own-Adventure-AI](https://github.com/techwithtim/Choose-Your-Own-Adventure-AI)
- **[Groq](https://groq.com)** - For providing FREE, lightning-fast LLM API
- **[Vercel](https://vercel.com)** - Amazing deployment platform with generous free tier
- **[Neon](https://neon.tech)** - Serverless PostgreSQL made easy
- **[FastAPI](https://fastapi.tiangolo.com)** - Best Python web framework
- **[React](https://react.dev)** - Powerful UI library

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Check Groq API status at [console.groq.com](https://console.groq.com)

---

**Built with ❤️** | [Live Demo](https://pathedplay.vercel.app) 
