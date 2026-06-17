# 🎓 ViVaMaTe AI

An AI-powered Research Understanding, Presentation Preparation, and Mock Viva Assistant designed to help students, researchers, and professionals quickly understand research papers, generate presentations, practice viva questions, and improve communication skills.

---

## 🚀 Overview

VivaMate AI transforms complex research papers into an interactive learning experience.

Instead of manually reading hundreds of pages and preparing presentations from scratch, users can:

* Upload research papers
* Chat with the paper using AI
* Generate presentation summaries
* Create slide-wise presentation content
* Practice research viva questions
* Receive performance reports and feedback

The platform acts as a personal research mentor, presentation coach, and viva examiner in one place.

---

## ✨ Key Features

### 📚 Research Arena

* Upload and index research papers
* Semantic search using vector embeddings
* Context-aware question answering
* Research-focused conversational interface
* Evidence-backed responses

### 📊 Presentation Generator

Automatically generates:

* 2-minute presentation summary
* 5-minute presentation summary
* Slide-by-slide presentation structure
* Speaker notes
* Key takeaways
* Likely viva questions

### 🎓 Mock Viva

Interactive viva simulation that:

* Generates research-based questions
* Evaluates user responses
* Provides scores and feedback
* Tracks viva performance history

### 🎤 Presentation Practice Mode

Practice presentations in a simulated environment.

Features include:

* Session tracking
* Confidence scoring
* Engagement scoring
* Presentation performance metrics
* Practice analytics

### 📈 Final Performance Report

Comprehensive report including:

* Research Understanding Score
* Viva Performance Score
* Presentation Score
* Overall Assessment
* Strengths Analysis
* Improvement Suggestions
* Radar Chart Visualization

---

## 🏗️ System Architecture

```text
Research Paper
      │
      ▼
PDF Processing
      │
      ▼
Text Chunking
      │
      ▼
Vector Embeddings
      │
      ▼
FAISS Vector Store
      │
      ▼
AI Retrieval System
      │
      ├── Research Chat
      ├── Presentation Generator
      ├── Mock Viva
      └── Performance Evaluation
```

---

## 🛠️ Technology Stack

### Frontend

* Streamlit

### AI & NLP

* LangChain
* OpenAI / LLM Integration
* Embedding Models

### Vector Database

* FAISS

### Document Processing

* PyPDF
* Text Chunking Pipeline

### Data Visualization

* Plotly

### Computer Vision (Practice Mode)

* OpenCV
* MediaPipe

---

## 📂 Project Structure

```text
VivaMate-AI/
│
├── app.py
│
├── modules/
│   ├── research_chat.py
│   ├── presentation_generator.py
│   ├── mock_viva.py
│   ├── presentation_practice.py
│   └── final_report.py
│
├── llm/
│   └── client.py
│
├── vectorstore/
│
├── uploads/
│
├── requirements.txt
│
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
cd VivaMate-AI
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
streamlit run app.py
```

---

## 🎯 Use Cases

* Research Paper Understanding
* Academic Presentation Preparation
* Thesis Defense Preparation
* Conference Presentation Training
* Mock Viva Practice
* Research Learning Assistant

---

## 🌟 Future Enhancements

* Real-time Eye Contact Detection
* Filler Word Analysis
* Voice Confidence Analysis
* Automatic PowerPoint Generation
* Multi-Paper Knowledge Base
* Team Collaboration Features
* Presentation Recording & Playback

---

## 👨‍💻 Developed For

AI-powered academic assistance and presentation preparation for students, researchers, educators, and professionals.

---

## 📄 License

This project is intended for educational and research purposes.
