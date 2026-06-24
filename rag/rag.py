"""
RAG core for a document Q&A pipeline.

Split deliberately so the *retrieval logic* (chunk, score, retrieve, build_prompt)
is pure and unit-testable OFFLINE, while only `answer` touches the network. The 3
contract tests exercise the deterministic logic with NO API key set, so keep the
scorer deterministic and keep the LLM call isolated in `answer`.

Conventions used throughout:
  - A "chunk" is a dict {"doc": str, "text": str} — `doc` is the source document
    name (for citations), `text` is the chunk body.
  - `score(query, chunk_text)` returns a non-negative float; higher = more relevant.
    It must be deterministic (no randomness, no network) so retrieval is testable.
"""
from __future__ import annotations
import os


def chunk(text: str, size: int, overlap: int) -> list[str]:
    """Split `text` into overlapping chunks.

    TODO:
      - split into pieces of at most `size` units, where consecutive chunks
        overlap by `overlap` units (so an answer near a boundary is not cut in
        half). Word-based units are fine (text.split()).
      - the step between chunk starts is (size - overlap); require overlap < size.
      - every chunk has length <= size; the overlap between neighbours is `overlap`.
      - do not drop the tail: the final chunk may be shorter than `size`.
    Return a list of chunk strings, in document order.
    """
    raise NotImplementedError("Implement chunk")


def score(query: str, chunk_text: str) -> float:
    """Deterministic relevance score between a query and a chunk.

    TODO:
      - return a non-negative number; a higher score means more relevant.
      - a keyword/term-overlap score is enough for the contract (e.g. count the
        distinct query terms that appear in the chunk). For the stretch goal,
        swap this for an embedding cosine similarity.
      - MUST be deterministic and offline (no API call, no randomness) so the
        retrieval test is reproducible without a key.
    """
    raise NotImplementedError("Implement score")


def retrieve(query: str, chunks: list[dict], k: int) -> list[dict]:
    """Return the top-`k` chunks for `query`, most relevant first.

    TODO:
      - score each chunk in `chunks` with score(query, chunk["text"]).
      - sort by score DESCENDING and return the top k.
      - return at most k chunks (fewer if there are fewer than k).
    Each returned item is one of the input chunk dicts ({"doc", "text"}).
    """
    raise NotImplementedError("Implement retrieve")


def build_prompt(question: str, contexts: list[dict]) -> str:
    """Assemble the grounded prompt sent to the model.

    TODO:
      - include EVERY retrieved context's text in the prompt, each labelled with
        its source `doc` so the model can cite it.
      - include the `question` verbatim.
      - instruct the model to answer ONLY from the provided contexts and to cite
        the source doc(s); if the contexts don't contain the answer, say so
        rather than guessing.
    Return the full prompt string. (The 3rd contract test checks that the
    question text and each context's text both appear in the returned string.)
    """
    raise NotImplementedError("Implement build_prompt")


def answer(question: str, chunks: list[dict], k: int = 3) -> dict:
    """End-to-end: retrieve, build a grounded prompt, call the model, return it.

    This is the ONLY function that touches the network. Tests do NOT call it.

    TODO:
      - contexts = retrieve(question, chunks, k)
      - prompt = build_prompt(question, contexts)
      - read the key from os.environ["ANTHROPIC_API_KEY"] (never hardcode it).
      - call the Anthropic Messages API with a CURRENT model id:
        "claude-sonnet-4-6" (default) or "claude-haiku-4-5-20251001" (cheaper).
        NEVER a claude-3-* id.
      - return {"answer": <text>, "sources": [c["doc"] for c in contexts]}.
    """
    raise NotImplementedError("Implement answer")
