# 🔬 AI Research Arena

A Retrieval-Augmented Generation (RAG) system that enables intelligent question answering over research papers using multiple AI personas and explainable citations.

---

## 🚀 Overview

AI Research Arena is a document intelligence system that allows users to upload research papers (PDFs) and interact with them using a conversational AI assistant.

The system retrieves relevant sections from the document and generates grounded answers using a Large Language Model (LLM), ensuring responses are strictly based on the provided context.

---

## 🧠 Key Features

- 📄 PDF-based question answering
- 🔎 Semantic search using FAISS vector database
- 🧩 Chunk-based document understanding
- 🤖 LLM-powered response generation (Groq / HuggingFace compatible)
- 🎭 Multi-persona AI system:
  - Professor (academic analysis)
  - Student (simple explanations)
  - Skeptic (critical review)
  - Industry Expert (real-world perspective)
  - Interviewer (technical questioning style)
- 📚 Citation-based answers with source tracking
- 💬 Chat-based interactive UI using Streamlit

---

## 🏗️ System Architecture

1. PDF Upload  
2. Text Extraction  
3. Chunking  
4. Embedding Generation  
5. FAISS Vector Store Creation  
6. Semantic Retrieval (Top-K chunks)  
7. LLM-based Answer Generation  
8. Persona-based Response Formatting  
9. Citation + Source Display  

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- FAISS
- Hugging Face / Groq LLMs
- Sentence Transformers

---

## 📂 Project Structure
ai-research-arena/
│
├── app.py
├── rag/
│ ├── pdf_loader.py
│ ├── text_splitter.py
│ ├── vector_store.py
│ ├── retriever.py
│ ├── embeddings.py
│
├── llm/
│ ├── client.py
│ ├── response_generator.py
│ ├── prompt_templates.py
│
├── utils/
│ ├── memory.py
│
├── requirements.txt
└── README.md  


---

## 💡 Example Use Cases

- Understanding research papers faster
- Interview preparation using technical papers
- Academic summarization
- AI-powered study assistant
- Research exploration tool

---

## ⚠️ Limitations

- Performance depends on quality of embeddings and chunking
- May struggle with highly scanned PDFs
- Not a replacement for full human research understanding

---

## 🔮 Future Improvements

- Multi-paper comparison
- Better retrieval ranking (reranking models)
- Highlight-based citations in UI
- Cloud deployment
- Fine-tuned domain-specific embeddings

---

## 📸 UI Preview

(Add screenshots here)

---

## 🧑‍💻 Author

Built as a learning + portfolio project exploring:
- RAG systems
- LLM orchestration
- Document intelligence
- AI product design

---

## 📌 Status

🚧 Work in progress — actively improving retrieval quality and UI experience.