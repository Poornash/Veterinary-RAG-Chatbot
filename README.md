🐾 PawMedBot – Offline Veterinary AI Assistant (RAG-based)

PawMedBot is an AI-powered veterinary assistant built using Retrieval-Augmented Generation (RAG).
It works offline using a local LLM (via Ollama) and provides reliable, document-grounded answers related to pet health, diseases, care, and veterinary guidance.

This project is developed as part of an AI/ML academic project and is optimized for CPU-only systems, with optional GPU acceleration if available.
🚀 Features

🐶 Veterinary Q&A (dogs, cats, birds, rabbits, etc.)
📚 RAG-based answers using uploaded veterinary books & documents
🧠 Local LLM inference (offline support)
⚡ Fast non-pet query rejection
🗂️ Chat history & user authentication
🖥️ Clean Streamlit-based UI
🔒 No external API dependency (privacy-friendly)

🛠️ Tech Stack

Python 3.11
Streamlit – Frontend
LangChain – RAG pipeline
ChromaDB – Vector database
HuggingFace Embeddings – Text embeddings
Ollama – Local LLM runtime
SQLite – User & chat history storage

📂 Project Structure

RAGBOT/
├── app.py
├── backend/
│   ├── rag.py
│   ├── preprocessor.py
│   ├── auth.py
│   ├── db.py
│   └── __init__.py
├── pages/
│   ├── 1_login.py
│   ├── 2_signup.py
│   ├── 3_profile.py
│   ├── 4_chat.py
│   └── 5_history.py
├── data/
│   ├── veterinary_books.pdf
│   ├── clinics.csv
├── requirements.txt
├── README.md
└── .gitignore

🧩 Prerequisites
1️⃣ Python (MANDATORY)

Install Python 3.11.x

🔗 Download:
https://www.python.org/downloads/

✔ During installation:

Check “Add Python to PATH”

Verify:
```bash
python --version
```

2️⃣ Ollama (Local LLM Runtime)

Install Ollama for your OS:

🔗 https://ollama.com/download

Verify installation:
```bash
ollama --version
```
ollama --version

3️⃣ Download Required LLM Model
We use Phi-3 Mini (fast + lightweight).
```bash
ollama pull phi3:mini
```
option if LARGER MODEL WORKS
```bash
ollama pull llama3:instruct
```
📦 Project Setup Instructions
1️⃣ Clone the Repository
```basg=h
git clone https://github.com/<your-username>/PawMedBot.git
cd PawMedBot
```

2️⃣ Create a Virtual Environment (Recommended)
```bash
python -m venv venv
```
Activate it:
Windows
```
venv\Scripts\activate
```
Mac/Linux
```
source venv/bin/activate
```

3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

If pip gives errors, upgrade it:
```
python -m pip install --upgrade pip
```

📚 Build the Vector Database (IMPORTANT)

This step converts the documents in /data into embeddings.
```
python backend/preprocessor.py
```
✔ This will:
Chunk documents
Generate embeddings
Create vectorstore/ folder automatically
⏱️ Takes time depending on system performance (normal).
▶️ Run the Application
```
python -m streamlit run app.py
```
Then open the browser at:
http://localhost:8501

👤 First-Time Usage Flow
Open app
Signup with email & password
Login
Go to Chat
Ask veterinary-related questions
View history & profile anytime

🧠 How the AI Works (High-Level)

Retrieval:
Relevant document chunks are fetched from ChromaDB

Augmentation:
Retrieved context is injected into a prompt

Generation:
Local LLM (Phi-3 Mini) generates an answer grounded in documents

⚡ Performance Notes
CPU-only systems may take 20–40 seconds per response
GPU-enabled systems will be significantly faster
Non-pet queries are rejected instantly (rule-based filter)

❌ Common Issues & Fixes
❗ Ollama model not found
```
ollama list
```
If missing:
```
ollama pull phi3:mini
```
❗ Vectorstore missing error
Run:
```
python backend/preprocessor.py
```
❗ Streamlit not found
```
pip install streamlit
```
👤 First-Time Usage Flow

Open app

Signup with email & password

Login

Go to Chat

Ask veterinary-related questions

View history & profile anytime

🧠 How the AI Works (High-Level)

Retrieval:
Relevant document chunks are fetched from ChromaDB

Augmentation:
Retrieved context is injected into a prompt

Generation:
Local LLM (Phi-3 Mini) generates an answer grounded in documents

⚡ Performance Notes

CPU-only systems may take 20–40 seconds per response

GPU-enabled systems will be significantly faster

Non-pet queries are rejected instantly (rule-based filter)

❌ Common Issues & Fixes
❗ Ollama model not found
ollama list


If missing:

ollama pull phi3:mini

❗ Vectorstore missing error

Run:

python backend/preprocessor.py

❗ Streamlit not found
pip install streamlit


This project falls under:

Artificial Intelligence & Machine Learning (AIML)
specifically Natural Language Processing (NLP) and Information Retrieval (IR).

❤️ Final Note

If the project runs on one system, it will run identically on another if these steps are followed correctly.

Happy building 🐾✨


