#!/usr/bin/env python3
"""CL - Concept Language prototype: parser, validator, compressor, glosser.

One statement per line:

    [@id] MODE SUBJECT RELATION OBJECT [key=value ...]

    #key=value ...      header line: defaults applied to every statement
    @n                  a statement id; usable as a term to refer to it
    !term               negation
    quant.term          quantifier prefix (all.sys, none.data ...)
    concept:instance    typed instance (sys:srv1, res:mem, val:95)
    q="..."             verbatim text, never paraphrased
"""
import json
import re
import shlex
import sys
from pathlib import Path

LEX = json.loads((Path(__file__).parent / "lexicon.json").read_text())
TERM_CATS = ["entities", "states", "actions", "quantifiers", "modifiers"]
CONCEPTS = {}
for _c in TERM_CATS:
    for _k in LEX[_c]:
        assert _k not in CONCEPTS, f"duplicate concept {_k}"
        CONCEPTS[_k] = _c
for _k in LEX["relations"]:
    assert _k not in CONCEPTS and _k not in LEX["modes"], f"clash {_k}"

# Relations that a pure observation almost never justifies.
INFERRED_RELS = {"cause", "enable", "block", "need"}
MODE_LABEL = {"obs": "OBSERVED", "inf": "INFERRED", "est": "ESTIMATED",
              "unk": "UNKNOWN", "req": "REQUEST", "cmd": "COMMAND", "ack": "ACK"}


class CLError(Exception):
    def __init__(self, code, msg, line=None):
        self.code, self.line = code, line
        super().__init__(f"[{code}]" + (f" line {line}:" if line else "") + f" {msg}")


def parse_term(tok, ids, ln):
    t = {"neg": False, "quant": None, "concept": None, "inst": None, "ref": None}
    if tok.startswith("!"):
        t["neg"], tok = True, tok[1:]
    if tok.startswith("@"):
        if tok not in ids:
            raise CLError("E_REF", f"reference {tok} to unknown/later statement", ln)
        t["ref"] = tok
        return t
    head, sep, inst = tok.partition(":")
    if "." in head:
        q, head = head.split(".", 1)
        if q not in LEX["quantifiers"]:
            raise CLError("E_QUANT", f"unknown quantifier '{q}'", ln)
        t["quant"] = q
    if head not in CONCEPTS:
        raise CLError("E_CONCEPT", f"unknown concept '{head}'", ln)
    if head in LEX["quantifiers"]:
        raise CLError("E_QUANT", f"quantifier '{head}' must prefix a concept", ln)
    t["concept"], t["inst"] = head, (inst if sep else None)
    return t


def parse_fields(toks, ln):
    out = {}
    for tok in toks:
        k, sep, v = tok.partition("=")
        if not sep:
            raise CLError("E_SYNTAX", f"expected key=value, got '{tok}'", ln)
        if k not in LEX["fields"]:
            raise CLError("E_FIELD", f"unknown field '{k}'", ln)
        if k in out:
            raise CLError("E_FIELD", f"duplicate field '{k}'", ln)
        if k in ("conf", "dur"):
            try:
                v = float(v)
            except ValueError:
                raise CLError("E_VALUE", f"{k} must be a number", ln)
            if k == "conf" and not 0 <= v <= 1:
                raise CLError("E_VALUE", "conf must be within 0..1", ln)
        elif k == "t":
            if not re.fullmatch(r"\d+", v):
                raise CLError("E_VALUE", "t must be integer unix seconds", ln)
            v = int(v)
        elif k == "scope" and v not in LEX["quantifiers"]:
            raise CLError("E_VALUE", f"scope must be a quantifier, got '{v}'", ln)
        out[k] = v
    return out


