# ViVaMaTe AI

> An AI-powered research paper companion for understanding, presenting, practicing, and defending academic work.

ViVaMaTe AI turns a research paper into an interactive preparation workspace. Upload a PDF, ask grounded questions about the paper, switch between expert personas, generate presentation material, practice viva answers, analyze delivery quality, and review your readiness in a final performance dashboard.

The project combines a Streamlit research assistant with Flask-based practice surfaces for presentation delivery and voice viva preparation.

---

## Highlights

- PDF-based research paper ingestion and question answering
- Retrieval-Augmented Generation using FAISS and sentence-transformer embeddings
- Five AI personas for different review styles
- AI-generated summaries, slide outlines, takeaways, and viva questions
- Mock viva question generation and answer evaluation
- Camera and microphone based presentation practice mode
- Speech transcription with Faster Whisper
- Filler word, fluency, eye contact, face visibility, confidence, and engagement analysis
- Final readiness report with weighted scores and a radar chart
- Separate spoken viva practice server

---

## Core Features

### 1. Research Paper Intelligence

Upload a research paper as a PDF and let the app build a searchable knowledge base.

What happens after upload:

1. Text is extracted with PyMuPDF.
2. The paper is split into overlapping chunks.
3. Chunks are embedded with `sentence-transformers/all-MiniLM-L6-v2`.
4. A FAISS vector store is created in memory.
5. User questions retrieve the top matching chunks.
6. Groq-hosted LLM responses are generated from the retrieved context.

The chat is intentionally source-grounded. Answers are built from the retrieved paper chunks and include an expandable evidence panel showing the exact chunks used.

### 2. Multi-Persona Research Chat

The same paper can be explored from five perspectives:

| Persona | Focus |
| --- | --- |
| Professor | Formal academic explanation, methodology, findings, limitations |
| Student | Beginner-friendly explanations and simpler wording |
| Skeptic | Critical review, assumptions, gaps, and probing questions |
| Industry Expert | Practical feasibility, deployment, cost, and production readiness |
| Interviewer | Technical interview-style explanation and follow-up questions |

Chat history is preserved during the session, and the LLM receives the latest conversation turns for continuity.

### 3. Presentation Generator

The presentation generator converts the uploaded paper into practical presentation prep material.

It can generate:

- A two-minute research summary
- A five-minute research summary
- A slide-by-slide deck outline
- Speaker notes for each slide
- Key takeaways
- Ten likely viva questions

The slide outline supports a configurable slide count from 5 to 10 slides.

### 4. Mock Viva

The mock viva module creates realistic viva questions from the uploaded paper.

Capabilities:

- Choose an examiner persona
- Generate one paper-specific viva question
- Type an answer transcript
- Evaluate the answer using an academic scoring prompt
- Receive a score out of 10, strengths, weaknesses, and a better answer
- Review previous viva attempts in the current session

### 5. Presentation Practice Mode

The practice mode runs as a standalone Flask app and is linked from the Streamlit interface.

It records webcam and microphone input, then calculates:

- Eye contact rate
- Face detection rate
- Confidence score
- Engagement score
- Filler word usage
- Speech transcript
- Strengths
- Areas for improvement

Video analysis uses OpenCV and MediaPipe Face Mesh. Speech analysis uses SoundDevice for recording and Faster Whisper for transcription.

### 6. Voice Mock Viva

The voice viva app is a second Flask surface for spoken viva practice.

It can:

- Generate a viva question from `paper_context.json`
- Record a spoken answer
- Transcribe the answer
- Count filler words
- Calculate speaking fluency and words per minute
- Evaluate the answer with the LLM

This server is separate from the main Streamlit app and runs on port `5001`.

### 7. Final Performance Report

The final report brings together research, viva, and presentation metrics.

It includes:

- Research understanding score
- Viva score
- Presentation score
- Communication score
- Overall readiness score
- Readiness label
- Radar chart across Research, Viva, Presentation, and Communication
- Progress breakdown for each major category

The report reads presentation metrics from `results.json`, which is produced by the practice mode server.

---

## Tech Stack

| Layer | Tools |
| --- | --- |
| Main UI | Streamlit |
| Practice UIs | Flask, HTML, CSS, JavaScript |
| LLM | Groq API, `llama-3.1-8b-instant` |
| RAG | LangChain, FAISS, Hugging Face embeddings |
| PDF Processing | PyMuPDF |
| Embeddings | Sentence Transformers |
| Speech | SoundDevice, Faster Whisper, SciPy |
| Vision | OpenCV, MediaPipe |
| Charts | Plotly |
| Utilities | python-dotenv, NumPy |

---

## Project Structure

