# ingest.py - simple script to ingest .txt files from ../data/
import os
from rag import ingest_texts

BASE = os.path.join(os.path.dirname(__file__), "..", "..", "data")
BASE = os.path.abspath(BASE)

def ingest_all():
    texts = []
    metas = []
    if not os.path.exists(BASE):
        print("data/ folder not found. Create data/ and place .txt files.")
        return

    for fname in os.listdir(BASE):
        path = os.path.join(BASE, fname)
        if os.path.isfile(path) and fname.lower().endswith((".txt", ".md")):
            with open(path, "r", encoding="utf-8") as f:
                texts.append(f.read())
            metas.append({"filename": fname})

    if not texts:
        print("No .txt files found in data/. Add files and run again.")
        return

    print(f"Ingesting {len(texts)} files...")
    res = ingest_texts(texts, metadatas=metas)
    print(res)

if __name__ == "__main__":
    ingest_all()
