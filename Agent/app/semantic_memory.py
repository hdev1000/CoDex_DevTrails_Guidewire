import chromadb

class SemanticMemory:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="semantic_sop_memory"
        )

    def store_sop(self, text: str, source: str):
        chunks = [text[i:i+800] for i in range(0, len(text), 800)]

        for idx, chunk in enumerate(chunks):
            self.collection.add(
                documents=[chunk],
                metadatas=[{
                    "type": "standard_procedure",
                    "source": source
                }],
                ids=[f"{source}_{idx}"]
            )