```text
ResearchPresentationTrainer/
|-- app.py                         # Main Streamlit application
|-- requirements.txt               # Python dependencies
|-- README.md                      # Project documentation
|-- agents/                        # Persona wrappers
|-- llm/                           # Groq client, prompt templates, response generation
|-- rag/                           # PDF loading, splitting, embeddings, FAISS retrieval
|-- modules/                       # Streamlit feature modules
|   |-- presentation_generator.py
|   |-- mock_viva.py
|   |-- final_report.py
|   `-- viva_audio.py
|-- practice_mode/                 # Flask presentation practice server
|   |-- pracapp.py
|   |-- video_analyzer.py
|   |-- speech_analyzer.py
|   |-- metrics.py
|   `-- templates/
|-- voice_viva/                    # Flask voice viva server
|   |-- vivapp.py
|   |-- viva_speech_analyzer.py
|   `-- templates/
|-- static/                        # Logo and static assets
|-- utils/                         # Session and memory helpers
`-- data/                          # Runtime uploads/results folders
```

---

## How It Works

```text
PDF Upload
   |
   v
PyMuPDF text extraction
   |
   v
Recursive text chunking
   |
   v
Sentence-transformer embeddings
   |
   v
FAISS vector store
   |
   v
Top-k semantic retrieval
   |
   v
Persona-aware Groq response
   |
   v
Streamlit chat, presentation tools, viva, and report
```

Presentation practice flow:

```text
Start Practice
   |
   +--> Webcam capture -> MediaPipe Face Mesh -> eye contact / face visibility
   |
   +--> Microphone recording -> Faster Whisper -> transcript / fillers / fluency
   |
   v
Metric calculation
   |
   v
results.json
   |
   v
Streamlit practice summary and final report
```

---

## Setup

### Prerequisites

- Python 3.10 recommended
- Webcam and microphone for practice features
- Groq API key

### 1. Create and activate a virtual environment

```bash
python -m venv venv310
```

On Windows PowerShell:

```powershell
.\venv310\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source venv310/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## Running the App

### Main Streamlit app

```bash
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal, upload a PDF, and use the tabs inside the app.

### Presentation practice server

Run this in a second terminal:

```bash
python practice_mode/pracapp.py
```

Then open:

```text
http://127.0.0.1:5000
```

The Streamlit app also includes a button that links to this address from the Practice Mode tab.

### Voice viva server

Run this in another terminal after a paper has been uploaded in the main app:

```bash
python voice_viva/vivapp.py
```

Then open:

```text
http://127.0.0.1:5001
```

Voice viva reads `paper_context.json`, which is created when the main app processes an uploaded paper.

---

## Runtime Files

The app may create or update these local files while running:

| File | Purpose |
| --- | --- |
| `paper_context.json` | Stores the latest uploaded paper name and extracted text |
| `results.json` | Stores the latest presentation practice metrics |
| `practice_audio.wav` | Temporary microphone recording for speech analysis |
| `data/uploads/` | Local uploaded documents, if used |

These files are runtime artifacts and do not need to be committed.

---

## Main Modules

| Module | Responsibility |
| --- | --- |
| `app.py` | Main Streamlit shell, sidebar, PDF processing, tabs, and practice summary |
| `rag/pdf_loader.py` | Extracts text from uploaded PDFs |
| `rag/text_splitter.py` | Splits extracted text into overlapping chunks |
| `rag/embeddings.py` | Loads Hugging Face embedding model |
| `rag/vector_store.py` | Builds FAISS vector store with source metadata |
| `rag/retriever.py` | Retrieves top matching chunks for a query |
| `llm/client.py` | Wraps Groq chat completion calls |
| `llm/prompt_templates.py` | Defines personas and RAG grounding rules |
| `modules/presentation_generator.py` | Generates summaries, outlines, takeaways, and viva questions |
| `modules/mock_viva.py` | Generates and evaluates typed viva attempts |
| `modules/final_report.py` | Combines viva and practice metrics into readiness report |
| `practice_mode/video_analyzer.py` | Tracks face visibility and eye contact |
| `practice_mode/speech_analyzer.py` | Records audio, transcribes speech, detects fillers |
| `practice_mode/metrics.py` | Calculates confidence, engagement, strengths, and improvements |
| `voice_viva/vivapp.py` | Runs the spoken viva Flask app |

---

## Current Limitations

- The FAISS index is in memory and resets when the Streamlit session restarts.
- The main app handles one active paper at a time.
- Camera and microphone permissions are required for practice modes.
- Faster Whisper runs on CPU by default, so first startup/transcription can take time.
- The spoken viva app depends on `paper_context.json` from the latest uploaded paper.
- The presentation practice server writes `results.json` relative to its running working directory.

---

## Roadmap Ideas

- Persistent multi-paper knowledge base
- Exportable presentation deck files
- Citation extraction and bibliography support
- In-app voice viva integration
- Session history persistence
- Practice recording export
- Deployment-ready configuration
- Better calibration controls for camera-based eye contact detection

---

## Author

Developed by Madhu.

Built to help students and researchers understand papers deeply, present them clearly, and defend them with confidence.
