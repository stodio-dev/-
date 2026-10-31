# CL v0.1 – Concept Language (prototype)

A compact, domain-neutral language for machine-to-machine (and model-to-model) technical messages.
Goals: fewer tokens, no drift, no concept confusion, no translation through natural language.

## Principles
1. **Concepts, not words.** Every symbol maps to one atomic concept in `lexicon.json`. No synonyms, no polysemy.
2. **Every concept carries a contrast** (`not` field): the nearest concept it must not be confused with
   (e.g. `cause` vs `corr`, `fail` vs `stop`, `data` vs `store`).
3. **Epistemic status is grammar.** Every statement has a mode (`obs inf est unk req cmd ack`).
   Each mode has mandatory fields (source, time, and confidence for `inf`/`est`).
   A statement without them is *invalid*, not just vague.
4. **No paraphrase.** Free text is allowed only as `q="..."` and is always a verbatim quotation.
5. **Cheap tokens.** Codes are short ASCII words that common tokenizers usually keep whole.
   Emoji/symbols are a display layer only.
6. **Defaults are omitted; exceptions are explicit.** Fields shared by all statements move to a `#` header.

## Grammar
```
message   := (header | statement)*
header    := '#' field+                     # defaults for every statement below
statement := ['@'N] MODE TERM REL TERM field*
TERM      := ['!'] [QUANT '.'] CONCEPT [':' instance]  |  ['!'] '@'N
field     := key '=' value                  # conf src t scope dur unit q
```
- `@N` labels a statement; later statements may use `@N` as a term (causal chains, conditions).
- `!` negates a term; `QUANT.` is one of `all some one none many`.
- `concept:instance` names a specific thing: `sys:srv1`, `res:mem`, `val:92`.

## Validation rules (E_* codes)
| Code | Meaning |
|---|---|
| E_SYNTAX | wrong shape, or subject/object missing |
| E_MODE / E_REL / E_CONCEPT / E_QUANT | unknown symbol |
| E_FIELD / E_VALUE | unknown/duplicate field, bad value (e.g. conf outside 0..1) |
| E_MISSING | mode requires a field that is absent |
| E_REF | `@N` reference to unknown or later statement |
| WARN | e.g. `obs` used with `cause/enable/block/need` (causation is rarely observed; use `inf`) |

## Example
```
#src=mon t=1730415600
@1 obs sys:srv1 has fail
@2 inf res:mem has full conf=.95
@3 inf @2 cause @1 conf=.95
```
= "Monitor observed srv1 failing; it infers (95%) that memory was full and that this caused the failure."

## Known limits of v0.1
- Token savings are measured with a heuristic counter only (tiktoken could not download its encoding here). Re-measure with the real tokenizer of the target model.
- The receiver must know the lexicon. It pays off when the lexicon is cached or the conversation is long.
- ~65 concepts, all general-purpose. Domain extensions (network, medical, finance...) should be separate lexicon files with their own contrast pairs.
- Units, numeric ranges, sets and nested conditions are minimal.
- Not yet tested on a real LLM: the key open experiment is whether a model reading CL drifts less than one reading prose.
