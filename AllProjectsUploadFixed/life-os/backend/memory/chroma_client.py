import chromadb
import os

persist_dir = os.path.join(os.getcwd(), ".chromadb")

# NEW Chroma client (2025 API)
client = chromadb.PersistentClient(path=persist_dir)

collection = client.get_or_create_collection(
    name="life_events",
    metadata={"hnsw:space": "cosine"}
)
