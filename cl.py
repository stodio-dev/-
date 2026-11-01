#!/usr/bin/env python3
"""CL - Concept Language: parser, validator, compressor, glosser. Version follows lexicon.json.

One statement per line:

    [@id] MODE SUBJECT [!]RELATION OBJECT [key=value ...]

    #key=value ...      header line: defaults for every following statement
                        (#t0=N sets the base for relative times t=+N)
    @n                  a statement id; usable as a term to refer to it
    !term / !rel        negation of a term / of the relation
    quant.term          quantifier prefix (all.sys, none.data ...)
    concept:instance    typed instance (sys:srv1, res:mem, val:95)
    q="..."             verbatim text, never paraphrased

commands: cl.py check|gloss|pack FILE   |   cl.py lexicon   (compact lexicon for transport)
"""
import json
import math
import re
import shlex
import sys
from pathlib import Path

LEX = json.loads((Path(__file__).parent / "lexicon.json").read_text())
TERM_CATS = ["entities", "states", "actions", "quantifiers"]
CONCEPTS = {}
for _c in TERM_CATS:
    for _k in LEX[_c]:
        assert _k not in CONCEPTS, f"duplicate concept {_k}"
        CONCEPTS[_k] = _c
for _k in LEX["relations"]:
    assert _k not in CONCEPTS and _k not in LEX["modes"], f"clash {_k}"

# Relations that a pure observation almost never justifies (negated or not).
INFERRED_RELS = {"cause", "enable", "block", "need"}

# Field defaults come from the lexicon: applied by parse(), never serialised by dumps().
DEFAULTS = {k: v["default"] for k, v in LEX["fields"].items() if v.get("default") is not None}
HEADER_ONLY = {"t0"}
MODE_LABEL = {"obs": "OBSERVED", "inf": "INFERRED", "est": "ESTIMATED", "pred": "PREDICTED",
              "unk": "UNKNOWN", "req": "REQUEST", "cmd": "COMMAND", "ack": "ACK"}
_CTX = re.compile(r"[A-Za-z0-9_.\-]+")


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


def parse_fields(toks, ln, t0=None):
    """Parse key=value tokens. A relative time t=+N is resolved against t0."""
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
            if not math.isfinite(v):
                raise CLError("E_VALUE", f"{k} must be finite", ln)
            if k == "conf" and not 0 <= v <= 1:
                raise CLError("E_VALUE", "conf must be within 0..1", ln)
        elif k == "t":
            if re.fullmatch(r"\d+", v):
                v = int(v)
            elif re.fullmatch(r"\+\d+", v):
                if t0 is None:
                    raise CLError("E_MISSING", "relative time t=+N needs a #t0 header", ln)
                v = t0 + int(v[1:])
            else:
                raise CLError("E_VALUE", "t must be integer unix seconds or +N", ln)
        elif k == "t0":
            if not re.fullmatch(r"\d+", v):
                raise CLError("E_VALUE", "t0 must be integer unix seconds", ln)
            v = int(v)
        elif k == "ctx" and not _CTX.fullmatch(v):
            raise CLError("E_VALUE", "ctx may contain only letters, digits, '.', '_' and '-'", ln)
        elif k == "scope" and v not in LEX["quantifiers"]:
            raise CLError("E_VALUE", f"scope must be a quantifier, got '{v}'", ln)
        out[k] = v
    return out


def parse(text):
    """Return (statements, warnings). Raises CLError on the first invalid line."""
    defaults, stmts, warns, ids, t0 = {}, [], [], set(), None
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
            toks = [x for x in toks if x]
            base = [x for x in toks if x.startswith("t0=")]          # t0 first, so t=+N in the same line works
            if base:
                t0 = parse_fields(base, ln)["t0"]
            defaults.update(parse_fields([x for x in toks if not x.startswith("t0=")], ln, t0))
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
        rneg = rel.startswith("!")
        rel = rel[1:] if rneg else rel
        if rel not in LEX["relations"]:
            raise CLError("E_REL", f"unknown relation '{rel}'", ln)
        subj, obj = parse_term(s, ids, ln), parse_term(o, ids, ln)
        if mode == "ack" and subj["ref"] is None:
            raise CLError("E_SYNTAX", "ack: the subject must be the @N being acknowledged", ln)
        bad = [x for x in rest if x.partition("=")[0] in HEADER_ONLY]
        if bad:
            raise CLError("E_FIELD", f"'{bad[0].partition('=')[0]}' is allowed only in a # header", ln)
        fields = {**DEFAULTS, **defaults, **parse_fields(rest, ln, t0)}
        missing = [f for f in LEX["modes"][mode]["needs"] if f not in fields]
        if missing:
            raise CLError("E_MISSING", f"mode '{mode}' requires {missing}", ln)
        if mode == "obs" and rel in INFERRED_RELS:
            warns.append(f"line {ln}: '{rel}' is rarely directly observable; consider mode 'inf'")
        if "q" in fields and mode in ("est", "inf") and "conf" not in fields:
            raise CLError("E_MISSING", "free text needs conf", ln)
        stmts.append({"id": sid, "mode": mode, "s": subj, "rel": rel, "rneg": rneg, "o": obj, "f": fields})
        if sid:
            ids.add(sid)
    return stmts, warns


# ---------- serialisation / compression ----------

_PLAIN = re.compile(r"[^\s'\"\\]*")


def quote_tok(tok):
    """Quote only when shlex would otherwise split or alter the token (keeps '!' and '.' bare)."""
    return tok if _PLAIN.fullmatch(tok) else shlex.quote(tok)


