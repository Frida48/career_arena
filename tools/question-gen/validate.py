"""Datasetin yoxlanması: say, unikal id, variantlar, cavab indeksi, boş sahələr."""
import json
import sys
from pathlib import Path

DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "src" / "data" / "questions"
errors, total, ids, texts = [], 0, set(), {}

for f in sorted(DATA.glob("grade*-*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    for s in d["sections"]:
        qs = s["questions"]
        if len(qs) != 30:
            errors.append(f"{f.name}/{s['id']}: {len(qs)} sual (30 olmalıdır)")
        for q in qs:
            total += 1
            qid = q["id"]
            if qid in ids:
                errors.append(f"{qid}: təkrarlanan id")
            ids.add(qid)
            for k in ("text", "explanation", "topic", "difficulty", "type"):
                if not str(q.get(k, "")).strip():
                    errors.append(f"{qid}: boş sahə {k}")
            if q["difficulty"] not in ("easy", "medium", "hard"):
                errors.append(f"{qid}: səhv çətinlik")
            key = (q["text"], q.get("passage"), tuple(sorted(q.get("options", []))))
            if key in texts:
                errors.append(f"{qid}: mətni {texts[key]} ilə eynidir")
            texts[key] = qid
            if q["type"] == "single":
                o = q["options"]
                if len(o) != 5 or len(set(o)) != 5:
                    errors.append(f"{qid}: 5 fərqli variant olmalıdır: {o}")
                if not (0 <= q["correctIndex"] < len(o)):
                    errors.append(f"{qid}: correctIndex səhvdir")
            elif q["type"] == "open":
                if not str(q.get("answer", "")).strip():
                    errors.append(f"{qid}: açıq sualın cavabı yoxdur")
            else:
                errors.append(f"{qid}: naməlum tip {q['type']}")

print(f"{total} sual yoxlanıldı")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("Xəta yoxdur.")
