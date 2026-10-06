"""Query expansion using a small domain synonym map.

A hosted LLM could generate richer paraphrases here, but for a tool library the
vocabulary is small and stable, so a curated map is predictable and fast.
"""

from __future__ import annotations

from typing import List

from app.retrieval.tokenize import content_terms

_SYNONYMS = {
    "drill": ["cordless", "battery", "power-tool"],
    "battery": ["charge", "charger", "lithium"],
    "ladder": ["rungs", "step", "climb", "safety"],
    "canning": ["jars", "canner", "water-bath", "kitchen"],
    "sewing": ["bobbin", "needle", "thread", "machine"],
    "fee": ["fees", "charge", "cost", "late"],
    "late": ["overdue", "fee", "due"],
    "hold": ["holds", "waitlist", "reserve"],
    "lost": ["missing", "replacement", "damage"],
    "damaged": ["damage", "repair", "broken"],
    "hours": ["open", "closed", "schedule"],
    "parking": ["lot", "street", "permit"],
    "renew": ["renewal", "extend", "loan"],
    "member": ["membership", "join", "resident"],
}


def expand_query(query: str, max_variants: int = 3) -> List[str]:
    terms = content_terms(query)
    variants: List[str] = [query]
    extras: List[str] = []
    for term in terms:
        for syn in _SYNONYMS.get(term, []):
            if syn not in extras:
                extras.append(syn)
    for syn in extras[: max_variants - 1]:
        variants.append(f"{query} {syn}")
    return variants
