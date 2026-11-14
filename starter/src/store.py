"""PostgreSQL + pgvector vector store implementation."""
import json
from typing import Any
import psycopg
from psycopg.rows import dict_row

try:
    from .models import Chunk
except (ImportError, ValueError):
    from models import Chunk


class PgVectorStore:
    def __init__(self, database_url: str, dimensions: int = 768) -> None:
        self.database_url = database_url
        self.dimensions = dimensions

    def create_schema(self) -> None:
        """Create table and vector extension."""
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS document_chunks (
                        chunk_id VARCHAR(255) PRIMARY KEY,
                        strategy VARCHAR(50) NOT NULL,
                        document_id VARCHAR(100) NOT NULL,
                        source VARCHAR(255) NOT NULL,
                        page INT NOT NULL,
                        text TEXT NOT NULL,
                        metadata JSONB NOT NULL,
                        embedding vector({self.dimensions}) NOT NULL
                    );
                """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_strategy ON document_chunks (strategy);
                """)
                conn.commit()

    def upsert(self, strategy: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        """Upsert chunks with stable IDs; clear prior strategy chunks for idempotency."""
        if len(chunks) != len(vectors):
            raise ValueError(f"Length mismatch: {len(chunks)} chunks vs {len(vectors)} vectors.")

        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                # Xóa dữ liệu cũ của chiến lược này trước khi nạp lại để không bao giờ bị nhân đôi
                cur.execute("DELETE FROM document_chunks WHERE strategy = %s;", (strategy,))
                
                query = """
                    INSERT INTO document_chunks 
                    (chunk_id, strategy, document_id, source, page, text, metadata, embedding)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
                records = [
                    (
                        c.chunk_id,
                        strategy,
                        c.document_id,
                        c.source,
                        c.page,
                        c.text,
                        json.dumps(c.metadata),
                        v
                    )
                    for c, v in zip(chunks, vectors)
                ]
                cur.executemany(query, records)
                conn.commit()

    def search(
        self,
        strategy: str,
        query_vector: list[float],
        top_k: int = 3,
        filters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Search top-k chunks by cosine distance with optional SQL metadata filter."""
        conditions = ["strategy = %(strategy)s"]
        params: dict[str, Any] = {
            "strategy": strategy,
            "query_vec": query_vector,
            "top_k": top_k
        }

        # Áp dụng bộ lọc metadata qua SQL parameterized query
        if filters:
            for key, val in filters.items():
                param_key = f"filter_{key}"
                conditions.append(f"metadata->>'{key}' = %({param_key})s")
                params[param_key] = str(val)

        where_clause = " AND ".join(conditions)
        sql = f"""
            SELECT 
                chunk_id,
                document_id,
                source,
                page,
                text,
                metadata,
                1 - (embedding <=> %(query_vec)s::vector) AS score
            FROM document_chunks
            WHERE {where_clause}
            ORDER BY embedding <=> %(query_vec)s::vector ASC
            LIMIT %(top_k)s;
        """

        with psycopg.connect(self.database_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchall()
