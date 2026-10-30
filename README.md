# 🏥 HealthAI — Healthcare AI Microservice

An intelligent healthcare assistant powered by **Flask**, **LangGraph**, **LangChain**, and **Gemini AI**.

## 🚀 Quick Start

### 1. Clone & Configure
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 2. Run with Docker (Recommended)
```bash
docker-compose up --build
```

### 3. Run Locally
```bash
pip install -r requirements.txt
python run.py
```

Open **http://localhost:5000**

---

## 🤖 Agent Pipeline

```
User Input → Researcher → Planner → Scheduler → Summarizer → Report
```

| Agent | Role |
|-------|------|
| **Researcher** | Analyzes symptoms, identifies possible conditions |
| **Planner** | Creates treatment and care plan |
| **Scheduler** | Builds follow-up schedule and referrals |
| **Summarizer** | Compiles final patient summary report |

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Gunicorn
- **AI/ML**: LangGraph, LangChain, Gemini 1.5 Flash, FAISS, Sentence Transformers
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Docker, Docker Compose, AWS EC2

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main UI |
| `GET` | `/dashboard` | System dashboard |
| `POST` | `/api/analyze` | Run AI agent analysis |
| `GET` | `/api/health` | Health check |

### POST `/api/analyze`
```json
{
  "symptoms": "Severe headache, fever 101°F, fatigue for 3 days",
  "patient_info": "Age: 35 | Gender: Male | Medical History: None"
}
```

## ⚠️ Disclaimer

This application provides AI-generated health information for educational purposes only.
Always consult a licensed healthcare professional for medical advice.
