#!/usr/bin/env python3
"""
Deterministic Easy Read lint. No API key needed.

Checks a response for the patterns the skill bans and that can be detected
without a judge: multi-clause joiners (C2), formal words that have an
everyday equivalent (C3), idioms and metaphors (C4), childish or cheerful
decoration (C6), plus two measured checks: any sentence over 20 words (C2)
and any paragraph over 4 sentences (C2).

Usage:
    python lint.py response.md [more.md ...]
    python lint.py --json response.md
    cat response.md | python lint.py -

Exit code is the number of files with at least one finding (max 1 per file),
so it works as a CI gate.
"""
import json
import re
import sys

MULTI_CLAUSE = [
    r"\bhowever\b", r"\bnevertheless\b", r"\bnonetheless\b", r"\bfurthermore\b",
    r"\bmoreover\b", r"\bin addition\b", r"\badditionally\b", r"\bwhereas\b",
    r"\bnotwithstanding\b", r"\bconsequently\b", r"\bthereby\b", r"\bwhereby\b",
    r"\binsofar as\b", r"\bprovided that\b",
]

FORMAL_WORD = [
    r"\butili[sz]\w*\b", r"\bfacilitat\w*\b", r"\bimplement\w*\b", r"\bin order to\b",
    r"\bat this point in time\b", r"\bprior to\b", r"\bsubsequent(ly)?\b",
    r"\bcommence\w*\b", r"\bterminate\w*\b", r"\bpurchas\w*\b", r"\bendeavou?r\b",
    r"\bascertain\b", r"\bexpedite\b", r"\bleverag\w*\b", r"\bpursuant to\b",
    r"\bin the event (of|that)\b", r"\bwith regard to\b", r"\bin accordance with\b",
    r"\baforementioned\b", r"\baccordingly\b", r"\bdesignated\b", r"\bexecute a\b",
    r"\bconfers?\b", r"\bincapacit\w*\b", r"\bobjectives?\b", r"\bindividual circumstances\b",
    r"\bit would be advisable\b", r"\bconsult (an|a|your) (attorney|professional|specialist)\b",
    r"\betc\.?", r"\be\.g\.", r"\bi\.e\.",
]

IDIOMS = [
    r"\bhit the ground running\b", r"\btough nut to crack\b", r"\blow[- ]hanging fruit\b",
    r"\bmove the needle\b", r"\bon the same page\b", r"\bball is in your court\b",
    r"\bbite the bullet\b", r"\bpiece of cake\b", r"\bsilver bullet\b",
    r"\brule of thumb\b", r"\bin a nutshell\b", r"\bthe elephant in the room\b",
    r"\bback to the drawing board\b", r"\bthink outside the box\b",
    r"\bbang for (the|your) buck\b", r"\btake (it|this) with a grain of salt\b",
    r"\bno[- ]brainer\b", r"\bdouble[- ]edged sword\b", r"\bslippery slope\b",
    r"\buphill battle\b", r"\bget the ball rolling\b", r"\bon the fence\b",
    r"\bbreak the bank\b", r"\bcut corners\b", r"\bdown the (road|line)\b",
    r"\bat the end of the day\b", r"\bpeace of mind\b", r"\bsafety net\b",
    r"\bred flag\b", r"\bgreen light\b", r"\bin the long run\b", r"\bon the table\b",
    r"\bkeep in mind\b", r"\bbear in mind\b", r"\bweigh (up )?(the|your) options\b",
    r"\bshop around\b", r"\bfine print\b", r"\bjump through hoops\b", r"\bnail(ed)? down\b",
    r"\bfood for thought\b", r"\ba can of worms\b", r"\bnavigate the\b",
]

