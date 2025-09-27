# rag.py - ingestion, Pinecone init, and conversational chain helper
import os
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import TextLoader
import pinecone
from deps import OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

def get_embeddings():
    """Return LangChain OpenAI embeddings object."""
    return OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def create_index_if_missing(vector_dim: int = 1536):
    """Create Pinecone index if it does not exist."""
    existing = pinecone.list_indexes()
    if PINECONE_INDEX_NAME not in existing:
        pinecone.create_index(name=PINECONE_INDEX_NAME, dimension=vector_dim)
    return PINECONE_INDEX_NAME

def ingest_texts(texts: List[str], metadatas: Optional[List[dict]] = None):
    """Split texts into chunks, create embeddings, upsert into Pinecone index."""
    embeddings = get_embeddings()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = []
    metas = []

    for i, t in enumerate(texts):
        parts = splitter.split_text(t)
        for j, p in enumerate(parts):
            chunks.append(p)
            meta = {"source_doc": f"doc_{i}", "chunk": j}
            if metadatas and i < len(metadatas):
                meta.update(metadatas[i])
            metas.append(meta)

    if not chunks:
        return {"status": "no_chunks", "uploaded": 0}

    create_index_if_missing()
    # Upsert using LangChain helper
    Pinecone.from_texts(chunks, embeddings, metadatas=metas, index_name=PINECONE_INDEX_NAME)
    return {"status": "ok", "uploaded": len(chunks)}

def ingest_file_text(file_path: str):
    """Simple loader for plain text files using LangChain TextLoader."""
    loader = TextLoader(file_path, encoding="utf-8")
    docs = loader.load()
    texts = [d.page_content for d in docs]
    return ingest_texts(texts, metadatas=[{"filename": os.path.basename(file_path)}])

def get_conversational_chain():
    """Return a LangChain ConversationalRetrievalChain connected to Pinecone."""
    embeddings = get_embeddings()
    vector_store = Pinecone.from_existing_index(index_name=PINECONE_INDEX_NAME, embedding=embeddings)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    # Model: adjust model_name if not available for your key
    llm = ChatOpenAI(temperature=0.0, model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
    chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, return_source_documents=True)
    return chain