def term_str(t):
    if t["ref"]:
        return ("!" if t["neg"] else "") + t["ref"]
    return quote_tok(("!" if t["neg"] else "") + (t["quant"] + "." if t["quant"] else "")
                     + t["concept"] + (":" + t["inst"] if t["inst"] is not None else ""))


def fmt_val(v):
    if isinstance(v, float):
        s = repr(v)                                    # shortest string that round-trips exactly
        if s.endswith(".0"):
            s = s[:-2]
        if s.startswith("0."):
            s = s[1:]                                  # .95 instead of 0.95
        elif s.startswith("-0."):
            s = "-" + s[2:]
        return s
    return shlex.quote(str(v))


def explicit_fields(f):
    """Fields that differ from the lexicon default; defaults are never serialised."""
    return {k: v for k, v in f.items() if DEFAULTS.get(k) != v}


def dumps(stmts, factor=True):
    """Serialise compactly without reordering statements.

    - Times become offsets from a #t0 base when they differ.
    - A field present in every statement is groupable: a run of 2+ equal values becomes a
      '#' header change, and statements matching the current header omit it.
    - A field missing from any statement is always written inline, so a header can never
      leak a value into a statement that did not have it.
    """
    fl = [explicit_fields(s["f"]) for s in stmts]
    factor = factor and len(stmts) > 1
    ts = [f.get("t") for f in fl]
    t0 = min(ts) if factor and all(isinstance(x, int) for x in ts) and len(set(ts)) > 1 else None

    def val(k, v):
        return f"+{v - t0}" if k == "t" and t0 is not None else fmt_val(v)

    groupable = sorted(set.intersection(*(set(f) for f in fl))) if factor else []
    cur, lines = {}, []
    for i, (s, f) in enumerate(zip(stmts, fl)):
        change = {}
        for k in groupable:
            if cur.get(k, cur) == f[k]:                 # `cur` as sentinel: never equals a value
                continue
            run = 1
            while i + run < len(fl) and fl[i + run][k] == f[k]:
                run += 1
            if run >= 2:
                change[k] = f[k]
        cur.update(change)
        head = [f"{k}={val(k, v)}" for k, v in change.items()]
        if i == 0 and t0 is not None:
            head.append(f"t0={t0}")
        if head:
            lines.append("#" + " ".join(head))
        rel = ("!" if s["rneg"] else "") + s["rel"]
        parts = ([s["id"]] if s["id"] else []) + [s["mode"], term_str(s["s"]), rel, term_str(s["o"])]
        parts += [f"{k}={val(k, v)}" for k, v in f.items() if not (k in groupable and cur.get(k, cur) == v)]
        lines.append(" ".join(parts))
    return "\n".join(lines)


# ---------- compact lexicon for transport ----------

def lexicon_text():
    """The lexicon as compact text (fewer tokens than JSON). Generated; lexicon.txt must match it."""
    L = [f"CL {LEX['version']} (compact; full spec: SPEC.md). One statement per line: [@N] MODE SUBJECT [!]REL OBJECT key=value...",
         "TERM: [!][quant.]concept[:instance] | [!]@N (earlier statement; ids unique per message). !REL negates the relation.",
         "#key=value line: default for all following lines until changed; a statement's own field overrides it.",
         "t: unix seconds or +N meaning t0+N (#t0=N, header only). ctx: context id. q=\"...\": verbatim text only.",
         "A statement missing a field its mode requires is invalid. Below: code: definition | not: confusable"]
    L.append("MODES (required fields in braces)")
    L += [f"{k} {{{' '.join(v['needs'])}}}: {v['def']}" for k, v in LEX["modes"].items()]
    for cat, title in (("relations", "RELATIONS (A rel B; !rel negates)"), ("entities", "ENTITIES"),
                       ("states", "STATES"), ("actions", "ACTIONS"), ("quantifiers", "QUANTIFIERS (prefix: all.sys)")):
        L.append(title)
        L += [f"{k}: {v['def']} | not: {v['not']}" for k, v in LEX[cat].items()]
    L.append("FIELDS")
    L += [f"{k}: {v['def']}" + (f" (default {v['default']})" if v.get("default") is not None else "")
          for k, v in LEX["fields"].items()]
    return "\n".join(L) + "\n"


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
        extras = ", ".join(f"{k}={v}" for k, v in explicit_fields(s["f"]).items())
        rel = ("NOT " if s["rneg"] else "") + s["rel"].upper()
        out.append(f"{(s['id'] + ' ') if s['id'] else ''}{MODE_LABEL[s['mode']]}: "
                   f"{term_gloss(s['s'], verbose)} --{rel}--> "
                   f"{term_gloss(s['o'], verbose)}" + (f"  [{extras}]" if extras else ""))
    return "\n".join(out)


# ---------- token counting ----------

def count_tokens(text):
    """Return (count, method). Uses tiktoken if its encoding is obtainable, otherwise a rough
    heuristic. For real numbers use tools/count_tokens.mjs (bundled vocabularies, no network)."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text)), "tiktoken/cl100k_base"
    except Exception:
        pieces = re.findall(r"[A-Za-z]+|\d{1,3}|[^\sA-Za-z\d]", text)
        n = 0
        for p in pieces:
            n += max(1, -(-len(p) // 6)) if p.isalpha() else 1   # ~6 letters/token for rare words
        return n, "heuristic (rough; real counts: tools/count_tokens.mjs)"


def main(argv):
    if len(argv) == 2 and argv[1] == "lexicon":
        sys.stdout.write(lexicon_text())
        return 0
    if len(argv) < 3 or argv[1] not in ("check", "gloss", "pack"):
        print("usage: cl.py check|gloss|pack FILE   |   cl.py lexicon")
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
