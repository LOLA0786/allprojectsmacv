from backend.memory.chroma_client import collection

async def process_event(event_dict):
    doc_id = event_dict["id"]
    content = event_dict["content"]
    metadata = event_dict.get("metadata", {})

    collection.add(
        ids=[doc_id],
        documents=[content],
        metadatas=[metadata]
    )
