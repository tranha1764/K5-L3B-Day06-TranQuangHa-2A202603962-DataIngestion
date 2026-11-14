"""OpenAI Embedding Adapter using standard library HTTP client."""
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
    """Real embedder connecting to OpenAI API (text-embedding-3-small)."""

    def __init__(self, model_name: str = "text-embedding-3-small", dimensions: int = 768) -> None:
        env_model = os.getenv("EMBEDDING_MODEL")
        self.model_name = env_model or model_name
        self.dimensions = dimensions
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is missing from environment variables (.env).")
        self.endpoint = "https://api.openai.com/v1/embeddings"

    def _call_batch_api(self, texts: list[str]) -> list[list[float]]:
        """Call OpenAI embeddings endpoint with dimensions parameter."""
        payload = json.dumps({
            "model": self.model_name,
            "input": [t[:8000] for t in texts],
            "dimensions": self.dimensions  # Chuẩn hóa về 768 chiều
        }).encode("utf-8")

        req = urllib.request.Request(
            self.endpoint,
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )

        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = json.loads(response.read().decode("utf-8"))
                    items = sorted(data["data"], key=lambda x: x["index"])
                    return [item["embedding"] for item in items]
            except urllib.error.HTTPError as e:
                err_msg = e.read().decode("utf-8", errors="ignore")
                if e.code in (429, 500, 502, 503) and attempt < 4:
                    sleep_time = 2 ** attempt
                    print(f"OpenAI API error {e.code}. Retrying in {sleep_time}s...")
                    time.sleep(sleep_time)
                else:
                    raise RuntimeError(f"OpenAI API error {e.code}: {err_msg}")
            except Exception as e:
                if attempt < 4:
                    time.sleep(2)
                else:
                    raise e
        raise RuntimeError("Failed after 5 retries to embed contents via OpenAI.")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed document texts in batches of 100."""
        batch_size = 100
        all_embeddings: list[list[float]] = []
        total = len(texts)

        for i in range(0, total, batch_size):
            batch = texts[i:i + batch_size]
            emb = self._call_batch_api(batch)
            all_embeddings.extend(emb)
            print(f"  -> Tiến độ embedding OpenAI: {len(all_embeddings)}/{total} chunks...")

        return all_embeddings

    def embed_query(self, question: str) -> list[float]:
        """Embed single search query."""
        emb = self._call_batch_api([question])
        return emb[0]
