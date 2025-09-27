# 🧠 Conversational RAG Chatbot — LangChain, Pinecone, FastAPI

A **domain-specific Retrieval-Augmented Generation (RAG) chatbot** built with:
- [LangChain](https://www.langchain.com/)
- [Pinecone](https://www.pinecone.io/) (vector database)
- [OpenAI](https://platform.openai.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/) (optional for deployment)

This chatbot ingests your documents, indexes them into Pinecone, and answers questions with context-aware responses using LLMs.

---

## 🚀 Features
- Document ingestion (`ingest.py`) → text, PDFs, etc.
- Vector embeddings stored in **Pinecone**
- Query answering with **LangChain + OpenAI**
- API served via **FastAPI**
- Ready for local dev or Docker deployment

---

## 📂 Project Structure
backend/
│── app/
│ ├── main.py # FastAPI app entrypoint
│ ├── rag.py # Core RAG pipeline (retriever + LLM)
│ ├── ingest.py # Script to load and index docs
│ ├── deps.py # API key/env variable loader
│ └── requirements.txt # Python dependencies
│
│── .env # Environment variables (DO NOT COMMIT)
│── README.md # Project documentation

yaml
Copy code

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/your-username/rag-chatbot.git
cd rag-chatbot/backend
2. Create virtual environment
bash
Copy code
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
3. Install dependencies
bash
Copy code
pip install -r app/requirements.txt
4. Configure .env
Create a file backend/.env:

ini
Copy code
OPENAI_API_KEY=sk-your-openai-key
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=us-east1-gcp   # adjust to your region
PINECONE_INDEX_NAME=my-index
⚠️ Never commit .env to GitHub.

📥 Ingest Documents
To index documents into Pinecone:

bash
Copy code
python app/ingest.py
This loads your docs and populates the Pinecone vector store.

💬 Run Chatbot API
Start FastAPI:

bash
Copy code
uvicorn app.main:app --reload
Then open in browser:

arduino
Copy code
http://127.0.0.1:8000/docs
You can test endpoints with Swagger UI.

🐳 Run with Docker (optional)
Build and run:

bash
Copy code
docker build -t rag-chatbot .
docker run -p 8000:8000 rag-chatbot
🛠️ Tech Stack
FastAPI → API framework

LangChain → LLM + RAG orchestration

OpenAI → LLM + embeddings

Pinecone → Vector database

Docker → Containerized deployment

📝 Notes
If you see warnings like DeprecationWarning: Importing ... from langchain, replace imports with langchain_community.

Make sure you have created a Pinecone index with the same name as in .env.

🤝 Contributing
Pull requests are welcome. Please open issues to suggest improvements.

📜 License
MIT License

yaml
Copy code

---

I can also create a **ready-to-use `requirements.txt`** + updated **`rag.py` imports** so that if you copy everything, it will run locally without any LangChain module errors.  

Do you want me to do that next?






