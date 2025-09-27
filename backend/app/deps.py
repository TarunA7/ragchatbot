# deps.py - environment and simple validation
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "rag-chat-index")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in .env")
if not PINECONE_API_KEY:
    raise RuntimeError("PINECONE_API_KEY not set in .env")
if not PINECONE_ENVIRONMENT:
    raise RuntimeError("PINECONE_ENVIRONMENT not set in .env")