CHILDISH = [
    r"\bsuper (easy|simple|fun|important|helpful)\b", r"\btotally\b", r"\bawesome\b",
    r"\bno worries\b", r"\bdon'?t worry\b", r"\byou'?ve got this\b", r"\bgreat job\b",
    r"\bgood job\b", r"\bwell done\b", r"\bfun fact\b", r"\bthink of it like a\b",
    r"\bimagine a (magic|superhero|robot|cookie|toy)\b", r"\blike a (superhero|magic wand|piggy bank)\b",
    r"\bbuddy\b", r"\bokay\?\s*!", r"!{2,}", r"\bgreat question\b", r"\bhope this helps\b",
    r"\blet me know if\b", r"\bfeel free to\b", r"\bi'?d be happy to\b",
]

CHECKS = [
    ("C2 multi-clause joiner", MULTI_CLAUSE),
    ("C3 formal word", FORMAL_WORD),
    ("C4 idiom", IDIOMS),
    ("C6 childish/cheer", CHILDISH),
]

MAX_SENTENCE_WORDS = 20
MAX_PARAGRAPH_SENTENCES = 4

_LIST_MARK = re.compile(r"^\s*(\d+[.)]|[-*•])\s+")
_SENT_END = re.compile(r"(?<=[.!?])\s+")


def _sentences(block: str):
    """Split a block of text into sentences. Each line is its own boundary."""
    out = []
    for line in block.splitlines():
        line = _LIST_MARK.sub("", line).strip()
        if not line:
            continue
        for s in _SENT_END.split(line):
            s = s.strip()
            if s:
                out.append(s)
    return out


def _measure(text: str):
    """Return findings for long sentences and long paragraphs, plus stats."""
    findings = []
    longest = 0
    pos = 0
    for para in re.split(r"\n\s*\n", text):
        start = text.find(para, pos)
        pos = start + len(para)
        if not para.strip() or para.lstrip().startswith("#"):
            continue
        body_lines = [l for l in para.splitlines() if l.strip() and not _LIST_MARK.match(l)]
        list_lines = [l for l in para.splitlines() if _LIST_MARK.match(l)]
        prose_sents = _sentences("\n".join(body_lines))
        all_sents = prose_sents + _sentences("\n".join(list_lines))
        for s in all_sents:
            n = len(re.findall(r"\S+", s))
            longest = max(longest, n)
            if n > MAX_SENTENCE_WORDS:
                findings.append({"check": "C2 sentence >20 words",
                                 "match": f"({n} words) {s[:48]}...", "pos": start + para.find(s[:20])})
        if len(prose_sents) > MAX_PARAGRAPH_SENTENCES:
            findings.append({"check": "C2 paragraph >4 sentences",
                             "match": f"({len(prose_sents)} sentences) {prose_sents[0][:40]}...", "pos": start})
    return findings, longest


def lint(text: str) -> dict:
    findings = []
    low = text.lower()
    for label, patterns in CHECKS:
        for pat in patterns:
            for m in re.finditer(pat, low):
                findings.append({"check": label, "match": text[m.start():m.end()], "pos": m.start()})
    measured, longest = _measure(text)
    findings.extend(measured)
    findings.sort(key=lambda f: f["pos"])
    words = len(text.split())
    questions = text.count("?")
    examples = len(re.findall(r"\bfor example\b", low))
    return {
        "words": words,
        "longest_sentence": longest,
        "questions": questions,
        "examples": examples,
        "findings": findings,
        "clean": not findings,
    }


def main(argv):
    as_json = "--json" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    failed = 0
    out = {}
    for p in paths:
        text = sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()
        r = lint(text)
        out[p] = r
        if not r["clean"]:
            failed += 1
        if not as_json:
            status = "CLEAN" if r["clean"] else f"{len(r['findings'])} finding(s)"
            print(f"{p}: {status}  [{r['words']} words, longest sentence {r['longest_sentence']} words, "
                  f"{r['questions']} question(s), {r['examples']} example(s)]")
            for f in r["findings"]:
                print(f"    {f['check']:<26} \"{f['match']}\"")
    if as_json:
        print(json.dumps(out, indent=2))
    return min(failed, 1)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
