"""
Index the corpus and answer a question:

    python -m rag.cli "How much does the Pro plan cost?"

Loads every markdown doc under dataset/docs/, chunks them into an in-memory
index, then runs the RAG pipeline. Needs ANTHROPIC_API_KEY set for the final
`answer` call (chunk/score/retrieve/build_prompt run without a key).
"""
import argparse
import os
from pathlib import Path

from .rag import chunk, answer

DOCS_DIR = Path(__file__).resolve().parent.parent / "dataset" / "docs"
CHUNK_SIZE = 120        # words per chunk — tune this
CHUNK_OVERLAP = 20      # word overlap between chunks
TOP_K = 3


def build_index(docs_dir: Path) -> list[dict]:
    """Read every .md doc and return a flat list of {"doc", "text"} chunks."""
    chunks: list[dict] = []
    for path in sorted(docs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for piece in chunk(text, CHUNK_SIZE, CHUNK_OVERLAP):
            chunks.append({"doc": path.name, "text": piece})
    return chunks


def main() -> None:
    ap = argparse.ArgumentParser(description="Answer a question over the corpus with RAG.")
    ap.add_argument("question", help="The question to answer")
    args = ap.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY in your environment first.")

    if not DOCS_DIR.exists():
        raise SystemExit(
            f"Corpus not found at {DOCS_DIR}. Put the sample docs/ folder there "
            "(see your project page → Resources)."
        )

    index = build_index(DOCS_DIR)
    result = answer(args.question, index, k=TOP_K)
    print(result["answer"])
    print("\nSources:", ", ".join(dict.fromkeys(result["sources"])))


if __name__ == "__main__":
    main()
