"""
Contract tests — fail against the starter stubs; make them pass.

These run OFFLINE: no ANTHROPIC_API_KEY, no network. They exercise only the
deterministic retrieval logic (chunk, score, retrieve, build_prompt) — never
`answer`, which is the only function that calls the real API.
"""
from rag import chunk, score, retrieve, build_prompt


def test_chunk_respects_size_and_overlap():
    # 10 words, size 4, overlap 1 -> step 3 -> starts at 0,3,6,9.
    words = [f"w{i}" for i in range(10)]
    text = " ".join(words)
    chunks = chunk(text, size=4, overlap=1)

    # No chunk exceeds `size` words.
    assert all(len(c.split()) <= 4 for c in chunks)
    # Every original word is covered (nothing dropped).
    covered = " ".join(chunks).split()
    assert set(covered) == set(words)
    # Consecutive chunks overlap by `overlap` words: last word of one chunk
    # reappears as the first word of the next.
    first, second = chunks[0].split(), chunks[1].split()
    assert first[-1:] == second[:1]


def test_retrieve_returns_top_k_in_descending_score_order():
    # Query has two distinct terms ("python" and "testing"); the best chunk
    # contains both, the next contains one, the last contains neither — so the
    # ranking is unambiguous for any sensible term-overlap or embedding scorer.
    chunks = [
        {"doc": "a.md", "text": "python is a programming language"},      # 1 term: python
        {"doc": "b.md", "text": "the weather today is cold and grey"},    # 0 terms
        {"doc": "c.md", "text": "python testing with pytest is great"},   # 2 terms
    ]
    top = retrieve("python testing", chunks, k=2)

    assert len(top) == 2                                   # returns exactly k
    scores = [score("python testing", c["text"]) for c in top]
    assert scores == sorted(scores, reverse=True)          # descending order
    assert top[0]["doc"] == "c.md"                         # best (both terms) first
    assert top[1]["doc"] == "a.md"                         # next-best (one term)
    assert "b.md" not in [c["doc"] for c in top]           # irrelevant dropped


def test_build_prompt_includes_contexts_and_question():
    contexts = [
        {"doc": "02-pricing-and-plans.md", "text": "Pro is $8 per user per month."},
        {"doc": "03-sync-and-offline.md", "text": "Sync usually completes in seconds."},
    ]
    question = "How much does the Pro plan cost?"
    prompt = build_prompt(question, contexts)

    # The question and every context's text must appear in the prompt.
    assert question in prompt
    for c in contexts:
        assert c["text"] in prompt
    # Sources should be identifiable for citation.
    assert "02-pricing-and-plans.md" in prompt
