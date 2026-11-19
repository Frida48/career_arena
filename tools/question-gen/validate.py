"""Sual bankının yoxlanması:
- hər sinif × fənn faylında gözlənilən mövzular var
- hər mövzuda 3 quiz × 20 sual (Reading: 3 × 10)
- unikal id, boş sahə yoxdur, çətinlik orta/çətin
- variantlı suallarda 5 fərqli variant və düzgün cavab indeksi
- quiz daxilində eyni sual təkrarlanmır"""
import json
import sys
from pathlib import Path

DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "src" / "data" / "questions"
EXPECTED = {
    "math": ["num-real", "num-frac", "num-pow", "num-abs", "num-pct", "alg-eq", "alg-sys", "alg-quad", "alg-prog", "alg-func",
             "geo-basic", "geo-poly", "geo-circle", "geo-trig", "stat-avg", "stat-prob"],
    "az": ["aze-sound", "aze-orth", "aze-syn", "aze-idiom", "aze-noun", "aze-verb", "aze-member", "aze-complex"],
    "en": ["eng-tense", "eng-cond", "eng-passive", "eng-word", "eng-phrasal", "eng-reading"],
}
PER_QUIZ = {"eng-reading": 10}

errors, total, ids = [], 0, set()
for grade in (9, 10, 11):
    for subject, topics in EXPECTED.items():
        f = DATA / f"grade{grade}-{subject}.json"
        if not f.exists():
            errors.append(f"{f.name}: fayl yoxdur")
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        got = [t["topicId"] for t in d["topics"]]
        if got != topics:
            errors.append(f"{f.name}: mövzular uyğun deyil: {got}")
        for t in d["topics"]:
            need = PER_QUIZ.get(t["topicId"], 20)
            if len(t["quizzes"]) != 3:
                errors.append(f"{f.name}/{t['topicId']}: {len(t['quizzes'])} quiz (3 olmalıdır)")
            seen_topic = set()
            for qi, quiz in enumerate(t["quizzes"], 1):
                if len(quiz) != need:
                    errors.append(f"{f.name}/{t['topicId']}/quiz{qi}: {len(quiz)} sual ({need} olmalıdır)")
                for q in quiz:
                    total += 1
                    qid = q["id"]
                    if qid in ids:
                        errors.append(f"{qid}: təkrarlanan id")
                    ids.add(qid)
                    for k in ("text", "explanation", "difficulty", "type"):
                        if not str(q.get(k, "")).strip():
                            errors.append(f"{qid}: boş sahə {k}")
                    if q["difficulty"] not in ("medium", "hard"):
                        errors.append(f"{qid}: çətinlik orta və ya çətin olmalıdır")
                    key = (q["text"], q.get("passage"), tuple(sorted(q.get("options", []))), q.get("answer"))
                    if key in seen_topic:
                        errors.append(f"{qid}: mövzuda təkrarlanan sual")
                    seen_topic.add(key)
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
    print("\n".join(errors[:50]))
    print(f"... cəmi {len(errors)} xəta" if len(errors) > 50 else "")
    sys.exit(1)
print("Xəta yoxdur.")
