# StudyAbroad AI Counselor

An AI-powered chatbot that helps students who want to study abroad. The system acts as a 24/7 AI counselor that answers questions about universities, admission requirements, documents, and student visa processes using Retrieval Augmented Generation (RAG).

## Features

- **AI Chatbot**: Ask questions about universities, courses, admission requirements, visas, and scholarships
- **University Recommendations**: Get personalized university suggestions based on your profile
- **RAG-Powered Responses**: Uses knowledge base + LLM for accurate, grounded answers
- **Visa Guidance**: Detailed visa information for USA, Canada, UK, and Australia
- **Modern Chat UI**: Clean, responsive interface similar to ChatGPT

## Project Structure

```
study-abroad-ai/
├── backend/
│   ├── app.py              # Flask API with RAG implementation
│   ├── knowledge_base.json  # Structured dataset
│   ├── llm_service.py      # LLM API integration
│   ├── recommendation.py   # University recommendation engine
│   └── .env                # API configuration
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── style.css           # Styling
│   └── app.js              # Frontend logic
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Prerequisites

- Python 3.8+
- A Groq API key (free at https://console.groq.com)

## Setup Instructions

### 1. Clone/Create the Project

Create the project folder structure as shown above.

### 2. Configure API Key

Edit the `.env` file in the `backend/` folder:

```env
LLM_API_KEY=your_actual_groq_api_key_here
LLM_API_URL=https://api.groq.com/openai/v1/chat/completions
LLM_MODEL=llama-3.1-8b-instant
```

To get a Groq API key:
1. Go to https://console.groq.com
2. Sign up/Login
3. Click "Create API Key"
4. Copy the key and paste it in the .env file

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Backend

```bash
cd backend
python app.py
```

The server will start on http://localhost:5000

### 5. Open the Frontend

Open `frontend/index.html` in your browser, or serve it with a local server:

```bash
# Using Python
cd frontend
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Send a message to the chatbot |
| `/recommend-university` | POST | Get university recommendations |
| `/knowledge` | GET | Search universities |
| `/visa-info/<country>` | GET | Get visa information |
| `/universities` | GET | Get all universities |

## Example Usage

### Chat Message
```json
POST /chat
{"message": "What are the requirements for Canadian student visa?"}
```

### University Recommendation
```json
POST /recommend-university
{
  "country": "Canada",
  "budget": "45000",
  "ielts": "7.0",
  "field": "Computer Science",
  "gpa": "3.5"
}
```

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **AI**: Groq API (Llama 3.1 model)
- **Database**: JSON knowledge base

## Knowledge Base

The system includes:
- 20+ universities from USA, Canada, UK, Australia, and Germany
- Visa requirements for 4 countries
- Scholarship information
- Admission requirements (IELTS, GRE, GPA, deadlines)

## License

MIT License
