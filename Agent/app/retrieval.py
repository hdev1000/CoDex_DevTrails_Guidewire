class SOPRetriever:
    def __init__(self, semantic_memory):
        self.collection = semantic_memory.collection

    def retrieve_procedures(self, query: str, k: int = 3) -> list[str]:
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            where={"type": "standard_procedure"}
        )

        documents = results.get("documents", [])
        if not documents:
            return []

        return documents[0]