def parse(text):
    """Return (statements, warnings). Raises CLError on the first invalid line."""
    defaults, stmts, warns, ids = {}, [], [], set()
    for ln, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("//"):
            continue
        try:
            toks = shlex.split(line)
        except ValueError as e:
            raise CLError("E_SYNTAX", str(e), ln)
        if line.startswith("#"):
            toks[0] = toks[0][1:]
            defaults.update(parse_fields([x for x in toks if x], ln))
            continue
        sid = None
        if toks[0].startswith("@") and re.fullmatch(r"@\d+", toks[0]):
            sid = toks.pop(0)
            if sid in ids:
                raise CLError("E_REF", f"duplicate id {sid}", ln)
        if len(toks) < 4:
            raise CLError("E_SYNTAX", "need: MODE SUBJECT RELATION OBJECT", ln)
        mode, s, rel, o, *rest = toks
        if "=" in s or "=" in o:
            raise CLError("E_SYNTAX", "a field (key=value) appeared where a term was expected; "
                          "subject or object is missing", ln)
        if mode not in LEX["modes"]:
            raise CLError("E_MODE", f"unknown mode '{mode}'", ln)
        if rel not in LEX["relations"]:
            raise CLError("E_REL", f"unknown relation '{rel}'", ln)
        subj, obj = parse_term(s, ids, ln), parse_term(o, ids, ln)
        fields = {**defaults, **parse_fields(rest, ln)}
        missing = [f for f in LEX["modes"][mode]["needs"] if f not in fields]
        if missing:
            raise CLError("E_MISSING", f"mode '{mode}' requires {missing}", ln)
        if mode == "obs" and rel in INFERRED_RELS:
            warns.append(f"line {ln}: '{rel}' is rarely directly observable; consider mode 'inf'")
        if "q" in fields and mode in ("est", "inf") and "conf" not in fields:
            raise CLError("E_MISSING", "free text needs conf", ln)
        stmts.append({"id": sid, "mode": mode, "s": subj, "rel": rel, "o": obj, "f": fields})
        if sid:
            ids.add(sid)
    return stmts, warns


# ---------- serialisation / compression ----------

def term_str(t):
    if t["ref"]:
        return ("!" if t["neg"] else "") + t["ref"]
    return ("!" if t["neg"] else "") + (t["quant"] + "." if t["quant"] else "") \
        + t["concept"] + (":" + t["inst"] if t["inst"] is not None else "")


def fmt_val(v):
    if isinstance(v, float):
        s = f"{v:.3f}".rstrip("0").rstrip(".")
        return s[1:] if s.startswith("0.") else s      # .95 instead of 0.95
    return shlex.quote(str(v))


def dumps(stmts, factor=True):
    """Serialise; fields identical in every statement move to a '#' header."""
    common = {}
    if factor and len(stmts) > 1:
        keys = set.intersection(*(set(s["f"]) for s in stmts))
        common = {k: stmts[0]["f"][k] for k in keys
                  if all(s["f"][k] == stmts[0]["f"][k] for s in stmts)}
    lines = []
    if common:
        lines.append("#" + " ".join(f"{k}={fmt_val(v)}" for k, v in sorted(common.items())))
    for s in stmts:
        parts = ([s["id"]] if s["id"] else []) + [s["mode"], term_str(s["s"]), s["rel"], term_str(s["o"])]
        parts += [f"{k}={fmt_val(v)}" for k, v in s["f"].items() if k not in common]
        lines.append(" ".join(parts))
    return "\n".join(lines)


# ---------- human gloss (for debugging / audit, never for transport) ----------

def term_gloss(t, verbose=False):
    if t["ref"]:
        return ("NOT " if t["neg"] else "") + f"[statement {t['ref']}]"
    c = t["concept"]
    s = c + (f" '{t['inst']}'" if t["inst"] is not None else "")
    if t["quant"]:
        s = t["quant"].upper() + " " + s
    if t["neg"]:
        s = "NOT " + s
    if verbose:
        s += f" ({LEX[CONCEPTS[c]][c]['def']})"
    return s


def gloss(stmts, verbose=False):
    out = []
    for s in stmts:
        extras = ", ".join(f"{k}={v}" for k, v in s["f"].items())
        out.append(f"{(s['id'] + ' ') if s['id'] else ''}{MODE_LABEL[s['mode']]}: "
                   f"{term_gloss(s['s'], verbose)} --{s['rel'].upper()}--> "
                   f"{term_gloss(s['o'], verbose)}" + (f"  [{extras}]" if extras else ""))
    return "\n".join(out)


# ---------- token counting ----------

def count_tokens(text):
    """Return (count, method). Uses tiktoken if its encoding is obtainable,
    otherwise a pre-tokenizer-style heuristic (words, digit runs, punctuation)."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text)), "tiktoken/cl100k_base"
    except Exception:
        pieces = re.findall(r"[A-Za-z]+|\d{1,3}|[^\sA-Za-z\d]", text)
        n = 0
        for p in pieces:
            n += max(1, -(-len(p) // 6)) if p.isalpha() else 1   # ~6 letters/token for rare words
        return n, "heuristic (approx.)"


def main(argv):
    if len(argv) < 3 or argv[1] not in ("check", "gloss", "pack"):
        print("usage: cl.py check|gloss|pack FILE")
        return 2
    try:
        stmts, warns = parse(Path(argv[2]).read_text())
    except CLError as e:
        print("INVALID", e)
        return 1
    for w in warns:
        print("WARN", w)
    if argv[1] == "check":
        print(f"OK: {len(stmts)} statements")
    elif argv[1] == "gloss":
        print(gloss(stmts, verbose="-v" in argv))
    else:
        print(dumps(stmts))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
