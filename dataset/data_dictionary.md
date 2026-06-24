# Sample material — `docs/` corpus + `eval_qa.json`

Not a CSV project. Instead of a dataset you get **sample material**: a small
knowledge corpus about a *fictional* product (**Nimbus Notes**) and an evaluation
Q&A set to drive and test your RAG pipeline. **Sample material — Square 1-owned
(synthetic), free for learners.**

> ⚠️ The corpus is written so each eval question has **one clearly best source
> doc** — there is a real, recoverable retrieval signal. Your retriever's job is
> to surface that doc's chunk; your generator's job is to answer **only** from
> retrieved text and **cite the source**. Do not hardcode answers — let
> retrieval + the model produce them, then check against the eval set.

## `docs/` — the knowledge corpus (8 markdown docs)

Eight short docs about Nimbus Notes, each owning a distinct topic so retrieval is
checkable:

| File | Topic it owns |
|---|---|
| `01-getting-started.md` | Creating notebooks, the Free tier basics. |
| `02-pricing-and-plans.md` | Plan tiers, prices, storage limits, billing. |
| `03-sync-and-offline.md` | Sync status, fixing stalled sync, offline edits. |
| `04-sharing-and-permissions.md` | Share roles (Viewer/Commenter/Editor), links. |
| `05-search-and-tags.md` | Search shortcut, tags, combined filters. |
| `06-import-export.md` | Import sources (Evernote/.enex), export formats. |
| `07-security-and-privacy.md` | Encryption, 2FA, account deletion. |
| `08-api-and-integrations.md` | REST API, tokens, rate limit, integrations. |

These are plain markdown — chunk them, embed/score the chunks, and retrieve.

## `eval_qa.json` — 10 evaluation questions

| Field | Type | Description |
|---|---|---|
| `id` | string | `q01`–`q10`. |
| `question` | string | The user question to send through your pipeline. |
| `expected_source_doc` | string | The single doc in `docs/` a correct retriever should rank first — use it to score **retrieval accuracy**. |
| `expected_answer_contains` | array | A few substrings a faithful, grounded answer should include — use them to sanity-check **answer groundedness** (not a strict string match). |
| `note` | string | Plain-English description of the correct answer and which doc it comes from. |

**What to do with it:** for each item, run your pipeline, check whether the
retrieved chunk came from `expected_source_doc` (retrieval hit rate), and whether
the answer contains the `expected_answer_contains` cues and cites the right doc
(groundedness). A correct chunk-level keyword/embedding retriever recovers the
expected doc for **all 10** questions — verify it does.

_Licence: Sample material — Square 1 AI-owned, synthetic. No attribution
required. Free for learners. Regenerate with `generate_dataset.py` (seed 42)._
