# Smart Document Q&A (RAG) — Square 1 AI starter

**Part of [Square 1 AI](https://square1-tutor.vercel.app) · Generative AI · Project 2.**

✅ **Data included.** The dataset is committed in [`dataset/`](dataset/) and is the **same standardized dataset every learner uses** — so results are comparable. It is 100% synthetic and Square 1-owned (no third-party or personal data). You can also download it as a single file from the project page on Square 1.

To run the commands below, copy the files into `data/` (`mkdir -p data && cp -r dataset/* data/`) or point the commands straight at `dataset/`.

MIT licensed — fork it, build on it, put it in your portfolio.

---

# Smart Document Q&A (RAG) — starter

Starter for Square 1 AI **Generative AI · Project 2**. Build a Retrieval-Augmented Generation pipeline that indexes documents, retrieves the relevant chunks, and answers questions **with citations**.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Get the material
The sample material lives on your project page (Resources): a `docs/` corpus of 8 markdown docs about *Nimbus Notes* and a 10-item `eval_qa.json`. Put them in a `dataset/` folder next to `rag/` so `python -m rag.cli` can load the corpus:
```
starter/
  rag/
  dataset/
    docs/*.md
    eval_qa.json
```

## Your task
Three tests define the contract — they run **offline** (no API key; the scorer is deterministic and the LLM is never called) and fail until you implement the stubs in `rag/rag.py`:
```bash
pytest -q
```
Then wire `answer` to the Anthropic SDK and run the pipeline:
```bash
export ANTHROPIC_API_KEY=sk-ant-...      # Windows: set ANTHROPIC_API_KEY=...
python -m rag.cli "How much does the Pro plan cost?"
```
Pipeline: `chunk` (overlapping, size-respecting) → `score` (deterministic relevance) → `retrieve` (top-k, highest first) → `build_prompt` (contexts + question, "answer only from these, cite the source") → `answer` (Anthropic call, returns answer + sources).

**Model + key:** use a current id — `claude-sonnet-4-6` (default) or `claude-haiku-4-5-20251001` (cheaper). Read `ANTHROPIC_API_KEY` from the environment; **never hardcode it**. Never use a `claude-3-*` id. The 3 tests must keep passing with no key set.

Then run your pipeline against `eval_qa.json`: for each question, check whether the retrieved chunk came from `expected_source_doc` (retrieval accuracy) and whether the answer contains the expected cues and cites the right doc (groundedness). Write up your chunk size/overlap, `k`, and the accuracy you got. Full brief, rubric, and references are on your Square 1 project page. MIT licensed.
