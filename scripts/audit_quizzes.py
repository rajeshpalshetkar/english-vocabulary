#!/usr/bin/env python3
"""Audit exact and normalized duplicate questions across every quiz JSON file."""
import json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUIZZES = ROOT / "content" / "quizzes"

def normalize(value):
    value = unicodedata.normalize("NFKC", str(value or "")).casefold()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())

def main():
    files = sorted(QUIZZES.glob("quiz-*.json"))
    seen = {}
    id_seen = {}
    total = 0
    duplicates = []
    id_duplicates = []
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        for q in data.get("questions", []):
            total += 1
            key = normalize(q.get("question"))
            loc = f"{path.name}:{q.get('id', '?')}"
            if key in seen:
                duplicates.append((loc, seen[key], q.get("question", "")))
            else:
                seen[key] = loc
            qid = str(q.get("id", "")).strip()
            if qid and qid in id_seen:
                id_duplicates.append((loc, id_seen[qid], qid))
            elif qid:
                id_seen[qid] = loc
    print(f"QUIZ AUDIT: {len(files)} files, {total} question slots, {len(seen)} unique normalized question texts")
    print(f"Repeated question texts: {len(duplicates)}")
    for current, original, question in duplicates[:250]:
        print(f"DUPLICATE | {current} | first={original} | {question}")
    print(f"Repeated question IDs: {len(id_duplicates)}")
    for current, original, qid in id_duplicates[:100]:
        print(f"ID DUPLICATE | {current} | first={original} | id={qid}")
    print("NOTE: This checks exact/normalized text only; semantic duplicates require editorial review.")

if __name__ == "__main__":
    main()

# Trigger full repository quiz audit through the configured GitHub Actions path filter.
# Batch checkpoint: 100 original questions added to quizzes 0991-1000.

# Full audit and deployment trigger after replacing quizzes 0971-0980.
