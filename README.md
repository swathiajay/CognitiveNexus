# 🧠 CognitiveNexus

## 📌 Project Overview

CognitiveNexus is an AI-powered knowledge and productivity assistant built using Python and Streamlit.

The system adapts its prompts according to the user's task, maintains conversational context, retrieves relevant information from uploaded PDF documents, and evaluates generated responses.

---

## 🎯 Objectives

- Provide a multi-purpose AI assistant for different user tasks.
- Implement Smart Prompt Engineering.
- Support task-specific AI responses.
- Provide PDF-based knowledge retrieval using RAG.
- Maintain conversation context during an active session.
- Provide response evaluation.
- Provide personalized study assistance.

---

## ✨ Key Features

### 1. Smart Prompt Engineering

- Detects the user's task.
- Selects an appropriate AI mode.
- Optimizes the prompt according to the task.
- Creates a structured prompt before sending it to the AI model.

### 2. Six AI Modes

- 🔎 Research
- 📚 Study
- 📊 Analysis
- ✍️ Content
- 🎨 Creative
- 💬 General Chat

### 3. Personalized Study Mode

Study Mode supports:

- Auto Detect
- Explanation
- Summary
- Quiz
- Flashcards
- Learning Plan

### 4. RAG Knowledge Assistant

- Upload PDF documents.
- Extract text from PDFs.
- Divide documents into smaller chunks.
- Retrieve relevant chunks using TF-IDF and cosine similarity.
- Use retrieved content as context for AI responses.
- Display source/page information when available.

### 5. Conversation Memory

- Maintains previous messages during the active Streamlit session.
- Uses conversation history as context for subsequent questions.

### 6. Response Evaluation

Generated responses are evaluated using:

- Relevance
- Completeness
- Accuracy
- Hallucination Risk
- Overall Score

### 7. Source Support

When PDF retrieval is used, the application provides retrieved source/page information where available.

### 8. Task-Specific Prompt Optimization

Different tasks receive different prompt structures so that the AI response can be adapted to the user's selected task.

---

## 🤖 AI Modes

| Mode | Purpose |
|---|---|
| Research | Information research and explanation |
| Study | Learning and educational assistance |
| Analysis | Analysis, comparison, advantages and disadvantages |
| Content | Content creation and writing assistance |
| Creative | Creative ideas and responses |
| General Chat | General-purpose conversation |

---

## 📚 Personalized Study Mode

The Study Mode provides different learning options:

| Study Option | Purpose |
|---|---|
| Auto Detect | Automatically identifies the study task |
| Explanation | Explains a topic clearly |
| Summary | Provides concise summaries |
| Quiz | Generates practice questions |
| Flashcards | Creates question-and-answer flashcards |
| Learning Plan | Creates a structured learning plan |

---

## 🧩 Smart Prompt Engineering

CognitiveNexus uses a Smart Prompt Engineering layer to improve task-specific responses.

The process includes:

1. User Input
2. Mode Selection
3. Task Detection
4. Prompt Optimization
5. Structured Prompt Creation
6. AI Model Inference
7. Response Processing

This allows the system to adapt the prompt structure according to the user's task.

---

## 📄 RAG Knowledge Assistant

The RAG component allows users to ask questions based on uploaded PDF documents.

### RAG Pipeline

1. Upload PDF
2. Extract PDF text
3. Split text into chunks
4. Convert text into TF-IDF vectors
5. Calculate cosine similarity
6. Retrieve relevant chunks
7. Provide retrieved content as context
8. Generate the AI response
9. Display source/page information

The implementation uses PyPDF for PDF text extraction and Scikit-learn for TF-IDF and cosine similarity retrieval.

---

## 🧠 Conversation Memory

CognitiveNexus maintains conversation history using Streamlit session state.

This allows the assistant to use previous messages as context during the active session.

> Note: Conversation memory is session-based and is not permanent across separate sessions.

---

## 📑 Source Support

For PDF-based questions, CognitiveNexus retrieves relevant document chunks and provides source/page information where available.

This helps users understand which part of the uploaded document was used as supporting context.

---

## 📊 Response Evaluation

CognitiveNexus includes a response evaluation component.

Each generated response can be evaluated using:

- **Relevance**
- **Completeness**
- **Accuracy**
- **Hallucination Risk**
- **Overall Score**

The evaluation provides an additional assessment of the generated response.

> Evaluation scores are model-generated estimates and should not be treated as guaranteed ground truth.

---

## 🏗️ System Architecture

```text
User Input
    ↓
Mode Selection
    ↓
Task Detection
    ↓
Smart Prompt Optimization
    ↓
Conversation Memory
    ↓
PDF Retrieval (when available)
    ↓
Structured Prompt
    ↓
Hugging Face Inference API
    ↓
AI Response
    ↓
Source Support
    ↓
Response Evaluation
    ↓
Final Output
```

## 📸 Screenshots