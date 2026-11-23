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
    "az": ["aze-sound", "aze-orth", "aze-syn", "aze-idiom", "aze-isim", "aze-sifet", "aze-say", "aze-evez", "aze-feil",
           "aze-zerf", "aze-qosma", "aze-bag", "aze-edat", "aze-modal", "aze-nida", "aze-member", "aze-complex", "aze-punct"],
    "en": ["eng-tense", "eng-cond", "eng-passive", "eng-word", "eng-phrasal", "eng-reading"],
}
PER_QUIZ = {"eng-reading": 10}
# «Orta qiymət və moda» 11-ci sinifdə yoxdur
SKIP = {(11, "math"): {"stat-avg"}}

errors, total, ids = [], 0, set()
math_texts = set()
az_keys = set()
for grade in (9, 10, 11):
    for subject, topics in EXPECTED.items():
        f = DATA / f"grade{grade}-{subject}.json"
        if not f.exists():
            errors.append(f"{f.name}: fayl yoxdur")
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        got = [t["topicId"] for t in d["topics"]]
        want = [t for t in topics if t not in SKIP.get((grade, subject), set())]
        if got != want:
            errors.append(f"{f.name}: mövzular uyğun deyil: {got}")
        for t in d["topics"]:
            need = PER_QUIZ.get(t["topicId"], 30 if subject == "az" else 20)
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
                    if "image" in q and not (q["image"].startswith("<svg") and q["image"].endswith("</svg>")):
                        errors.append(f"{qid}: image SVG deyil")
                    if subject == "math":
                        if q["text"] in math_texts:
                            errors.append(f"{qid}: mətn başqa sinifdə/mövzuda təkrarlanır")
                        math_texts.add(q["text"])
                        if grade in (9, 11) and q["difficulty"] != "hard":
                            errors.append(f"{qid}: 9 və 11-ci sinifdə riyaziyyat sualları çətin olmalıdır")
                    if subject == "az":
                        if (q["text"], tuple(sorted(q.get("options", [])))) in az_keys:
                            errors.append(f"{qid}: Azərbaycan dili sualı başqa sinifdə/mövzuda təkrarlanır")
                        az_keys.add((q["text"], tuple(sorted(q.get("options", [])))))
                        if grade in (9, 11) and q["difficulty"] != "hard":
                            errors.append(f"{qid}: 9 və 11-ci sinifdə Azərbaycan dili sualları çətin olmalıdır")
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
