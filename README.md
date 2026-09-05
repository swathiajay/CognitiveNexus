# 🧠 CognitiveNexus

## AI-Powered Knowledge & Productivity Assistant

CognitiveNexus is a Streamlit-based AI application designed to provide
context-aware assistance for research, study, analysis, content creation,
creative tasks, and general conversations.

The system combines Smart Prompt Engineering, Conversation Memory,
RAG-based PDF Knowledge Assistance, Source Support, Response Evaluation,
and Personalized Study Mode into one unified AI workspace.

---

## 🎯 Objectives

- Provide multiple AI assistance modes in one application.
- Automatically optimize prompts according to the user's task.
- Maintain conversation context during the active session.
- Allow users to ask questions from uploaded PDF documents.
- Provide source/page information for document-based answers.
- Evaluate generated responses using multiple quality criteria.
- Support personalized learning activities for students.

---

## ✨ Key Features

### 🧠 1. Conversation Memory

CognitiveNexus maintains conversation history during the active
Streamlit session so that follow-up questions can use previous context.

### 📄 2. RAG Knowledge Assistant

Users can upload a PDF and ask questions about its content.

The system:

1. Extracts text from the PDF.
2. Splits the text into smaller chunks.
3. Uses TF-IDF and cosine similarity to retrieve relevant chunks.
4. Provides the retrieved information as context to the AI model.

### ⚙️ 3. Task-Specific Prompt Optimization

CognitiveNexus detects the user's intended task and adapts the prompt.

Examples:

- Explanation
- Summary
- Quiz
- Flashcards
- Learning Plan
- Comparison
- Analysis
- Email
- Social Media Post
- Article
- Story
- Brainstorming

### 📌 4. Source Support

When a response uses information retrieved from an uploaded PDF,
CognitiveNexus displays the relevant PDF page number.

### 📊 5. Response Evaluation

Generated responses are evaluated using:

- Relevance
- Completeness
- Accuracy
- Hallucination Safety
- Overall Score

An evaluation summary is also provided.

### 🎓 6. Personalized Study Mode

Study Mode provides different learning tasks:

- Explanation
- Summary
- Quiz
- Flashcards
- Learning Plan

This allows students to use the application for different learning needs.

---

## 🤖 AI Modes

CognitiveNexus provides six main modes:

| Mode | Purpose |
|------|---------|
| Research | Structured research-oriented responses |
| Study | Learning and revision assistance |
| Analysis | Logical analysis and comparison |
| Content | Professional content generation |
| Creative | Stories and creative ideas |
| General Chat | General-purpose conversation |

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