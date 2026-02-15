# 🎮 Interactive Story Generator

A full-stack choose-your-own-adventure story generator powered by **FREE AI** (Groq). Create engaging, branching narratives with multiple paths and endings.

> **Note:** This project was inspired by [Tech With Tim's Choose-Your-Own-Adventure-AI](https://github.com/techwithtim/Choose-Your-Own-Adventure-AI). This version uses Groq (free) instead of OpenAI and includes enhanced features like balanced difficulty and improved story generation.

![Story Generator Demo](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.13+-blue)
![React](https://img.shields.io/badge/React-18+-61dafb)

## ✨ Features

- 🤖 **FREE AI-powered story generation** using Groq (Llama 3.1)
- 🎯 **Balanced gameplay** - 1 winning path, 3 losing paths per story
- 🌳 **Multi-level decision trees** - 2 choice points with 4 possible endings
- 🎨 **Custom themes** - Generate stories for any genre (fantasy, sci-fi, horror, etc.)
- ⚡ **Fast generation** - Stories ready in 12-15 seconds
- 💾 **Persistent stories** - SQLite database with full story history
- 🔄 **Real-time updates** - Job polling system for generation status

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Groq** - FREE LLM API (Llama 3.1-8B-Instant)
- **SQLAlchemy** - Database ORM
- **SQLite** - Lightweight database (PostgreSQL ready)
- **Pydantic** - Data validation

### Frontend
- **React** - UI library
- **React Router** - Navigation
- **Axios** - HTTP client
- **Vite** - Build tool

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Node.js 16+
- Free Groq API key ([Get one here](https://console.groq.com))

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
cp .env.example .env

# Add your Groq API key to .env
# GROQ_API_KEY=your_key_here
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file (if needed)
cp .env.example .env
```

### Running the Application

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

## 📁 Project Structure

```
├── backend/
│   ├── core/
│   │   ├── config.py           # Configuration settings
│   │   ├── models.py           # Pydantic models
│   │   ├── prompts.py          # AI prompts
│   │   └── story_generator.py  # Story generation logic
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
│   ├── main.py                 # FastAPI app
│   └── .env.example            # Environment variables template
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── StoryGenerator.jsx  # Main generator component
│   │   │   ├── StoryLoader.jsx     # Story display loader
│   │   │   ├── StoryGame.jsx       # Interactive story UI
│   │   │   ├── ThemeInput.jsx      # Theme input form
│   │   │   └── LoadingStatus.jsx   # Loading indicator
│   │   ├── App.jsx
│   │   └── util.js             # API configuration
│   └── package.json
│
└── README.md
```

## 🎮 How It Works

### Story Generation Flow

1. **User enters a theme** (e.g., "murder mystery", "space adventure")
2. **Backend creates a job** and returns `job_id`
3. **Groq AI generates story** (7-node decision tree)
4. **Frontend polls job status** every second
5. **Story is saved to database** with unique `story_id`
6. **User plays the interactive story** making choices at each node

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

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
DEBUG=True
API_PREFIX=/api

# Database (optional - defaults to SQLite)
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=story_db
```

**Frontend (.env):**
```env
VITE_API_URL=http://localhost:8000
```

## 📡 API Endpoints

### Stories
- `POST /api/stories/create` - Create new story generation job
- `GET /api/stories/jobs/{job_id}` - Check job status
- `GET /api/stories/{story_id}/complete` - Get complete story

### Health
- `GET /` - API info
- `GET /health` - Health check

## 🎨 Customization

### Adjusting Story Depth

Edit `backend/core/story_generator.py`:

```python
# Change max_tokens for longer/shorter stories
max_tokens=2000  # Increase for more detailed stories

# Adjust temperature for creativity
temperature=0.8  # Higher = more creative, Lower = more consistent
```

### Adding More Themes

Pre-set themes can be added to the frontend theme selector:

```javascript
const themes = [
  "fantasy", "sci-fi", "horror", "mystery", 
  "romance", "adventure", "western", "cyberpunk"
];
```

### Changing Difficulty

Edit the prompt in `story_generator.py` to adjust win/loss ratio:

```python
# Current: 1 win, 3 losses (25% success)
# Easy mode: 2 wins, 2 losses (50% success)
# Hard mode: 1 win, 7 losses (12.5% success - requires deeper tree)
```

## 🐛 Troubleshooting

### "Groq not installed" error
```bash
pip install groq
```

### CORS errors
Make sure `ALLOWED_ORIGINS` includes your frontend URL in `.env`

### Stories not generating
1. Check Groq API key is valid
2. Check backend logs for errors
3. Verify Groq API is accessible (not blocked by firewall)

### Frontend polling timeout
Increase timeout in `StoryGenerator.jsx`:
```javascript
const maxAttempts = 60; // Increase to 120 for slower connections
```

## 🚀 Deployment

### Backend
1. Set environment variables in platform dashboard
2. Use PostgreSQL database instead of SQLite
3. Update `DEBUG=False` in production

### Frontend
1. Build: `npm run build`
2. Set `VITE_API_URL` to backend URL
3. Deploy `dist/` folder

## 💡 Future Enhancements

- [ ] User accounts and authentication
- [ ] Story sharing and social features
- [ ] Save game progress
- [ ] Custom story templates
- [ ] AI image generation for scenes
- [ ] Voice narration
- [ ] Multiplayer stories
- [ ] Story analytics dashboard

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- **[Tech With Tim](https://github.com/techwithtim)** -Project inspiration and concept from [Choose-Your-Own-Adventure-AI](https://github.com/techwithtim/Choose-Your-Own-Adventure-AI)
- [Groq](https://groq.com) - For providing FREE, fast LLM API
- [FastAPI](https://fastapi.tiangolo.com) - Amazing Python web framework
- [React](https://react.dev) - UI library

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Open an issue on GitHub
3. Check Groq API status at [console.groq.com](https://console.groq.com)

---

**Made with ❤️** | [Report Bug](../../issues) | [Request Feature](../../issues)
