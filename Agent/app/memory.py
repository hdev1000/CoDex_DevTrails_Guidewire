import chromadb


class EpisodicMemory:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="debate_history"
        )

    def _conflict_signature(self, decisions: list) -> str:
        """
        Create a deterministic fingerprint for a set of decisions.
        Order-independent to ensure consistent recall.
        """
        return " | ".join(sorted(decisions))

    def store(self, decisions: list, resolution: str):
        """
        Store the resolution of a resolved conflict.
        Overwrites previous resolution for the same signature.
        """
        signature = self._conflict_signature(decisions)

        self.collection.add(
            documents=[resolution],
            metadatas=[{"signature": signature}],
            ids=[signature]
        )

    def recall(self, decisions: list) -> dict:
        """
        Recall a past resolution if this conflict has been seen before.
        Safe against empty database and empty query results.
        """
        signature = self._conflict_signature(decisions)

        results = self.collection.query(
            query_texts=[signature],
            n_results=1
        )

        docs = results.get("documents", [])

        if docs and docs[0]:
            return {
                "seen_before": True,
                "past_resolution": docs[0][0]
            }

        return {"seen_before": False}
