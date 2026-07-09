# 🤖 Universal Human Values (UHV) AI Tutor Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://universal-human-values-ai-tutor.streamlit.app/)

### 📖 What is this project?

This project is an **AI Study Buddy and Tutor** for college students taking the **"Universal Human Values" (UHV)** course. 

Instead of reading through long, dry PDF syllabus guides, you can use this dashboard to learn and study interactively:
* 💬 **Ask Questions**: Type any question (e.g. *"What is Sukh and Suvidha?"* or *"Explain harmony in the family"*). The AI searches the official syllabus PDF in the background and writes a clear, easy-to-understand answer.
* ✍️ **Take Quizzes**: Practice with 3-question multiple choice quizzes generated on the fly, get scored, and read encouraging explanations from your AI tutor.
* 📚 **Browse the Syllabus**: View objectives, units, and learning outcomes for all 5 semesters in a clean curriculum navigator.
* 📂 **Upload Your Own PDF**: Drag and drop your own study guides, lecture slides, or notebooks. The AI will instantly read them and start answering questions based on your files!

---

## 🌟 Key Features

1. **💬 Study Chatbot**:
   - Streams empathetic, educational explanations using the **Groq API** (`llama-3.1-8b-instant`).
   - Retrieves course context using **FAISS** local vector search from the official syllabus.
   - Automatically saves and restores conversation history (MongoDB backed with local session fallbacks).

2. **📚 Curriculum Navigator**:
   - Tab-based syllabus browser showing objectives, learning outcomes, and units for all 5 core minor courses (Semesters III - VII).
   - **Click-to-Query cards**: Pre-populated course-specific starter questions that can be queried with a single click.

3. **✍️ Practice Quiz Mode**:
   - Dynamically generates challenging 3-question multiple-choice quizzes based on selected course units.
   - Outputs interactive radio selectors and provides grading scores instantly.
   - Generates customized academic evaluation "report cards" explaining details of each answer.
   - Includes robust pre-compiled local quizzes in case the LLM API is offline.

4. **📂 Custom PDF Uploader**:
   - Upload any custom PDF study guide, textbook chapter, or slides in the sidebar.
   - Automatically parses, splits, and indexes the document into a separate custom FAISS store.
   - Switches the RAG context to focus answers exclusively on your uploaded material.

5. **🔍 Citations Drawer**:
   - Displays actual extracted text snippets and source page numbers under every chatbot response for study transparency.

6. **📥 Log Export**:
   - Download the entire chat log, including the corresponding verified syllabus citations, as a formatted Markdown file (`.md`).

---

## 📂 Repository Structure

```tree
Universal-Human-Values-AI-Tutor/
│
├── faiss_index/                            # Default FAISS vector database
│   ├── index.faiss                         # Embedded index representation
│   └── index.pkl                           # Pickle metadata for FAISS chunks
│
├── app.py                                  # Primary Streamlit Dashboard code (UI, RAG, Quiz, logic)
├── requirements.txt                        # Python dependencies
├── .env                                    # Local environment secrets configuration
├── .gitignore                              # Git untracked pattern matching
├── README.md                               # Project documentation (this file)
├── Syllabus-Universal-Human-Values (1).pdf # Default source course syllabus PDF
├── syllabus_text.txt                       # Text-extracted representation of the syllabus
├── evaluate_rag.py                         # DeepEval framework validation scripts
└── deployment_guide.md                     # Step-by-step cloud deployment instructions
```

---

## 🛠️ Local Installation & Run Guide

### Prerequisites
- Python 3.10, 3.11, or 3.12 (Python 3.11 recommended)
- A Groq API Key (Get a free key from the [Groq Console](https://console.groq.com/))
- (Optional) Local MongoDB instance running on port 27017

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Universal-Human-Values-AI-Tutor.git
   cd Universal-Human-Values-AI-Tutor
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment variables**:
   Create a `.env` file in the root directory and add your credentials:
   ```env
   GROQ_API_KEY="your-groq-api-key-here"
   MONGO_URI="mongodb://localhost:27017/" # defaults to local mongo, falls back to local memory if offline
   ```

4. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```
   The dashboard will boot up and be accessible locally at: **http://localhost:8501**

---

## 🚀 Cloud Deployment

The application is structured to easily deploy on free tiers of **Streamlit Community Cloud** or **Hugging Face Spaces**. Refer to the [deployment_guide.md](file:///c:/Users/faish/Downloads/Universal-Human-Values-AI-Tutor/deployment_guide.md) file for step-by-step instructions.

---

## 🧠 Technology Specifications
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense vectors)
- **Vector Search Engine**: `faiss-cpu` (Facebook AI Similarity Search)
- **Text Splitter**: LangChain's `RecursiveCharacterTextSplitter` (chunk size: 700, overlap: 120)
- **Chat LLM**: Llama 3.1 8B Instant (`llama-3.1-8b-instant`)
- **Memory Adapter**: `langchain-mongodb` (MongoDBChatMessageHistory)
