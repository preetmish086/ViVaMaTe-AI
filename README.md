# 🔬 ViVaMaTe AI

### Your AI-Powered Research Companion for Understanding, Presenting, and Defending Research Papers

ViVaMaTe AI is an intelligent research assistant that helps students, researchers, and professionals interact with research papers through Retrieval-Augmented Generation (RAG), AI-powered viva preparation, and real-time presentation analysis.

Instead of simply reading papers, users can:

* Ask questions directly from uploaded PDFs
* Switch between multiple AI expert personas
* Practice research paper presentations
* Receive AI-generated presentation feedback
* Prepare for technical viva examinations
* Improve communication, confidence, and engagement skills

---

## ✨ Features

### 📄 Research Paper Intelligence

* Upload any research paper in PDF format
* Automatic text extraction and chunking
* Semantic search using vector embeddings
* Retrieval-Augmented Generation (RAG)
* Source-grounded answers

---

### 🎭 Multi-Persona AI Assistant

Interact with your paper from different perspectives:

| Persona            | Role                                      |
| ------------------ | ----------------------------------------- |
| 📚 Professor       | Academic and rigorous explanations        |
| 🌱 Student         | Beginner-friendly understanding           |
| 🔍 Skeptic         | Critical questioning and challenges       |
| 💼 Industry Expert | Practical and deployment-focused insights |
| 🎯 Interviewer     | Viva and interview-style questioning      |

---

### 🎓 AI Viva Preparation

Generate and answer viva-style questions based on your uploaded research paper.

Features:

* Context-aware questioning
* Automated evaluation
* Performance tracking
* Research understanding assessment

---

### 🎤 Presentation Practice Mode

Dedicated Flask-powered presentation trainer that analyzes:

* Eye Contact
* Face Visibility
* Filler Words
* Speaking Confidence
* Audience Engagement

---

### 📊 Real-Time Presentation Analytics

ViVaMaTe AI evaluates:

* Confidence Score
* Engagement Score
* Eye Contact Rate
* Face Detection Rate
* Speaking Transcript
* Strengths
* Areas for Improvement

---

### 📈 Final Performance Dashboard

Comprehensive report including:

* Research Understanding Score
* Viva Performance
* Presentation Performance
* Communication Effectiveness
* Overall Readiness Score
* Radar Chart Visualization

---

## 🏗️ Architecture

PDF Upload
↓
Text Extraction (PyMuPDF)
↓
Chunking
↓
Embeddings (Sentence Transformers)
↓
FAISS Vector Store
↓
RAG Pipeline
↓
Groq LLM
↓
Streamlit Interface

Presentation Mode
↓
Flask Backend
↓
MediaPipe Face Tracking
↓
Speech Recognition
↓
Analytics Engine
↓
Results Dashboard

---

## 🛠️ Tech Stack

### Frontend

* Streamlit
* HTML
* CSS
* JavaScript
* Plotly

### Backend

* Python
* Flask

### AI & NLP

* Groq API
* LangChain
* Sentence Transformers
* FAISS
* Faster Whisper

### Computer Vision

* MediaPipe
* OpenCV

### Research Pipeline

* PyMuPDF
* Semantic Retrieval
* Retrieval-Augmented Generation (RAG)

---

## 🚀 Running Locally

### Clone Repository

```bash
git clone <your-repo-url>
cd ViVaMaTe-AI
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Streamlit

```bash
streamlit run app.py
```

### Start Presentation Practice Server

```bash
python flask_app.py
```

---

## 📸 Screenshots

Add screenshots here:

* Home Page
* Research Chat
* Viva Mode
* Practice Mode
* Final Report

---

## 🎯 Future Improvements

* PPT Upload Support
* Research Paper Summarization
* Voice-based Viva
* Multi-paper Knowledge Base
* Citation Generation
* Presentation Recording Export
* Cloud Deployment

---

## 👨‍💻 Developed By

Madhu
B.Tech CSE, IIIT Bhubaneswar

Built to make research papers easier to understand, explain, present, and defend.