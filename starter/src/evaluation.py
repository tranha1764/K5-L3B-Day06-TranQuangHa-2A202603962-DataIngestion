"""Evaluate retrieved evidence and preserve per-query traces."""
from typing import Any
import unicodedata
import re


def _normalize_for_match(text: str) -> str:
    """Normalize text for evidence comparison."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text).lower()
    return re.sub(r'\s+', ' ', text).strip()


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Check source/page and enough gold evidence; keep hit@1 and hit@3 trace.
    A hit requires: chunk belongs to gold_page AND contains evidence_quote.
    """
    gold_page = question["gold_page"]
    evidence = _normalize_for_match(question.get("evidence_quote", ""))
    filter_req = question.get("filter")

    hit_at_1 = False
    hit_at_3 = False
    filter_compliant = True

    analyzed_hits = []
    for rank, h in enumerate(hits, start=1):
        chunk_text = _normalize_for_match(h.get("text", ""))
        is_page_match = (h.get("page") == gold_page)

        # Kiểm tra sự xuất hiện của bằng chứng trong chunk
        is_evidence_match = False
        if evidence:
            if evidence in chunk_text:
                is_evidence_match = True
            elif len(evidence) > 35 and evidence[:35] in chunk_text:
                is_evidence_match = True

        is_hit = is_page_match and is_evidence_match

        if rank == 1 and is_hit:
            hit_at_1 = True
        if is_hit:
            hit_at_3 = True

        # Kiểm tra tuân thủ filter nếu câu hỏi có filter
        if filter_req:
            for k, v in filter_req.items():
                if h.get("metadata", {}).get(k) != v:
                    filter_compliant = False

        analyzed_hits.append({
            "rank": rank,
            "chunk_id": h.get("chunk_id"),
            "page": h.get("page"),
            "score": round(float(h.get("score", 0)), 4),
            "text": h.get("text"),
            "metadata": h.get("metadata", {}),
            "is_gold_page": is_page_match,
            "is_evidence_hit": is_hit
        })

    return {
        "query_id": question["id"],
        "split": question["split"],
        "type": question.get("type", "truc_tiep"),
        "question": question["question"],
        "expected_answer": question.get("expected_answer", ""),
        "gold_page": gold_page,
        "evidence_quote": question.get("evidence_quote", ""),
        "filter": filter_req,
        "filter_compliant": filter_compliant if filter_req else None,
        "hit_at_1": hit_at_1,
        "hit_at_3": hit_at_3,
        "hits": analyzed_hits
    }


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate Hit@1 and Evidence Hit@3 by strategy and dev/test split."""
    splits: dict[str, dict[str, Any]] = {}
    for t in traces:
        s = t["split"]
        if s not in splits:
            splits[s] = {"total": 0, "hit1": 0, "hit3": 0, "filter_total": 0, "filter_pass": 0}
        splits[s]["total"] += 1
        if t["hit_at_1"]:
            splits[s]["hit1"] += 1
        if t["hit_at_3"]:
            splits[s]["hit3"] += 1
        if t.get("filter") is not None:
            splits[s]["filter_total"] += 1
            if t.get("filter_compliant"):
                splits[s]["filter_pass"] += 1

    summary = {}
    for s, data in splits.items():
        summary[s] = {
            "count": data["total"],
            "hit1": f"{data['hit1']}/{data['total']}",
            "hit1_pct": round(data["hit1"] / data["total"] * 100, 1) if data["total"] else 0.0,
            "hit3": f"{data['hit3']}/{data['total']}",
            "hit3_pct": round(data["hit3"] / data["total"] * 100, 1) if data["total"] else 0.0,
            "filter_compliance": f"{data['filter_pass']}/{data['filter_total']}" if data["filter_total"] > 0 else "N/A"
        }
    return summary
