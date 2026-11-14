"""Gemini Embedding Adapter using standard library HTTP client."""
import json
import os
import time
import urllib.request
import urllib.error
from typing import Protocol


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text, in the same order."""
        ...

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with the stored document vectors."""
        ...


class MyEmbedder:
    """Real embedder connecting to Gemini text-embedding-004."""

    def __init__(self, model_name: str = "text-embedding-004") -> None:
        self.model_name = model_name
        self.dimensions = 768
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is missing from environment variables (.env).")
        self.endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model_name}:batchEmbedContents?key={self.api_key}"
        )

    def _call_batch_api(self, texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
        requests = []
        for text in texts:
            requests.append({
                "model": f"models/{self.model_name}",
                "content": {"parts": [{"text": text[:8000]}]},
                "taskType": task_type
            })

        payload = json.dumps({"requests": requests}).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=payload,
            headers={"Content-Type": "application/json"}
        )

        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = json.loads(response.read().decode("utf-8"))
                    return [item["values"] for item in data["embeddings"]]
            except urllib.error.HTTPError as e:
                err_msg = e.read().decode("utf-8", errors="ignore")
                if e.code in (429, 500, 503) and attempt < 4:
                    sleep_time = 2 ** attempt
                    print(f"Gemini API rate limit/error {e.code}. Retrying in {sleep_time}s...")
                    time.sleep(sleep_time)
                else:
                    raise RuntimeError(f"Gemini API error {e.code}: {err_msg}")
            except Exception as e:
                if attempt < 4:
                    time.sleep(2)
                else:
                    raise e
        raise RuntimeError("Failed after 5 retries to embed contents.")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed document texts in batches of 50."""
        batch_size = 50
        all_embeddings: list[list[float]] = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            emb = self._call_batch_api(batch, task_type="RETRIEVAL_DOCUMENT")
            all_embeddings.extend(emb)
            time.sleep(0.5)  # Tránh vượt rate limit
        return all_embeddings

    def embed_query(self, question: str) -> list[float]:
        """Embed single search query with RETRIEVAL_QUERY task type."""
        emb = self._call_batch_api([question], task_type="RETRIEVAL_QUERY")
        return emb[0]
