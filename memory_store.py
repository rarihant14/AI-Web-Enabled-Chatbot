import os
import chromadb
from datetime import datetime

DB_PATH = "chroma_memory"

# docs 
class MemoryStore:
    def __init__(self, user_id="default_user"):
        self.user_id = user_id
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_or_create_collection(name=f"chat_{self.user_id}")

    def add_message(self, role: str, content: str):
        _id = f"{datetime.now().timestamp()}_{role}"
        self.collection.add(
            ids=[_id],
            documents=[content],
            metadatas=[{"role": role, "time": str(datetime.now())}]
        )

    def get_recent_memory(self, limit: int = 8):
        results = self.collection.get(limit=limit)
        docs = results.get("documents", [])
        metas = results.get("metadatas", [])
        history = []

        for doc, meta in zip(docs, metas):
            history.append(f"{meta.get('role','user')}: {doc}")

        return "\n".join(history[-limit:]) if history else "No previous memory yet."

    def clear(self):
        self.client.delete_collection(name=f"chat_{self.user_id}")
